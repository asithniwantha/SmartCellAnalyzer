# Battery Charger Controller with Asyncio Support
# Raspberry Pi Pico 2 W (RP2350) with INA3221 and PCA9685

from src.drivers import INA3221Sensor, PCA9685
import time
import asyncio
from machine import Pin, I2C
import math


class BatteryChargerController:
    """
    A comprehensive battery charger controller that uses:
    - INA3221 for voltage and current monitoring
    - PCA9685 for PWM control of charging circuit

    Features:
    - Voltage regulation
    - Current limiting
    - Multiple charging modes (CC, CV, Custom)
    - Safety limits and monitoring
    - Real-time parameter adjustment
    """

    # Charging modes
    MODE_VOLTAGE_REGULATION = "voltage_regulation"
    MODE_CURRENT_LIMITING = "current_limiting"
    MODE_CC_CV = "cc_cv"  # Constant Current / Constant Voltage
    MODE_CUSTOM = "custom"
    MODE_STOPPED = "stopped"

    def __init__(self,
                 # INA3221 Configuration
                 ina_scl_pin=21, ina_sda_pin=20, ina_channel=0, ina_address=0x40,
                 # PCA9685 Configuration
                 pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
                 # Control Parameters
                 target_voltage=7.2, target_current=1000,
                 voltage_tolerance=0.05, current_tolerance=50,
                 duty_step=2, min_duty=0, max_duty=4095,
                 update_interval=0.01,
                 # Hybrid control parameters
                 sensor_read_interval=None, pwm_update_interval=None):
        """
        Initialize the battery charger controller.

        Args:
            ina_scl_pin (int): INA3221 SCL pin (default: 21)
            ina_sda_pin (int): INA3221 SDA pin (default: 20)
            ina_channel (int): INA3221 channel to monitor (0-2, default: 0)
            ina_address (int): INA3221 I2C address (0x40, 0x41, 0x42, or 0x43, default: 0x40)
            pca_scl_pin (int): PCA9685 SCL pin (default: 19)
            pca_sda_pin (int): PCA9685 SDA pin (default: 18)
            pca_channel (int): PCA9685 channel to control (default: 1)
            pca_freq (int): PCA9685 PWM frequency (default: 1526)
            target_voltage (float): Target voltage in volts (default: 7.2)
            target_current (float): Target current in mA (default: 1000)
            voltage_tolerance (float): Voltage tolerance in volts (default: 0.05)
            current_tolerance (float): Current tolerance in mA (default: 50)
            duty_step (int): PWM duty cycle step size (default: 2)
            min_duty (int): Minimum duty cycle (default: 0)
            max_duty (int): Maximum duty cycle (default: 4095)
            update_interval (float): Control loop update interval in seconds (default: 0.01)
            sensor_read_interval (float): Sensor read interval (None = use update_interval)
            pwm_update_interval (float): PWM update interval (None = use update_interval)
        
        Note: Multiple INA3221 modules can be used on the same I2C bus with different addresses:
            - 0x40 (default): Channels 0-2
            - 0x41: Channels 3-5  
            - 0x42: Channels 6-8
            - 0x43: Channels 9-11
        
        Hybrid Mode:
            When sensor_read_interval and pwm_update_interval are specified separately,
            the controller uses hybrid mode for optimal performance:
            - Sensors read at slower rate (e.g., 10ms) to save CPU
            - PWM updates at faster rate (e.g., 1ms) for quick response
            - Cached sensor data used for PWM control between reads
        """

        # Hardware configuration
        self.ina_channel = ina_channel
        self.ina_address = ina_address
        self.pca_channel = pca_channel

        # Control parameters
        self.target_voltage = target_voltage
        self.target_current = target_current
        self.voltage_tolerance = voltage_tolerance
        self.current_tolerance = current_tolerance
        self.duty_step = duty_step
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.update_interval = update_interval
        
        # Hybrid mode timing
        self.sensor_read_interval = sensor_read_interval if sensor_read_interval is not None else update_interval
        self.pwm_update_interval = pwm_update_interval if pwm_update_interval is not None else update_interval
        self.hybrid_mode = (sensor_read_interval is not None and pwm_update_interval is not None)
        
        # Cached measurements for hybrid mode
        self.cached_measurements = None
        self.last_sensor_read = 0

        # Current state
        self.current_duty = 1000
        self.current_mode = self.MODE_STOPPED
        self.is_running = False

        # Safety limits
        self.max_voltage = 30.0  # Maximum safe voltage
        self.max_current = 5000  # Maximum safe current in mA
        self.min_voltage = 0.1   # Minimum voltage threshold

        # Statistics
        self.cycle_count = 0
        self.total_energy = 0.0  # Wh
        self.start_time = 0

        # Initialize hardware
        self._initialize_hardware(
            ina_scl_pin, ina_sda_pin, ina_address, pca_scl_pin, pca_sda_pin, pca_freq)

    def _initialize_hardware(self, ina_scl, ina_sda, ina_addr, pca_scl, pca_sda, pca_freq):
        """Initialize INA3221 and PCA9685 hardware."""
        try:
            print("Initializing Battery Charger Controller...")

            # Initialize INA3221
            print(f"Setting up INA3221 at address {hex(ina_addr)} on I2C0 (SCL=GP{ina_scl}, SDA=GP{ina_sda})")
            self.ina3221 = INA3221Sensor(scl_pin=ina_scl, sda_pin=ina_sda, address=ina_addr)

            # Initialize PCA9685
            print(
                f"Setting up PCA9685 on I2C1 (SCL=GP{pca_scl}, SDA=GP{pca_sda})")
            self.i2c_pca = I2C(1, sda=Pin(pca_sda),
                               scl=Pin(pca_scl), freq=400000)
            self.pca9685 = PCA9685(i2c=self.i2c_pca, address=0x40)
            self.pca9685.freq(pca_freq)

            # Set initial duty cycle
            self.pca9685.duty(self.pca_channel, self.current_duty)

            print("Hardware initialization complete!")

        except Exception as e:
            print(f"Hardware initialization failed: {e}")
            raise

    def read_measurements(self):
        """
        Read current voltage, current, and power measurements.

        Returns:
            dict: Dictionary containing voltage, current, and power measurements
        """
        try:
            data = self.ina3221.read_channel(self.ina_channel)
            voltage = data['bus_voltage']
            current = data['current']
            power = voltage * current / 1000  # Convert to watts

            return {
                'voltage': voltage,
                'current': current,
                'power': power,
                'duty_cycle': self.current_duty,
                'timestamp': time.ticks_ms()
            }
        except Exception as e:
            print(f"Error reading measurements: {e}")
            return {
                'voltage': float('nan'),
                'current': float('nan'),
                'power': float('nan'),
                'duty_cycle': self.current_duty,
                'timestamp': time.ticks_ms()
            }

    def set_target_voltage(self, voltage):
        """
        Set the target voltage for regulation.

        Args:
            voltage (float): Target voltage in volts
        """
        if voltage < 0 or voltage > self.max_voltage:
            print(
                f"Warning: Voltage {voltage}V outside safe range (0-{self.max_voltage}V)")
            return False

        self.target_voltage = voltage
        print(f"Target voltage set to {voltage}V")
        return True

    def set_target_current(self, current):
        """
        Set the target current for regulation.

        Args:
            current (float): Target current in mA
        """
        if current < 0 or current > self.max_current:
            print(
                f"Warning: Current {current}mA outside safe range (0-{self.max_current}mA)")
            return False

        self.target_current = current
        print(f"Target current set to {current}mA")
        return True

    def set_duty_cycle(self, duty):
        """
        Manually set the PWM duty cycle.

        Args:
            duty (int): Duty cycle value (0-4095)
        """
        if duty < self.min_duty or duty > self.max_duty:
            print(
                f"Duty cycle {duty} outside range ({self.min_duty}-{self.max_duty})")
            return False

        self.current_duty = duty
        self.pca9685.duty(self.pca_channel, duty)
        print(f"Duty cycle set to {duty}")
        return True

    def set_control_parameters(self, duty_step=None, voltage_tolerance=None, current_tolerance=None, update_interval=None):
        """
        Adjust control loop parameters.

        Args:
            duty_step (int): PWM step size
            voltage_tolerance (float): Voltage regulation tolerance
            current_tolerance (float): Current regulation tolerance  
            update_interval (float): Control loop update interval
        """
        if duty_step is not None:
            self.duty_step = duty_step
            print(f"Duty step set to {duty_step}")

        if voltage_tolerance is not None:
            self.voltage_tolerance = voltage_tolerance
            print(f"Voltage tolerance set to {voltage_tolerance}V")

        if current_tolerance is not None:
            self.current_tolerance = current_tolerance
            print(f"Current tolerance set to {current_tolerance}mA")

        if update_interval is not None:
            self.update_interval = update_interval
            print(f"Update interval set to {update_interval}s")

    def _safety_check(self, measurements):
        """
        Perform safety checks on measurements.

        Args:
            measurements (dict): Current measurements

        Returns:
            bool: True if safe, False if unsafe
        """
        voltage = measurements['voltage']
        current = measurements['current']

        if math.isnan(voltage) or math.isnan(current):
            print("Warning: Invalid measurements detected")
            return False

        if voltage > self.max_voltage:
            print(
                f"SAFETY: Voltage {voltage}V exceeds maximum {self.max_voltage}V")
            return False

        if current > self.max_current:
            print(
                f"SAFETY: Current {current}mA exceeds maximum {self.max_current}mA")
            return False

        return True

    def _voltage_regulation_step(self, measurements):
        """Perform one step of voltage regulation with adaptive step size."""
        voltage = measurements['voltage']
        voltage_error = voltage - self.target_voltage

        if abs(voltage_error) <= self.voltage_tolerance:
            return  # Within tolerance

        # Adaptive step size based on error magnitude
        # Larger error = bigger steps (faster response)
        # Smaller error = smaller steps (precise control)
        if abs(voltage_error) > 1.0:  # Large error (>1V)
            step = self.duty_step * 8  # 8x speed
        elif abs(voltage_error) > 0.5:  # Medium error (>0.5V)
            step = self.duty_step * 4  # 4x speed
        elif abs(voltage_error) > 0.2:  # Small error (>0.2V)
            step = self.duty_step * 2  # 2x speed
        else:  # Very small error (<0.2V)
            step = self.duty_step  # Normal speed

        if voltage_error > 0:  # Voltage too high
            new_duty = min(self.current_duty + step, self.max_duty)
            if new_duty != self.current_duty:
                self.current_duty = new_duty
                self.pca9685.duty(self.pca_channel, self.current_duty)
        else:  # Voltage too low
            new_duty = max(self.current_duty - step, self.min_duty)
            if new_duty != self.current_duty:
                self.current_duty = new_duty
                self.pca9685.duty(self.pca_channel, self.current_duty)

    def _current_regulation_step(self, measurements):
        """Perform one step of current regulation with adaptive step size."""
        current = measurements['current']
        current_error = current - self.target_current

        if abs(current_error) <= self.current_tolerance:
            return  # Within tolerance

        # Adaptive step size based on error magnitude
        if abs(current_error) > 500:  # Large error (>500mA)
            step = self.duty_step * 8
        elif abs(current_error) > 250:  # Medium error (>250mA)
            step = self.duty_step * 4
        elif abs(current_error) > 100:  # Small error (>100mA)
            step = self.duty_step * 2
        else:  # Very small error (<100mA)
            step = self.duty_step

        if current_error > 0:  # Current too high
            new_duty = min(self.current_duty + step, self.max_duty)
            if new_duty != self.current_duty:
                self.current_duty = new_duty
                self.pca9685.duty(self.pca_channel, self.current_duty)
        else:  # Current too low
            new_duty = max(self.current_duty - step, self.min_duty)
            if new_duty != self.current_duty:
                self.current_duty = new_duty
                self.pca9685.duty(self.pca_channel, self.current_duty)

    def _cc_cv_step(self, measurements):
        """Perform CC/CV (Constant Current/Constant Voltage) regulation."""
        voltage = measurements['voltage']
        current = measurements['current']

        # In CC/CV mode, prioritize current limiting until voltage target is reached
        if voltage < self.target_voltage:
            # Constant Current phase
            self._current_regulation_step(measurements)
        else:
            # Constant Voltage phase
            self._voltage_regulation_step(measurements)

    async def start_regulation(self, mode=None):
        """
        Start the regulation control loop asynchronously with hybrid mode support.

        Args:
            mode (str): Regulation mode (voltage_regulation, current_limiting, cc_cv, custom)
        
        Hybrid Mode:
            If sensor_read_interval and pwm_update_interval are set differently,
            the controller operates in hybrid mode:
            - Sensor reads at sensor_read_interval (e.g., 10ms)
            - PWM updates at pwm_update_interval (e.g., 1ms)
            - Cached sensor data used between reads for faster PWM response
        """
        if mode is None:
            mode = self.MODE_VOLTAGE_REGULATION

        if mode not in [self.MODE_VOLTAGE_REGULATION, self.MODE_CURRENT_LIMITING,
                        self.MODE_CC_CV, self.MODE_CUSTOM]:
            print(f"Invalid mode: {mode}")
            return False

        self.current_mode = mode
        self.is_running = True
        self.cycle_count = 0
        self.start_time = time.ticks_ms()
        self.last_sensor_read = 0
        self.cached_measurements = None

        print("===="*10)
        print(f"Starting {mode} mode")
        if self.hybrid_mode:
            print(f"HYBRID MODE: Sensor={self.sensor_read_interval*1000:.1f}ms, PWM={self.pwm_update_interval*1000:.1f}ms")
        print(f"Target: V={self.target_voltage}V, I={self.target_current}mA")
        print("Press Ctrl+C to stop")

        try:
            while self.is_running:
                current_time = time.ticks_ms()
                
                # Hybrid mode: Read sensor only when interval elapsed
                if self.hybrid_mode:
                    if self.cached_measurements is None or \
                       time.ticks_diff(current_time, self.last_sensor_read) >= self.sensor_read_interval * 1000:
                        self.cached_measurements = self.read_measurements()
                        self.last_sensor_read = current_time
                        
                        # Safety check only when we have fresh data
                        if not self._safety_check(self.cached_measurements):
                            print("Safety check failed - stopping regulation")
                            break
                    
                    measurements = self.cached_measurements
                    update_interval = self.pwm_update_interval
                else:
                    # Standard mode: Read sensor every cycle
                    measurements = self.read_measurements()
                    
                    # Safety check
                    if not self._safety_check(measurements):
                        print("Safety check failed - stopping regulation")
                        break
                    
                    update_interval = self.update_interval

                # Execute control step based on mode (uses cached or fresh data)
                if mode == self.MODE_VOLTAGE_REGULATION:
                    self._voltage_regulation_step(measurements)
                elif mode == self.MODE_CURRENT_LIMITING:
                    self._current_regulation_step(measurements)
                elif mode == self.MODE_CC_CV:
                    self._cc_cv_step(measurements)
                # MODE_CUSTOM can be implemented by overriding this method

                # Update statistics
                self.cycle_count += 1
                if self.cycle_count % 2000 == 0:  # Print every 2000 cycles
                    self._print_status(measurements)

                # Wait for next cycle (non-blocking)
                await asyncio.sleep(update_interval)

        except asyncio.CancelledError:
            print("\nRegulation cancelled")
        except Exception as e:
            print(f"Error in regulation loop: {e}")
        finally:
            self.stop_regulation()

    def stop_regulation(self):
        """Stop the regulation control loop."""
        self.is_running = False
        self.current_mode = self.MODE_STOPPED

        # Final measurements
        final_measurements = self.read_measurements()

        print(f"\nRegulation stopped")
        print(f"Final measurements:")
        print(f"  Voltage: {final_measurements['voltage']:.3f}V")
        print(f"  Current: {final_measurements['current']:.3f}mA")
        print(f"  Power: {final_measurements['power']:.3f}W")
        print(f"  Duty Cycle: {self.current_duty}")
        print(f"  Total Cycles: {self.cycle_count}")

        self.set_duty_cycle(self.max_duty)  # max duty to stop output
        if self.start_time > 0:
            runtime = (time.ticks_ms() - self.start_time) / 1000
            print(f"  Runtime: {runtime:.1f}s")

    def _print_status(self, measurements):
        """Print current status information."""
        voltage = measurements['voltage']
        current = measurements['current']
        power = measurements['power']

        print(f"V:{voltage:.3f}V I:{current:.1f}mA P:{power:.2f}W D:{self.current_duty} T:{self.target_voltage}V/{self.target_current}mA")

    def get_status(self):
        """
        Get current controller status.

        Returns:
            dict: Status information
        """
        measurements = self.read_measurements()

        return {
            'mode': self.current_mode,
            'running': self.is_running,
            'measurements': measurements,
            'targets': {
                'voltage': self.target_voltage,
                'current': self.target_current
            },
            'duty_cycle': self.current_duty,
            'cycle_count': self.cycle_count,
            'runtime': (time.ticks_ms() - self.start_time) / 1000 if self.start_time > 0 else 0
        }
