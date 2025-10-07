# INA3221 Wrapper Class for Easy Access
# Provides simplified interface to the Adafruit INA3221 library


from machine import I2C, Pin
try:
    # Try importing from same directory (when uploaded to Pico)
    from adafruit_ina3221 import INA3221
except ImportError:
    # Try importing from src.drivers (for development)
    from src.drivers.adafruit_ina3221 import INA3221

class INA3221Sensor:
    """
    A wrapper class for the INA3221 3-channel power monitor that provides
    easy access to voltage and current measurements.
    
    Supports multiple INA3221 modules on the same I2C bus with different addresses.
    Available addresses: 0x40, 0x41, 0x42, 0x43
    
    Usage:
        # Single module
        ina = INA3221Sensor(address=0x40)
        channel = ina.channels[0]  # Using first channel
        bus_voltage = channel.bus_voltage  # Returns voltage in volts
        
        # Multiple modules
        ina1 = INA3221Sensor(address=0x40)  # Channels 0-2
        ina2 = INA3221Sensor(address=0x41)  # Channels 3-5
        ina3 = INA3221Sensor(address=0x42)  # Channels 6-8
        ina4 = INA3221Sensor(address=0x43)  # Channels 9-11
    """
    
    # Class variable to share I2C bus across all instances
    _i2c_bus = None
    _i2c_config = None
    
    def __init__(self, scl_pin=21, sda_pin=20, i2c_freq=400000, address=0x40, 
                 shunt_resistances=[0.1, 0.1, 0.1], enable_channels=[0, 1, 2]):
        """
        Initialize the INA3221 sensor.
        
        Args:
            scl_pin (int): GPIO pin for I2C SCL (default: 21)
            sda_pin (int): GPIO pin for I2C SDA (default: 20)
            i2c_freq (int): I2C frequency in Hz (default: 400000)
            address (int): I2C address of the INA3221 (0x40, 0x41, 0x42, or 0x43)
            shunt_resistances (list): Shunt resistance values in ohms for each channel (default: [0.1, 0.1, 0.1])
            enable_channels (list): List of channels to enable (default: [0, 1, 2])
        
        Note: Multiple INA3221 modules can share the same I2C bus but must have different addresses.
        """
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.i2c_freq = i2c_freq
        self.address = address
        self.shunt_resistances = shunt_resistances
        self.enable_channels = enable_channels
        self.ina = None
        self.channels = []
        self.is_initialized = False
        
        # Initialize the sensor
        self._initialize()
    
    def _initialize(self):
        """Initialize the INA3221 sensor and configure channels."""
        try:
            # Validate address
            valid_addresses = [0x40, 0x41, 0x42, 0x43]
            if self.address not in valid_addresses:
                print(f"Warning: Address {hex(self.address)} is not standard.")
                print(f"Valid addresses: {[hex(a) for a in valid_addresses]}")
            
            # Setup I2C bus (shared across all instances)
            current_config = (self.scl_pin, self.sda_pin, self.i2c_freq)
            
            if INA3221Sensor._i2c_bus is None or INA3221Sensor._i2c_config != current_config:
                # Create new I2C bus
                INA3221Sensor._i2c_bus = I2C(0, scl=Pin(self.scl_pin), sda=Pin(self.sda_pin), freq=self.i2c_freq)
                INA3221Sensor._i2c_config = current_config
                
                # Scan for devices
                print(f"\nScanning I2C bus (SCL=GP{self.scl_pin}, SDA=GP{self.sda_pin})...")
                devices = INA3221Sensor._i2c_bus.scan()
                print("Found devices at addresses:", [hex(addr) for addr in devices])
                
                if not devices:
                    print("No I2C devices found! Check wiring:")
                    print(f"- INA3221 SDA -> GP{self.sda_pin}")
                    print(f"- INA3221 SCL -> GP{self.scl_pin}")
                    print("- INA3221 VCC -> 3V3")
                    print("- INA3221 GND -> GND")
                    return False
            
            # Use the shared I2C bus
            self.i2c = INA3221Sensor._i2c_bus
            
            # Check if the requested address exists
            devices = self.i2c.scan()
            if self.address not in devices:
                print(f"ERROR: INA3221 not found at address {hex(self.address)}")
                print(f"Available addresses: {[hex(addr) for addr in devices]}")
                return False
            
            print(f"\nInitializing INA3221 at address {hex(self.address)}...")
            
            # Initialize INA3221
            self.ina = INA3221(self.i2c, address=self.address, enable=self.enable_channels, probe=False)
            print(f"INA3221 at {hex(self.address)} initialized successfully!")
            
            # Verify device IDs
            try:
                mfg_id = self.ina.manufacturer_id
                die_id = self.ina.die_id
                print(f"Manufacturer ID: 0x{mfg_id:04x} (expected 0x5449)")
                print(f"Die ID: 0x{die_id:04x} (expected 0x3220)")
                
                if mfg_id != 0x5449 or die_id != 0x3220:
                    print("WARNING: Device IDs don't match expected values!")
            except Exception as e:
                print(f"Could not read device IDs: {e}")
            
            # Configure each enabled channel
            for i, channel_num in enumerate(self.enable_channels):
                if channel_num < len(self.shunt_resistances):
                    self.ina.channels[channel_num].shunt_resistance = self.shunt_resistances[channel_num]
                    print(f"Channel {channel_num} shunt resistance set to: {self.shunt_resistances[channel_num]} ohms")
            
            # Configure for robust operation
            try:
                self.ina.bus_voltage_conv_time = 4  # 1ms conversion time
                self.ina.shunt_voltage_conv_time = 4  # 1ms conversion time
                self.ina.averaging_mode = 3  # 64 samples average for noise reduction
                print("Configured for robust operation")
            except Exception as e:
                print(f"Could not configure timing: {e}")
            
            # Set power valid limits (safety feature)
            try:
                self.ina.power_valid_limits = (0.5, 24.0)  # 0.5V to 24V
                print("Set power valid limits to 0.5V - 24V")
            except Exception as e:
                print(f"Could not set power limits: {e}")
            
            # Create easy access to channels
            self.channels = self.ina.channels
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"INA3221 initialization failed at {hex(self.address)}: {e}")
            print("Trying lower I2C frequency...")
            try:
                # Try with lower frequency
                INA3221Sensor._i2c_bus = I2C(0, scl=Pin(self.scl_pin), sda=Pin(self.sda_pin), freq=100000)
                INA3221Sensor._i2c_config = (self.scl_pin, self.sda_pin, 100000)
                self.i2c = INA3221Sensor._i2c_bus
                self.ina = INA3221(self.i2c, address=self.address, enable=self.enable_channels, probe=False)
                
                # Configure channels again
                for i, channel_num in enumerate(self.enable_channels):
                    if channel_num < len(self.shunt_resistances):
                        self.ina.channels[channel_num].shunt_resistance = self.shunt_resistances[channel_num]
                
                self.channels = self.ina.channels
                self.is_initialized = True
                print("Initialized with lower I2C frequency")
                return True
                
            except Exception as e2:
                print(f"Still failed with lower frequency: {e2}")
                self.is_initialized = False
                return False
    
    def read_channel(self, channel_num):
        """
        Read all measurements from a specific channel.
        
        Args:
            channel_num (int): Channel number (0, 1, or 2)
        
        Returns:
            dict: Dictionary containing bus_voltage, shunt_voltage, and current
        """
        if not self.is_initialized:
            print("Sensor not initialized!")
            return {"bus_voltage": float('nan'), "shunt_voltage": float('nan'), "current": float('nan')}
        
        if channel_num < 0 or channel_num >= 3:
            print("Invalid channel number! Must be 0, 1, or 2")
            return {"bus_voltage": float('nan'), "shunt_voltage": float('nan'), "current": float('nan')}
        
        try:
            channel = self.channels[channel_num]
            return {
                "bus_voltage": channel.bus_voltage,      # Volts
                "shunt_voltage": channel.shunt_voltage,  # Millivolts
                "current": channel.current               # Milliamps
            }
        except Exception as e:
            print(f"Error reading channel {channel_num}: {e}")
            return {"bus_voltage": float('nan'), "shunt_voltage": float('nan'), "current": float('nan')}
    
    def read_all_channels(self):
        """
        Read measurements from all enabled channels.
        
        Returns:
            list: List of dictionaries containing measurements for each channel
        """
        results = []
        for i in range(3):
            if i in self.enable_channels:
                results.append(self.read_channel(i))
            else:
                results.append({"bus_voltage": float('nan'), "shunt_voltage": float('nan'), "current": float('nan')})
        return results
    
    def print_readings(self, channel_num=None):
        """
        Print formatted readings for a specific channel or all channels.
        
        Args:
            channel_num (int, optional): Specific channel to print. If None, prints all enabled channels.
        """
        if not self.is_initialized:
            print("Sensor not initialized!")
            return
        
        if channel_num is not None:
            # Print specific channel
            data = self.read_channel(channel_num)
            print(f"\nChannel {channel_num}:")
            print(f"  Bus Voltage:   {data['bus_voltage']:.3f} V")
            print(f"  Shunt Voltage: {data['shunt_voltage']:.3f} mV")
            print(f"  Current:       {data['current']:.3f} mA")
        else:
            # Print all enabled channels
            for i in self.enable_channels:
                data = self.read_channel(i)
                print(f"\nChannel {i}:")
                print(f"  Bus Voltage:   {data['bus_voltage']:.3f} V")
                print(f"  Shunt Voltage: {data['shunt_voltage']:.3f} mV")
                print(f"  Current:       {data['current']:.3f} mA")
    
    def set_shunt_resistance(self, channel_num, resistance):
        """
        Set the shunt resistance for a specific channel.
        
        Args:
            channel_num (int): Channel number (0, 1, or 2)
            resistance (float): Shunt resistance in ohms
        """
        if not self.is_initialized:
            print("Sensor not initialized!")
            return
        
        if channel_num < 0 or channel_num >= 3:
            print("Invalid channel number! Must be 0, 1, or 2")
            return
        
        try:
            self.channels[channel_num].shunt_resistance = resistance
            self.shunt_resistances[channel_num] = resistance
            print(f"Channel {channel_num} shunt resistance set to {resistance} ohms")
        except Exception as e:
            print(f"Error setting shunt resistance: {e}")
    
    def reset(self):
        """Reset the INA3221 device."""
        if self.is_initialized and self.ina:
            try:
                self.ina.reset()
                print("INA3221 reset successfully")
            except Exception as e:
                print(f"Error resetting INA3221: {e}")
    
    def get_device_info(self):
        """
        Get device information.
        
        Returns:
            dict: Dictionary containing device information
        """
        if not self.is_initialized or self.ina is None:
            return {"initialized": False}
        
        try:
            return {
                "initialized": True,
                "manufacturer_id": f"0x{self.ina.manufacturer_id:04x}",
                "die_id": f"0x{self.ina.die_id:04x}",
                "address": f"0x{self.address:02x}",
                "enabled_channels": self.enable_channels,
                "shunt_resistances": self.shunt_resistances
            }
        except Exception as e:
            return {"initialized": True, "error": str(e)}