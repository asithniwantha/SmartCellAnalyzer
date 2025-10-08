# Asyncio-based main file for multiple Battery Charger Controllers
# This allows regulating multiple controllers simultaneously


import asyncio
import time
from machine import Pin
import board
from src.controllers.battery_charger_controller import BatteryChargerController
from src.utils.performance_monitor import PerformanceMonitor
import _thread

# === DEVELOPMENT ONLY: Performance Monitoring ===
# Set to True to enable performance monitoring (shows CPU usage and available time)
# Set to False for production (removes ~5-10% overhead)
ENABLE_PERFORMANCE_MONITOR = True

# Create global performance monitor
perf_monitor = PerformanceMonitor(sample_interval=5.0)  # Update stats every 5 seconds

# async def blink_led(interval=0.2):
#     """
#     Blink the built-in LED asynchronously.
    
#     Args:
#         interval: Blink interval in seconds (default: 0.2 = 200ms)
#     """
#     led = Pin("LED", Pin.OUT)  # Built-in LED on Pico
#     print("LED blinking started (every 200ms)")
    
#     try:
#         while True:
#             board.led.toggle()
#             await asyncio.sleep(interval)
#     except asyncio.CancelledError:
#         board.led.off()  # Turn off LED when cancelled
#         print("LED blinking stopped")


async def monitor_performance():
    """
    Monitor and display performance statistics periodically.
    FOR DEVELOPMENT ONLY - Shows CPU usage and available processing time.
    """
    if not ENABLE_PERFORMANCE_MONITOR:
        return
    
    print("Performance monitoring started (updates every 5 seconds)")
    
    try:
        while True:
            await asyncio.sleep(5.0)
            
            # Update and print statistics
            if perf_monitor.update():
                perf_monitor.print_stats()
    
    except asyncio.CancelledError:
        print("Performance monitoring stopped")


async def run_controller(controller, mode, name="Controller"):
    """
    Run a single controller asynchronously with performance monitoring.
    
    Args:
        controller: BatteryChargerController instance
        mode: Regulation mode to use
        name: Name for logging purposes
    """
    print(f"\n{name}: Starting regulation")
    
    try:
        if ENABLE_PERFORMANCE_MONITOR:
            # Run with performance monitoring in hybrid mode
            controller.current_mode = mode
            controller.is_running = True
            controller.cycle_count = 0
            controller.start_time = time.ticks_ms()
            controller.last_sensor_read = 0
            controller.cached_measurements = None
            
            print("="*40)
            print(f"Starting {mode} mode")
            if controller.hybrid_mode:
                print(f"HYBRID MODE: Sensor={controller.sensor_read_interval*1000:.1f}ms, PWM={controller.pwm_update_interval*1000:.1f}ms")
            print(f"Target: V={controller.target_voltage}V, I={controller.target_current}mA")
            print("Press Ctrl+C to stop")
            
            while controller.is_running:
                current_time = time.ticks_ms()
                
                # Mark start of work
                perf_monitor.mark_busy_start()
                
                # Hybrid mode: Read sensor only when interval elapsed
                if controller.hybrid_mode:
                    if controller.cached_measurements is None or \
                       time.ticks_diff(current_time, controller.last_sensor_read) >= controller.sensor_read_interval * 1000:
                        controller.cached_measurements = controller.read_measurements()
                        controller.last_sensor_read = current_time
                        
                        # Safety check only when we have fresh data
                        if not controller._safety_check(controller.cached_measurements):
                            print("Safety check failed - stopping regulation")
                            break
                    
                    measurements = controller.cached_measurements
                    update_interval = controller.pwm_update_interval
                else:
                    # Standard mode: Read sensor every cycle
                    measurements = controller.read_measurements()
                    
                    # Safety check
                    if not controller._safety_check(measurements):
                        print("Safety check failed - stopping regulation")
                        break
                    
                    update_interval = controller.update_interval
                
                # Execute control step based on mode
                if mode == controller.MODE_VOLTAGE_REGULATION:
                    controller._voltage_regulation_step(measurements)
                elif mode == controller.MODE_CURRENT_LIMITING:
                    controller._current_regulation_step(measurements)
                elif mode == controller.MODE_CC_CV:
                    controller._cc_cv_step(measurements)
                
                # Update statistics
                controller.cycle_count += 1
                if controller.cycle_count % 2000 == 0:  # Print every 2000 cycles
                    controller._print_status(measurements)
                
                # Mark end of work
                perf_monitor.mark_busy_end()
                
                # Wait before next cycle (idle time)
                await asyncio.sleep(update_interval)
        else:
            # Run normally without monitoring (uses built-in hybrid mode)
            await controller.start_regulation(mode)
            
    except asyncio.CancelledError:
        print(f"{name}: Regulation cancelled")
    except Exception as e:
        print(f"{name}: Error - {e}")
    finally:
        controller.stop_regulation()


