# Multi-Module INA3221 Configuration Guide

## Overview

Your Smart Cell Analyzer now supports up to **4 INA3221 modules** on the same I2C bus, giving you access to **12 channels** total!

## Hardware Setup

### INA3221 I2C Addresses

Each INA3221 module can be configured to one of four addresses by connecting the A0 pin:

| Address | A0 Connection | Channels Available |
|---------|---------------|-------------------|
| 0x40    | GND (default) | 0, 1, 2          |
| 0x41    | VS+           | 0, 1, 2          |
| 0x42    | SDA           | 0, 1, 2          |
| 0x43    | SCL           | 0, 1, 2          |

### Wiring Multiple Modules

All modules share the same I2C bus:

```
Pico → All INA3221 Modules:
├── GP21 (SCL) → All SCL pins
├── GP20 (SDA) → All SDA pins
├── 3V3        → All VCC pins
└── GND        → All GND pins

Individual Module Configuration:
├── Module 1: A0 → GND  (Address 0x40)
├── Module 2: A0 → VS+  (Address 0x41)
├── Module 3: A0 → SDA  (Address 0x42)
└── Module 4: A0 → SCL  (Address 0x43)
```

## Usage Examples

### Example 1: Single Module (3 channels)

```python
from battery_charger_controller import BatteryChargerController

# Using first module (0x40), channel 0
controller1 = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20,
    ina_address=0x40,  # Module 1
    ina_channel=0,      # Channel 0
    pca_channel=0,
    target_voltage=8.4,
    target_current=700
)

# Using first module (0x40), channel 1
controller2 = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20,
    ina_address=0x40,  # Same module
    ina_channel=1,      # Channel 1
    pca_channel=1,
    target_voltage=7.4,
    target_current=500
)

# Using first module (0x40), channel 2
controller3 = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20,
    ina_address=0x40,  # Same module
    ina_channel=2,      # Channel 2
    pca_channel=2,
    target_voltage=12.0,
    target_current=1000
)
```

### Example 2: Multiple Modules (12 channels)

```python
# Module 1 (0x40) - Channels 0-2
battery1 = BatteryChargerController(ina_address=0x40, ina_channel=0, pca_channel=0)
battery2 = BatteryChargerController(ina_address=0x40, ina_channel=1, pca_channel=1)
battery3 = BatteryChargerController(ina_address=0x40, ina_channel=2, pca_channel=2)

# Module 2 (0x41) - Channels 3-5
battery4 = BatteryChargerController(ina_address=0x41, ina_channel=0, pca_channel=3)
battery5 = BatteryChargerController(ina_address=0x41, ina_channel=1, pca_channel=4)
battery6 = BatteryChargerController(ina_address=0x41, ina_channel=2, pca_channel=5)

# Module 3 (0x42) - Channels 6-8
battery7 = BatteryChargerController(ina_address=0x42, ina_channel=0, pca_channel=6)
battery8 = BatteryChargerController(ina_address=0x42, ina_channel=1, pca_channel=7)
battery9 = BatteryChargerController(ina_address=0x42, ina_channel=2, pca_channel=8)

# Module 4 (0x43) - Channels 9-11
battery10 = BatteryChargerController(ina_address=0x43, ina_channel=0, pca_channel=9)
battery11 = BatteryChargerController(ina_address=0x43, ina_channel=1, pca_channel=10)
battery12 = BatteryChargerController(ina_address=0x43, ina_channel=2, pca_channel=11)
```

### Example 3: Testing Individual Modules

```python
from src.drivers.ina3221_wrapper import INA3221Sensor

# Test Module 1 at 0x40
ina1 = INA3221Sensor(address=0x40)
ina1.print_readings()

# Test Module 2 at 0x41
ina2 = INA3221Sensor(address=0x41)
ina2.print_readings()

# Test Module 3 at 0x42
ina3 = INA3221Sensor(address=0x42)
ina3.print_readings()

# Test Module 4 at 0x43
ina4 = INA3221Sensor(address=0x43)
ina4.print_readings()
```

## Channel Mapping

Logical view of all 12 channels:

```
Module 0x40:
  Global Channel 0 → Module Channel 0
  Global Channel 1 → Module Channel 1
  Global Channel 2 → Module Channel 2

Module 0x41:
  Global Channel 3 → Module Channel 0
  Global Channel 4 → Module Channel 1
  Global Channel 5 → Module Channel 2

Module 0x42:
  Global Channel 6 → Module Channel 0
  Global Channel 7 → Module Channel 1
  Global Channel 8 → Module Channel 2

Module 0x43:
  Global Channel 9 → Module Channel 0
  Global Channel 10 → Module Channel 1
  Global Channel 11 → Module Channel 2
```

## Configuration in config.py

Update your configuration for multiple modules:

```python
# INA3221 Configuration
INA3221_SCL_PIN = 21
INA3221_SDA_PIN = 20
INA3221_I2C_FREQ = 400000

# Available addresses (configured by A0 pin)
INA3221_ADDRESSES = [0x40, 0x41, 0x42, 0x43]

# Shunt resistances for each module (3 channels per module)
SHUNT_RESISTANCES = {
    0x40: [0.1, 0.1, 0.1],  # Module 1 channels 0-2
    0x41: [0.1, 0.1, 0.1],  # Module 2 channels 3-5
    0x42: [0.1, 0.1, 0.1],  # Module 3 channels 6-8
    0x43: [0.1, 0.1, 0.1],  # Module 4 channels 9-11
}
```

## Important Notes

1. **Shared I2C Bus**: All modules share SCL and SDA lines
2. **Different Addresses**: Each module MUST have a unique address
3. **Pull-up Resistors**: Usually built into modules, but 4.7kΩ recommended for long wires
4. **Power Supply**: Ensure 3.3V supply can handle all modules (typically ~30mA each)
5. **Cable Length**: Keep I2C cables short (<30cm) for reliability at 400kHz

## Troubleshooting

### No devices found on I2C bus
- Check wiring connections
- Verify 3.3V power supply
- Check SCL and SDA not swapped

### Specific address not found
- Check A0 pin connection for that module
- Verify module has power
- Try I2C scan: `ina.i2c.scan()`

### Communication errors
- Reduce I2C frequency to 100kHz
- Add 4.7kΩ pull-up resistors
- Shorten cable lengths
- Check for loose connections

## Testing Procedure

1. **Connect one module at a time**
2. **Run I2C scan to verify address**
3. **Test readings from all 3 channels**
4. **Add next module and repeat**
5. **Test all modules together**

## Maximum Capacity

- **4 INA3221 modules** × **3 channels** = **12 monitoring channels**
- **16 PCA9685 channels** = **16 control channels**
- **Practical limit**: 12 battery chargers simultaneously

## See Also

- `examples/multi_module_example.py` - Complete working example
- `examples/multi_controller_example.py` - Advanced controller management
- `firmware/docs/QUICK_START.md` - Getting started guide
