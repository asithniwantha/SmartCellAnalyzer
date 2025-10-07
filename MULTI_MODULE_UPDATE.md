# 🎉 Multi-Module INA3221 Support Added!

## What's New

Your Smart Cell Analyzer now supports **up to 4 INA3221 modules** on the same I2C bus, giving you **12 monitoring channels**!

## Hardware Configuration

### INA3221 Address Selection

Configure each module's address using the A0 pin:

| Address | A0 Connection | Usage |
|---------|---------------|-------|
| **0x40** | GND (default) | Module 1 - Channels 0, 1, 2 |
| **0x41** | VS+           | Module 2 - Channels 0, 1, 2 |
| **0x42** | SDA           | Module 3 - Channels 0, 1, 2 |
| **0x43** | SCL           | Module 4 - Channels 0, 1, 2 |

### Wiring

All modules share the same I2C bus:
```
Pico          All INA3221 Modules
GP21 (SCL) ──→ SCL (all modules)
GP20 (SDA) ──→ SDA (all modules)
3V3        ──→ VCC (all modules)
GND        ──→ GND (all modules)

Then configure A0 for each module individually.
```

## Code Changes

### Updated BatteryChargerController

New parameter: `ina_address`

```python
# Before (single module only)
controller = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20, 
    ina_channel=0,  # Channel 0-2 only
    ...
)

# After (multiple modules supported)
controller1 = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20,
    ina_address=0x40,  # ✨ NEW: Specify module address
    ina_channel=0,      # Channel within that module
    ...
)

controller2 = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20,
    ina_address=0x41,  # ✨ Different module
    ina_channel=0,      # Same channel number, different module
    ...
)
```

### Updated INA3221Sensor

Now validates address and shares I2C bus across instances:

```python
# Multiple sensors on same bus
ina1 = INA3221Sensor(address=0x40)  # Module 1
ina2 = INA3221Sensor(address=0x41)  # Module 2
ina3 = INA3221Sensor(address=0x42)  # Module 3
ina4 = INA3221Sensor(address=0x43)  # Module 4
```

## Quick Start Examples

### Example 1: Use 3 Channels from One Module

```python
# All from module at 0x40
battery1 = BatteryChargerController(ina_address=0x40, ina_channel=0, pca_channel=0)
battery2 = BatteryChargerController(ina_address=0x40, ina_channel=1, pca_channel=1)
battery3 = BatteryChargerController(ina_address=0x40, ina_channel=2, pca_channel=2)
```

### Example 2: Use Channels from Different Modules

```python
# Channel 0 from module 0x40
battery1 = BatteryChargerController(ina_address=0x40, ina_channel=0, pca_channel=0)

# Channel 0 from module 0x41 (different module, same channel number)
battery2 = BatteryChargerController(ina_address=0x41, ina_channel=0, pca_channel=1)

# Channel 0 from module 0x42
battery3 = BatteryChargerController(ina_address=0x42, ina_channel=0, pca_channel=2)
```

### Example 3: Maximum Configuration (12 Channels)

```python
# Module 0x40 - Channels 0-2
b1 = BatteryChargerController(ina_address=0x40, ina_channel=0, pca_channel=0)
b2 = BatteryChargerController(ina_address=0x40, ina_channel=1, pca_channel=1)
b3 = BatteryChargerController(ina_address=0x40, ina_channel=2, pca_channel=2)

# Module 0x41 - Channels 3-5
b4 = BatteryChargerController(ina_address=0x41, ina_channel=0, pca_channel=3)
b5 = BatteryChargerController(ina_address=0x41, ina_channel=1, pca_channel=4)
b6 = BatteryChargerController(ina_address=0x41, ina_channel=2, pca_channel=5)

# Module 0x42 - Channels 6-8
b7 = BatteryChargerController(ina_address=0x42, ina_channel=0, pca_channel=6)
b8 = BatteryChargerController(ina_address=0x42, ina_channel=1, pca_channel=7)
b9 = BatteryChargerController(ina_address=0x42, ina_channel=2, pca_channel=8)

# Module 0x43 - Channels 9-11
b10 = BatteryChargerController(ina_address=0x43, ina_channel=0, pca_channel=9)
b11 = BatteryChargerController(ina_address=0x43, ina_channel=1, pca_channel=10)
b12 = BatteryChargerController(ina_address=0x43, ina_channel=2, pca_channel=11)
```

## Testing Individual Modules

Test each module after connecting:

```python
from src.drivers.ina3221_wrapper import INA3221Sensor

# Test module at 0x40
ina = INA3221Sensor(address=0x40)
ina.print_readings()  # Shows all 3 channels

# Test module at 0x41
ina2 = INA3221Sensor(address=0x41)
ina2.print_readings()
```

## New Files

1. **`firmware/docs/MULTI_MODULE_GUIDE.md`**
   - Complete guide with wiring diagrams
   - Configuration examples
   - Troubleshooting tips

2. **`firmware/examples/multi_module_example.py`**
   - Working example with 4+ controllers
   - Shows async operation with multiple modules

## Backward Compatibility

✅ **Fully backward compatible!**

Old code still works (defaults to 0x40):
```python
# This still works - defaults to address 0x40
controller = BatteryChargerController(
    ina_scl_pin=21, 
    ina_sda_pin=20, 
    ina_channel=0
)
```

## System Capacity

- **INA3221 Modules**: 4 max (addresses 0x40-0x43)
- **Monitoring Channels**: 12 total (3 per module)
- **PCA9685 Channels**: 16 (0-15)
- **Practical Limit**: 12 battery chargers simultaneously

## Important Notes

1. ✅ All modules share same I2C bus (SCL/SDA)
2. ✅ Each module needs unique address (via A0 pin)
3. ✅ I2C bus is shared efficiently (class variable)
4. ✅ Addresses are validated on initialization
5. ⚠️ Keep I2C cables short (<30cm) for reliability

## Next Steps

1. **Wire your modules** following the guide
2. **Test one module at a time** using the test examples
3. **Run multi_module_example.py** to see it in action
4. **Configure your own setup** based on your needs

## Documentation

- 📘 **`firmware/docs/MULTI_MODULE_GUIDE.md`** - Complete reference
- 📝 **`firmware/examples/multi_module_example.py`** - Working code
- 🚀 **`firmware/docs/QUICK_START.md`** - Getting started

## Need Help?

See the MULTI_MODULE_GUIDE.md for:
- Detailed wiring diagrams
- Troubleshooting steps
- Configuration examples
- Testing procedures

---

**All changes committed and pushed to GitHub!** 🎊

You can now monitor up to 12 batteries simultaneously! 🔋🔋🔋