async def main():
    """Main async function to run multiple controllers simultaneously."""
    
    print("=" * 60)
    print("Multi-Controller Battery Charger System")
    if ENABLE_PERFORMANCE_MONITOR:
        print("*** PERFORMANCE MONITORING ENABLED (Development Mode) ***")
    print("=" * 60)
    
    # Each controller can use different channels on the same hardware
    # or completely separate hardware instances
    
    # Controller 1: Charging Battery 1 at 8.4V (HYBRID MODE)
    controller1 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21)
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0, ina_address=0x41,  # Using channel 0
        # PCA9685 on I2C1 (GP18/GP19)
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,  # Using channel 0
        # Target settings for Battery 1
        target_voltage=8.4,
        target_current=700,
        duty_step=4,
        # HYBRID MODE: Fast PWM updates with slower sensor reads
        sensor_read_interval=0.010,  # Read sensor every 10ms (100 Hz)
        pwm_update_interval=0.001    # Update PWM every 1ms (1000 Hz) - 10x faster!
    )
    
    controller2 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21)
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1, ina_address=0x41, # Using channel 1
        # PCA9685 on I2C1 (GP18/GP19)
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,  # Using channel 1
        # Target settings for Battery 2
        target_voltage=8.4,
        target_current=700,
        duty_step=4,
        # HYBRID MODE: Fast PWM updates with slower sensor reads
        sensor_read_interval=0.010,  # Read sensor every 10ms (100 Hz)
        pwm_update_interval=0.001    # Update PWM every 1ms (1000 Hz) - 10x faster!
    )
    
    controller3 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21)
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=2, ina_address=0x41, # Using channel 2
        # PCA9685 on I2C1 (GP18/GP19)
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=2, pca_freq=1526,  # Using channel 2
        # Target settings for Battery 3
        target_voltage=8.4,
        target_current=700,
        duty_step=4,
        # HYBRID MODE: Fast PWM updates with slower sensor reads
        sensor_read_interval=0.010,  # Read sensor every 10ms (100 Hz)
        pwm_update_interval=0.001    # Update PWM every 1ms (1000 Hz) - 10x faster!
    )
    
    print("\nStarting all controllers...")
    print("Press Ctrl+C to stop all controllers\n")
    
    # Create tasks for all controllers and LED blinking
    tasks = [
        # asyncio.create_task(blink_led(0.05)),  # Blink LED every 50ms
        asyncio.create_task(run_controller(controller1, controller1.MODE_CC_CV, "Battery-1")),
        asyncio.create_task(run_controller(controller2, controller2.MODE_CC_CV, "Battery-2")),
        asyncio.create_task(run_controller(controller3, controller3.MODE_CC_CV, "Battery-3")),
        # Uncomment these as needed:
        # asyncio.create_task(run_controller(controller2, controller2.MODE_CC_CV, "Battery-2")),
        # asyncio.create_task(run_controller(controller3, controller3.MODE_VOLTAGE_REGULATION, "Battery-3")),
    ]
    
    # Add performance monitoring task if enabled
    if ENABLE_PERFORMANCE_MONITOR:
        tasks.append(asyncio.create_task(monitor_performance()))
    
    try:
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n\nStopping all controllers...")
        # Cancel all tasks
        for task in tasks:
            task.cancel()
        # Wait for all tasks to finish cancelling
        await asyncio.gather(*tasks, return_exceptions=True)
        print("All controllers stopped")

def core1_blink(interval=0.05):
    """
    Runs on RP2040 core1: simple periodic LED toggle.
    Keep this thread free of I2C/SPI unless you add bus locks.
    """
    led = Pin("LED", Pin.OUT)
    while True:
        board.led.toggle()
        time.sleep(interval)

def run():
    """Entry point to run the async main function."""
    try:
        _thread.start_new_thread(core1_blink, (0.05,))
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleanup complete")


if __name__ == "__main__":
    run()
