# Advanced Multi-Controller Example
# This demonstrates more complex scenarios with multiple battery chargers

from battery_charger_controller import BatteryChargerController
import asyncio


class MultiControllerManager:
    """Manager class for coordinating multiple battery charger controllers."""
    
    def __init__(self):
        self.controllers = []
        self.tasks = []
        self.is_running = False
    
    def add_controller(self, controller, mode, name):
        """
        Add a controller to the manager.
        
        Args:
            controller: BatteryChargerController instance
            mode: Regulation mode
            name: Identifier name
        """
        self.controllers.append({
            'controller': controller,
            'mode': mode,
            'name': name,
            'task': None
        })
        print(f"Added {name} to manager")
    
    async def run_single_controller(self, ctrl_dict):
        """Run a single controller and handle its lifecycle."""
        controller = ctrl_dict['controller']
        mode = ctrl_dict['mode']
        name = ctrl_dict['name']
        
        print(f"[{name}] Starting...")
        try:
            await controller.start_regulation(mode)
        except asyncio.CancelledError:
            print(f"[{name}] Cancelled")
        except Exception as e:
            print(f"[{name}] Error: {e}")
    
    async def start_all(self):
        """Start all controllers concurrently."""
        if self.is_running:
            print("Controllers already running!")
            return
        
        self.is_running = True
        print(f"\nStarting {len(self.controllers)} controllers...")
        
        # Create tasks for all controllers
        for ctrl_dict in self.controllers:
            task = asyncio.create_task(self.run_single_controller(ctrl_dict))
            ctrl_dict['task'] = task
            self.tasks.append(task)
        
        try:
            # Run all tasks concurrently
            await asyncio.gather(*self.tasks)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected")
            await self.stop_all()
    
    async def stop_all(self):
        """Stop all controllers gracefully."""
        if not self.is_running:
            return
        
        print("\nStopping all controllers...")
        
        # Stop each controller
        for ctrl_dict in self.controllers:
            ctrl_dict['controller'].is_running = False
            if ctrl_dict['task']:
                ctrl_dict['task'].cancel()
        
        # Wait for all tasks to finish
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        self.is_running = False
        self.tasks = []
        print("All controllers stopped")
    
    async def monitor_status(self, interval=5.0):
        """
        Periodically print status of all controllers.
        
        Args:
            interval: Status update interval in seconds
        """
        print(f"\nStatus monitor started (updating every {interval}s)")
        
        while self.is_running:
            await asyncio.sleep(interval)
            
            print("\n" + "="*60)
            print("SYSTEM STATUS")
            print("="*60)
            
            for ctrl_dict in self.controllers:
                controller = ctrl_dict['controller']
                name = ctrl_dict['name']
                status = controller.get_status()
                
                print(f"\n{name}:")
                print(f"  Mode: {status['mode']}")
                print(f"  Running: {status['running']}")
                print(f"  Voltage: {status['measurements']['voltage']:.3f}V (target: {status['targets']['voltage']}V)")
                print(f"  Current: {status['measurements']['current']:.1f}mA (target: {status['targets']['current']}mA)")
                print(f"  Power: {status['measurements']['power']:.2f}W")
                print(f"  Duty: {status['duty_cycle']}")
                print(f"  Cycles: {status['cycle_count']}")
                print(f"  Runtime: {status['runtime']:.1f}s")
            
            print("="*60)


# Example 1: Simple multi-controller setup
async def example_simple_multi_controller():
    """Run two controllers on different channels."""
    
    manager = MultiControllerManager()
    
    # Battery 1: 8.4V Li-ion charging
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    manager.add_controller(controller1, controller1.MODE_CC_CV, "Li-ion-8.4V")
    
    # Battery 2: 7.4V Li-ion charging (if you have channel 1 hardware)
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
        target_voltage=7.4,
        target_current=500,
        duty_step=2,
        update_interval=0.001
    )
    manager.add_controller(controller2, controller2.MODE_CC_CV, "Li-ion-7.4V")
    
    # Start monitoring task
    monitor_task = asyncio.create_task(manager.monitor_status(interval=10.0))
    
    # Start all controllers
    try:
        await manager.start_all()
    except KeyboardInterrupt:
        pass
    finally:
        monitor_task.cancel()
        await asyncio.gather(monitor_task, return_exceptions=True)


# Example 2: Different regulation modes for different purposes
async def example_mixed_modes():
    """Run controllers with different regulation modes."""
    
    manager = MultiControllerManager()
    
    # Controller 1: CC/CV charging
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    manager.add_controller(controller1, controller1.MODE_CC_CV, "CC-CV-Charger")
    
    # Controller 2: Voltage regulation only
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
        target_voltage=12.0,
        target_current=1000,
        duty_step=3,
        update_interval=0.002
    )
    manager.add_controller(controller2, controller2.MODE_VOLTAGE_REGULATION, "Voltage-Reg")
    
    # Controller 3: Current limiting only
    controller3 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=2,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=2, pca_freq=1526,
        target_voltage=15.0,
        target_current=800,
        duty_step=2,
        update_interval=0.001
    )
    manager.add_controller(controller3, controller3.MODE_CURRENT_LIMITING, "Current-Limiter")
    
    # Start monitoring
    monitor_task = asyncio.create_task(manager.monitor_status(interval=5.0))
    
    try:
        await manager.start_all()
    except KeyboardInterrupt:
        pass
    finally:
        monitor_task.cancel()
        await asyncio.gather(monitor_task, return_exceptions=True)


# Example 3: Dynamic controller management
async def example_dynamic_control():
    """Demonstrate starting and stopping controllers dynamically."""
    
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("Starting first controller for 10 seconds...")
    task1 = asyncio.create_task(controller1.start_regulation(controller1.MODE_CC_CV))
    
    # Run for 10 seconds
    await asyncio.sleep(10)
    
    print("\nChanging target voltage to 7.4V...")
    controller1.set_target_voltage(7.4)
    
    # Run for another 10 seconds
    await asyncio.sleep(10)
    
    print("\nStopping controller...")
    controller1.is_running = False
    await task1
    
    print("Controller stopped")


# Main function to select and run examples
async def main():
    """Main function to run examples."""
    
    print("=" * 60)
    print("Multi-Controller Battery Charger Examples")
    print("=" * 60)
    print("\nAvailable examples:")
    print("1. Simple multi-controller (2 controllers)")
    print("2. Mixed regulation modes (3 controllers)")
    print("3. Dynamic control demonstration")
    print("\nRunning Example 1 by default...")
    print("Edit this file to try other examples\n")
    
    # Choose which example to run
    # Uncomment the one you want to try:
    
    await example_simple_multi_controller()
    # await example_mixed_modes()
    # await example_dynamic_control()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Program finished")
