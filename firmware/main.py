# Asyncio-based main file for multiple Battery Charger Controllers
# This allows regulating multiple controllers simultaneously

# Import from new structure
import sys
sys.path.insert(0, '/src')
sys.path.insert(0, '/src/controllers')
sys.path.insert(0, '/src/drivers')

from battery_charger_controller import BatteryChargerController
import asyncio
from machine import Pin
import board


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


async def run_controller(controller, mode, name="Controller"):
    """
    Run a single controller asynchronously.
    
    Args:
        controller: BatteryChargerController instance
        mode: Regulation mode to use
        name: Name for logging purposes
    """
    print(f"\n{name}: Starting regulation")
    try:
        await controller.start_regulation(mode)
    except asyncio.CancelledError:
        print(f"{name}: Regulation cancelled")
    except Exception as e:
        print(f"{name}: Error - {e}")


async def main():
    """Main async function to run multiple controllers simultaneously."""
    
    print("=" * 60)
    print("Multi-Controller Battery Charger System")
    print("=" * 60)
    
    # Example 1: Single controller (same as before)
    # Uncomment this section if you want to run just one controller
    """
    controller1 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21)
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        # PCA9685 on I2C1 (GP18/GP19)
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        # Target settings
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001  # 1ms updates
    )
    
    await run_controller(controller1, controller1.MODE_CC_CV, "Controller-1")
    """
    
    # Example 2: Multiple controllers running simultaneously
    # This example shows how to run 2 controllers at the same time
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
    
    # Controller 2: Charging Battery 2 at 7.4V (if you have additional hardware)
    # Uncomment and modify if you have a second set of sensors/actuators
    """
    controller2 = BatteryChargerController(
        # INA3221 on I2C0 (GP20/GP21) - same sensor, different channel
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,  # Using channel 1
        # PCA9685 on I2C1 (GP18/GP19) - same PWM driver, different channel
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,  # Using channel 1
        # Target settings for Battery 2
        target_voltage=7.4,
        target_current=500,
        duty_step=2,
        update_interval=0.001  # 1ms updates
    )
    """
    
    # Controller 3: Voltage regulation only
    # Uncomment if you want to add a third controller
    """
    controller3 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=2,  # Using channel 2
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=2, pca_freq=1526,  # Using channel 2
        target_voltage=12.0,
        target_current=1000,
        duty_step=3,
        update_interval=0.002  # 2ms updates
    )
    """
    
    print("\nStarting all controllers...")
    print("Press Ctrl+C to stop all controllers\n")
    
    # Create tasks for all controllers and LED blinking
    tasks = [
        asyncio.create_task(blink_led(0.05)),  # Blink LED every 200ms
        asyncio.create_task(run_controller(controller1, controller1.MODE_CC_CV, "Battery-1")),
        # Uncomment these as needed:
        # asyncio.create_task(run_controller(controller2, controller2.MODE_CC_CV, "Battery-2")),
        # asyncio.create_task(run_controller(controller3, controller3.MODE_VOLTAGE_REGULATION, "Battery-3")),
    ]
    
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
