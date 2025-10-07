# Example: Using Performance Monitor
# Shows CPU usage and available processing time
# FOR DEVELOPMENT ONLY - Remove before final release

import asyncio
from machine import Pin
import board
from src.controllers.battery_charger_controller import BatteryChargerController
from src.utils.performance_monitor import PerformanceMonitor, time_function


# Global performance monitor
perf_monitor = PerformanceMonitor(sample_interval=2.0)  # Update every 2 seconds


async def blink_led(interval=0.2):
    """Blink the built-in LED asynchronously."""
    led = Pin("LED", Pin.OUT)
    print("LED blinking started")
    
    try:
        while True:
            board.led.toggle()
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        board.led.off()
        print("LED blinking stopped")


async def monitor_performance():
    """Monitor and display performance statistics periodically."""
    print("Performance monitoring started")
    
    try:
        while True:
            await asyncio.sleep(2.0)  # Update every 2 seconds
            
            # Update and print statistics
            if perf_monitor.update():
                perf_monitor.print_stats()
    
    except asyncio.CancelledError:
        print("Performance monitoring stopped")


async def run_controller(controller, mode, name="Controller"):
    """
    Run a single controller with performance monitoring.
    
    Args:
        controller: BatteryChargerController instance
        mode: Regulation mode to use
        name: Name for logging purposes
    """
    print(f"\n{name}: Starting regulation with performance monitoring")
    
    try:
        # Start regulation loop
        while True:
            # Mark start of work
            perf_monitor.mark_busy_start()
            
            # Do the actual work (one regulation cycle)
            await controller._regulation_cycle()
            
            # Mark end of work
            perf_monitor.mark_busy_end()
            
            # Small delay before next cycle (this is idle time)
            await asyncio.sleep(controller.update_interval)
    
    except asyncio.CancelledError:
        print(f"{name}: Regulation cancelled")
    except Exception as e:
        print(f"{name}: Error - {e}")


async def main():
    """Main async function with performance monitoring."""
    
    print("=" * 60)
    print("Multi-Controller System with Performance Monitor")
    print("FOR DEVELOPMENT ONLY")
    print("=" * 60)
    
    # Create controller
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001  # 1ms updates
    )
    
    print("\nStarting all tasks...")
    print("Press Ctrl+C to stop\n")
    
    # Create tasks
    tasks = [
        asyncio.create_task(blink_led(0.2)),
        asyncio.create_task(monitor_performance()),  # Performance monitoring task
        asyncio.create_task(run_controller(controller1, controller1.MODE_CC_CV, "Battery-1")),
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n\nStopping all tasks...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("All tasks stopped")


def run():
    """Entry point."""
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
