# Asyncio-based main file for multiple Battery Charger Controllers
# This allows regulating multiple controllers simultaneously


import asyncio
from machine import Pin
import board
from src.controllers.battery_charger_controller import BatteryChargerController
from src.utils.performance_monitor import PerformanceMonitor

# === DEVELOPMENT ONLY: Performance Monitoring ===
# Set to True to enable performance monitoring (shows CPU usage and available time)
# Set to False for production (removes ~5-10% overhead)
ENABLE_PERFORMANCE_MONITOR = True

# Create global performance monitor
perf_monitor = PerformanceMonitor(sample_interval=5.0)  # Update stats every 5 seconds

async def blink_led(interval=0.2):
    """
    Blink the built-in LED asynchronously.
    
    Args:
        interval: Blink interval in seconds (default: 0.2 = 200ms)
    """
    led = Pin("LED", Pin.OUT)  # Built-in LED on Pico
    print("LED blinking started (every 200ms)")
    
    try:
        while True:
            board.led.toggle()
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        board.led.off()  # Turn off LED when cancelled
        print("LED blinking stopped")


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
            # Run with performance monitoring
            while True:
                # Mark start of work
                perf_monitor.mark_busy_start()
                
                # Do one regulation cycle
                await controller._regulation_cycle()
                
                # Mark end of work
                perf_monitor.mark_busy_end()
                
                # Wait before next cycle (idle time)
                await asyncio.sleep(controller.update_interval)
        else:
            # Run normally without monitoring
            await controller.start_regulation(mode)
            
    except asyncio.CancelledError:
        print(f"{name}: Regulation cancelled")
    except Exception as e:
        print(f"{name}: Error - {e}")


async def main():
    """Main async function to run multiple controllers simultaneously."""
    
    print("=" * 60)
    print("Multi-Controller Battery Charger System")
    if ENABLE_PERFORMANCE_MONITOR:
        print("*** PERFORMANCE MONITORING ENABLED (Development Mode) ***")
    print("=" * 60)
    
    # Each controller can use different channels on the same hardware
    # or completely separate hardware instances
    
    # Controller 1: Charging Battery 1 at 8.4V
    controller1 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21)
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,  # Using channel 0
        # PCA9685 on I2C1 (GP18/GP19)
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,  # Using channel 0
        # Target settings for Battery 1
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001  # 1ms updates
    )
    
    
    print("\nStarting all controllers...")
    print("Press Ctrl+C to stop all controllers\n")
    
    # Create tasks for all controllers and LED blinking
    tasks = [
        asyncio.create_task(blink_led(0.05)),  # Blink LED every 50ms
        asyncio.create_task(run_controller(controller1, controller1.MODE_CC_CV, "Battery-1")),
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


def run():
    """Entry point to run the async main function."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleanup complete")


if __name__ == "__main__":
    run()
