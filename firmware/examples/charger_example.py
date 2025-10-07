# Example usage of Battery Charger Controller
# Raspberry Pi Pico 2 W with INA3221 and PCA9685

from battery_charger_controller import BatteryChargerController
import time

def main():
    """Main example demonstrating the battery charger controller."""
    
    print("Battery Charger Controller Example")
    print("=" * 40)
    
    # Create controller instance with default settings
    # You can customize all parameters here
    controller = BatteryChargerController(
        # Hardware pins
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1,
        
        # Control parameters  
        target_voltage=7.2,      # Target 7.2V
        target_current=1000,     # Target 1000mA (1A)
        voltage_tolerance=0.05,  # ±0.05V tolerance
        current_tolerance=50,    # ±50mA tolerance
        duty_step=2,             # Small steps for smooth control
        update_interval=0.01     # 10ms update rate
    )
    
    # Example 1: Basic voltage regulation
    print("\n1. Starting Voltage Regulation at 7.2V")
    controller.set_target_voltage(7.2)
    
    try:
        # Run for a few seconds, then stop
        controller.start_regulation(controller.MODE_VOLTAGE_REGULATION)
        
    except KeyboardInterrupt:
        print("Stopped by user")
    
    print("\n" + "=" * 40)
    
def interactive_demo():
    """Interactive demo allowing user to change parameters."""
    
    controller = BatteryChargerController()
    
    print("Interactive Battery Charger Controller")
    print("Commands:")
    print("  v <voltage>  - Set target voltage (e.g., 'v 12.0')")
    print("  i <current>  - Set target current in mA (e.g., 'i 1500')")
    print("  d <duty>     - Set duty cycle (e.g., 'd 2000')")
    print("  start <mode> - Start regulation (voltage_regulation, current_limiting, cc_cv)")
    print("  stop         - Stop regulation")
    print("  status       - Show current status")
    print("  read         - Take single measurement")
    print("  quit         - Exit")
    print()
    
    while True:
        try:
            cmd = input("charger> ").strip().lower().split()
            
            if not cmd:
                continue
                
            if cmd[0] == 'quit':
                break
                
            elif cmd[0] == 'v' and len(cmd) > 1:
                voltage = float(cmd[1])
                controller.set_target_voltage(voltage)
                
            elif cmd[0] == 'i' and len(cmd) > 1:
                current = float(cmd[1])
                controller.set_target_current(current)
                
            elif cmd[0] == 'd' and len(cmd) > 1:
                duty = int(cmd[1])
                controller.set_duty_cycle(duty)
                
            elif cmd[0] == 'start':
                mode = cmd[1] if len(cmd) > 1 else 'voltage_regulation'
                print(f"Starting {mode} mode (Ctrl+C to stop)")
                controller.start_regulation(mode)
                
            elif cmd[0] == 'stop':
                controller.stop_regulation()
                
            elif cmd[0] == 'status':
                status = controller.get_status()
                print(f"Mode: {status['mode']}")
                print(f"Running: {status['running']}")
                print(f"Voltage: {status['measurements']['voltage']:.3f}V (target: {status['targets']['voltage']}V)")
                print(f"Current: {status['measurements']['current']:.1f}mA (target: {status['targets']['current']}mA)")
                print(f"Power: {status['measurements']['power']:.2f}W")
                print(f"Duty: {status['duty_cycle']}")
                print(f"Cycles: {status['cycle_count']}")
                print(f"Runtime: {status['runtime']:.1f}s")
                
            elif cmd[0] == 'read':
                measurements = controller.read_measurements()
                print(f"Voltage: {measurements['voltage']:.3f}V")
                print(f"Current: {measurements['current']:.1f}mA")
                print(f"Power: {measurements['power']:.2f}W")
                print(f"Duty: {measurements['duty_cycle']}")
                
            else:
                print("Unknown command. Type 'quit' to exit.")
                
        except ValueError as e:
            print(f"Invalid value: {e}")
        except KeyboardInterrupt:
            print("\nRegulation interrupted")
            controller.stop_regulation()
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")

def preset_charging_profiles():
    """Example with different charging profiles."""
    
    controller = BatteryChargerController()
    
    # Charging profiles for different battery types
    profiles = {
        'li_ion_single': {'voltage': 4.2, 'current': 1000},    # Single Li-ion cell
        'li_ion_2s': {'voltage': 8.4, 'current': 2000},       # 2S Li-ion pack
        'lead_acid_6v': {'voltage': 7.2, 'current': 1500},    # 6V lead acid
        'lead_acid_12v': {'voltage': 14.4, 'current': 3000},  # 12V lead acid
        'nimh_6cell': {'voltage': 8.4, 'current': 1000},      # 6-cell NiMH
    }
    
    print("Preset Charging Profiles:")
    for name, profile in profiles.items():
        print(f"  {name}: {profile['voltage']}V @ {profile['current']}mA")
    
    while True:
        profile_name = input("\nSelect profile (or 'quit'): ").strip().lower()
        
        if profile_name == 'quit':
            break
            
        if profile_name in profiles:
            profile = profiles[profile_name]
            controller.set_target_voltage(profile['voltage'])
            controller.set_target_current(profile['current'])
            
            print(f"Selected {profile_name}: {profile['voltage']}V @ {profile['current']}mA")
            print("Starting CC/CV charging (Ctrl+C to stop)")
            
            try:
                controller.start_regulation(controller.MODE_CC_CV)
            except KeyboardInterrupt:
                print("Charging stopped")
                controller.stop_regulation()
        else:
            print("Unknown profile")

if __name__ == "__main__":
    print("Battery Charger Controller Examples")
    print("1. Basic example")
    print("2. Interactive demo") 
    print("3. Preset profiles")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        main()
    elif choice == '2':
        interactive_demo()
    elif choice == '3':
        preset_charging_profiles()
    else:
        print("Invalid choice")