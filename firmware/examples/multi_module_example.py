# Example: Using Multiple INA3221 Modules
# Demonstrates how to use up to 4 INA3221 modules (12 channels total)

from battery_charger_controller import BatteryChargerController
import asyncio

async def run_controller(controller, mode, name="Controller"):
    """Run a single controller asynchronously."""
    print(f"\n{name}: Starting regulation")
    try:
        await controller.start_regulation(mode)
    except asyncio.CancelledError:
        print(f"{name}: Regulation cancelled")
    except Exception as e:
        print(f"{name}: Error - {e}")


async def main():
    """
    Example: Running multiple controllers with different INA3221 modules.
    
    Hardware Setup:
    - INA3221 Module 1 at 0x40: Channels 0-2
    - INA3221 Module 2 at 0x41: Channels 3-5
    - INA3221 Module 3 at 0x42: Channels 6-8
    - INA3221 Module 4 at 0x43: Channels 9-11
    
    All modules share the same I2C bus (SCL=GP21, SDA=GP20)
    """
    
    print("=" * 60)
    print("Multi-Module INA3221 Battery Charger System")
    print("=" * 60)
    
    # Example 1: Using channels from different modules
    
    # Battery 1: Module at 0x40, Channel 0
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, 
        ina_address=0x40,  # First module
        ina_channel=0,     # First channel
        pca_scl_pin=19, pca_sda_pin=18, 
        pca_channel=0, 
        pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    # Battery 2: Module at 0x40, Channel 1
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20,
        ina_address=0x40,  # Same module
        ina_channel=1,     # Second channel
        pca_scl_pin=19, pca_sda_pin=18,
        pca_channel=1,
        pca_freq=1526,
        target_voltage=7.4,
        target_current=500,
        duty_step=2,
        update_interval=0.001
    )
    
    # Battery 3: Module at 0x40, Channel 2
    controller3 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20,
        ina_address=0x40,  # Same module
        ina_channel=2,     # Third channel
        pca_scl_pin=19, pca_sda_pin=18,
        pca_channel=2,
        pca_freq=1526,
        target_voltage=12.0,
        target_current=1000,
        duty_step=2,
        update_interval=0.001
    )
    
    # Battery 4: Module at 0x41, Channel 0
    controller4 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20,
        ina_address=0x41,  # Second module
        ina_channel=0,     # First channel of second module
        pca_scl_pin=19, pca_sda_pin=18,
        pca_channel=3,
        pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    # More controllers can be added using addresses 0x42 and 0x43...
    
    print("\nStarting all controllers...")
    print("Press Ctrl+C to stop all controllers\n")
    
    # Create tasks for all controllers
    tasks = [
        asyncio.create_task(run_controller(controller1, controller1.MODE_CC_CV, "Battery-1 (0x40:0)")),
        asyncio.create_task(run_controller(controller2, controller2.MODE_CC_CV, "Battery-2 (0x40:1)")),
        asyncio.create_task(run_controller(controller3, controller3.MODE_CC_CV, "Battery-3 (0x40:2)")),
        asyncio.create_task(run_controller(controller4, controller4.MODE_CC_CV, "Battery-4 (0x41:0)")),
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n\nStopping all controllers...")
        for task in tasks:
            task.cancel()
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
