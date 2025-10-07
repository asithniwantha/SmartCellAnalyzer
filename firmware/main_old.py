#Raspberry Pi Pico 2 W (RP2350)
#MicroPython v1.26.1 on 2025-09-11; Raspberry Pi Pico 2 W with RP2350

#PCA9685 16-Channel 12-Bit PWM Servo Driver + INA3221 Triple 0-26 VDC, ±3.2 Amp Power Monitor

from ina3221_wrapper import INA3221Sensor
from pca9685 import PCA9685
import time
from machine import Pin, I2C

# I2C Bus 0 for INA3221 (using default pins GP20/GP21)
# No need to pass I2C instance - wrapper creates its own on I2C0
ina3221 = INA3221Sensor(scl_pin=21, sda_pin=20)  # I2C0: SCL=GP21, SDA=GP20

# I2C Bus 1 for PCA9685 (using different pins)
i2c_pca = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)  # I2C1: SCL=GP19, SDA=GP18
pca = PCA9685(i2c=i2c_pca, address=0x40)

# Configure PCA9685
pca.freq(1526)  # Set frequency to 1526 Hz

# Voltage control parameters
target_voltage = 7.2  # Target voltage in volts
current_duty = 1000   # Starting duty cycle
min_duty = 0          # Minimum duty cycle
max_duty = 4095       # Maximum duty cycle (12-bit PWM)
duty_step = 2        # Step size for duty cycle adjustment
tolerance = 0.05      # Voltage tolerance (±0.05V)

print(f"Starting voltage regulation at {target_voltage}V")
print("Press Ctrl+C to stop")

try:
    while True:
        # Read voltage from INA3221 channel 0
        channel_data = ina3221.read_channel(0)
        current_voltage = channel_data['bus_voltage']
        current_current = channel_data['current']

        print(f"Voltage: {current_voltage:.3f}V, Duty: {current_duty}, Target: {target_voltage}V, Current: {current_current:.3f}mA")

        # Check if voltage is within tolerance
        if abs(current_voltage - target_voltage) <= tolerance:
            #print(f"Voltage stable at {current_voltage:.3f}V")
            pass
        elif current_voltage > target_voltage:
            # Voltage too high - increase duty cycle 
            if current_duty < max_duty:
                current_duty = min(current_duty + duty_step, max_duty)
                pca.duty(1, current_duty)
                #print(f"Voltage too high, increasing duty to {current_duty}")
            else:
                print("Duty cycle at maximum, cannot increase further")
        else:
            # Voltage too low - decrease duty cycle
            if current_duty > min_duty:
                current_duty = max(current_duty - duty_step, min_duty)
                pca.duty(1, current_duty)
                #print(f"Voltage too low, decreasing duty to {current_duty}")
            else:
                print("Duty cycle at minimum, cannot decrease further")
        
        # Wait before next measurement
        time.sleep_ms(10)

except KeyboardInterrupt:
    print("\nVoltage regulation stopped")
    print(f"Final duty cycle: {current_duty}")
    print(f"Final voltage: {ina3221.read_channel(0)['bus_voltage']:.3f}V")

