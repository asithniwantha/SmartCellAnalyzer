# Battery Charger Controller - Asyncio Implementation

## Overview

This codebase has been converted to use **asyncio** (uasyncio in MicroPython) to enable **simultaneous regulation of multiple battery charger controllers**. This allows you to charge multiple batteries or manage multiple power regulation tasks concurrently on a single Raspberry Pi Pico.

## Key Changes

### 1. **BatteryChargerController** - Async Support

The main controller class now uses asyncio:

- `start_regulation()` is now an **async method** that must be awaited
- Uses `asyncio.sleep()` instead of `time.sleep()` for non-blocking delays
- Can be cancelled gracefully using task cancellation
- Multiple controllers can run simultaneously without blocking each other

### 2. **main.py** - Multi-Controller Example

The main file demonstrates how to:
- Run multiple controllers concurrently
- Use different channels (INA3221 channels 0, 1, 2 and PCA9685 channels)
- Handle keyboard interrupts and graceful shutdown
- Configure different targets for each battery

### 3. **multi_controller_example.py** - Advanced Examples

Additional file with advanced usage patterns:
- `MultiControllerManager` class for coordinating multiple controllers
- Status monitoring across all controllers
- Dynamic controller management
- Different regulation modes running simultaneously

## Hardware Setup

### For Single Controller
- **INA3221**: I2C0 (SCL=GP21, SDA=GP20), Channel 0
- **PCA9685**: I2C1 (SCL=GP19, SDA=GP18), Channel 0

### For Multiple Controllers (Same Hardware)
You can use different channels on the same INA3221 and PCA9685:

**Controller 1:**
- INA3221 Channel 0
- PCA9685 Channel 0

**Controller 2:**
- INA3221 Channel 1
- PCA9685 Channel 1

**Controller 3:**
- INA3221 Channel 2
- PCA9685 Channel 2

## Usage Examples

### Example 1: Single Controller (Simplest)

```python
from battery_charger_controller import BatteryChargerController
import uasyncio as asyncio

async def main():
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        update_interval=0.001
    )
    
    await controller.start_regulation(controller.MODE_CC_CV)

asyncio.run(main())
```

### Example 2: Two Controllers Simultaneously

```python
from battery_charger_controller import BatteryChargerController
import uasyncio as asyncio

async def main():
    # Battery 1: 8.4V charging
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        update_interval=0.001
    )
    
    # Battery 2: 7.4V charging
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
        target_voltage=7.4,
        target_current=500,
        update_interval=0.001
    )
    
    # Run both controllers concurrently
    await asyncio.gather(
        controller1.start_regulation(controller1.MODE_CC_CV),
        controller2.start_regulation(controller2.MODE_CC_CV)
    )

asyncio.run(main())
```

### Example 3: Using the Manager Class

```python
from multi_controller_example import MultiControllerManager
from battery_charger_controller import BatteryChargerController
import uasyncio as asyncio

async def main():
    manager = MultiControllerManager()
    
    # Add controllers
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4, target_current=700
    )
    manager.add_controller(controller1, controller1.MODE_CC_CV, "Battery-1")
    
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
        target_voltage=7.4, target_current=500
    )
    manager.add_controller(controller2, controller2.MODE_CC_CV, "Battery-2")
    
    # Start monitoring
    monitor_task = asyncio.create_task(manager.monitor_status(interval=5.0))
    
    try:
        await manager.start_all()
    finally:
        monitor_task.cancel()

asyncio.run(main())
```

## Regulation Modes

Each controller supports different regulation modes:

1. **MODE_CC_CV** - Constant Current / Constant Voltage charging
   - Best for battery charging
   - Starts with constant current, transitions to constant voltage

2. **MODE_VOLTAGE_REGULATION** - Voltage regulation only
   - Maintains target voltage
   - Ignores current limits

3. **MODE_CURRENT_LIMITING** - Current limiting only
   - Maintains target current
   - Ignores voltage targets

4. **MODE_CUSTOM** - Custom regulation logic
   - Override `_custom_regulation_step()` for custom behavior

## Key Features

### Non-Blocking Operation
Each controller runs independently without blocking others. The asyncio scheduler switches between controllers automatically.

### Graceful Shutdown
Press Ctrl+C to stop all controllers gracefully. Each controller will:
1. Complete its current regulation cycle
2. Print final statistics
3. Set PWM to safe state (max duty to stop output)

### Safety Features
- Voltage and current limits (configurable)
- Real-time safety checks
- Automatic shutdown on safety violations
- Per-controller safety monitoring

### Real-Time Monitoring
- Individual controller status
- System-wide status monitoring
- Configurable update intervals
- Cycle counting and runtime tracking

## Configuration Parameters

### Essential Parameters
- `ina_channel`: INA3221 channel (0, 1, or 2)
- `pca_channel`: PCA9685 channel (0-15)
- `target_voltage`: Target voltage in volts
- `target_current`: Target current in mA

### Control Parameters
- `duty_step`: PWM adjustment step size (default: 2)
- `voltage_tolerance`: Voltage regulation tolerance (default: 0.05V)
- `current_tolerance`: Current regulation tolerance (default: 50mA)
- `update_interval`: Control loop interval (default: 0.01s)

### Safety Limits
- `max_voltage`: Maximum safe voltage (default: 30V)
- `max_current`: Maximum safe current (default: 5000mA)
- `min_voltage`: Minimum voltage threshold (default: 0.1V)

## Performance Considerations

### Update Intervals
- Faster intervals (0.001s) = more responsive control
- Slower intervals (0.01s) = less CPU usage
- Balance based on your application needs

### Number of Controllers
- Tested with up to 3 controllers (INA3221 has 3 channels)
- Each controller adds processing overhead
- Monitor performance and adjust `update_interval` if needed

### CPU Usage
With 3 controllers at 1ms update interval:
- ~30-40% CPU usage (estimated)
- Still leaves plenty of headroom for other tasks

## Troubleshooting

### Issue: Controllers not responding
**Solution:** Check that each controller uses a different channel number

### Issue: High CPU usage
**Solution:** Increase `update_interval` for one or more controllers

### Issue: Task cancelled errors
**Solution:** These are normal during shutdown - they indicate graceful cancellation

### Issue: I2C errors
**Solution:** Ensure proper wiring and that channels are enabled on INA3221

## Running the Examples

### Basic Example (main.py)
```bash
# Upload main.py to your Pico
# Run in REPL:
import main
```

### Advanced Example (multi_controller_example.py)
```bash
# Upload multi_controller_example.py to your Pico
# Run in REPL:
import multi_controller_example
```

## Migration from Non-Async Code

If you have existing code using the old synchronous version:

**Old code:**
```python
controller.start_regulation(controller.MODE_CC_CV)
```

**New code:**
```python
import uasyncio as asyncio

async def main():
    await controller.start_regulation(controller.MODE_CC_CV)

asyncio.run(main())
```

## Additional Notes

- The `time.sleep()` has been replaced with `asyncio.sleep()` for non-blocking delays
- All controller tasks can be cancelled using `task.cancel()`
- Use `asyncio.gather()` to run multiple controllers
- Status can be queried at any time using `controller.get_status()`

## Future Enhancements

Possible additions:
- Load balancing across controllers
- Power budget management
- Automatic failover
- Remote monitoring via WiFi
- Data logging to SD card

## Credits

Original implementation: AI Assistant, September 2025
Asyncio conversion: October 2025
