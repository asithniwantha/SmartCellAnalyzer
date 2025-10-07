# Deployment Guide

## Prerequisites

1. **Hardware:**
   - Raspberry Pi Pico / Pico 2 W
   - INA3221 current/voltage sensor
   - PCA9685 PWM controller
   - XL4015 buck converter(s)
   - Appropriate wiring and connections

2. **Software:**
   - MicroPython firmware installed on Pico
   - Thonny IDE or similar tool for file upload
   - VS Code with MicroPico extension (optional)

## Deployment Steps

### 1. Upload Firmware Files

Upload the following structure to your Pico:

```
Pico root:
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── battery_charger_controller.py
│   ├── drivers/
│   │   ├── __init__.py
│   │   ├── ina3221_wrapper.py
│   │   ├── adafruit_ina3221.py
│   │   └── pca9685.py
│   └── utils/
│       └── __init__.py
├── main.py
└── boot.py (optional)
```

### 2. Configuration

Edit `src/config.py` on your Pico to match your hardware setup:

```python
# Check and modify these values:
INA3221_SCL_PIN = 21
INA3221_SDA_PIN = 20
PCA9685_SCL_PIN = 19
PCA9685_SDA_PIN = 18
```

### 3. Test Hardware Connections

Run a simple test to verify hardware:

```python
from src.drivers import INA3221Sensor
sensor = INA3221Sensor()
sensor.print_readings()
```

### 4. Run Main Program

```python
import main
main.run()
```

Or set it to run automatically on boot by adding to `boot.py`:
```python
import main
main.run()
```

## Using Thonny IDE

1. Connect Pico to computer
2. Open Thonny
3. Select MicroPython (Raspberry Pi Pico) interpreter
4. Right-click on project folders → Upload to /
5. Open main.py and run (F5)

## Using VS Code with MicroPico

1. Install MicroPico extension
2. Connect to Pico (Ctrl+Shift+P → MicroPico: Connect)
3. Upload project (Ctrl+Shift+P → MicroPico: Upload Project)
4. Run main.py in REPL

## Troubleshooting

### Import Errors
If you get import errors, check that:
- All files are uploaded to correct locations
- Path structure matches exactly
- Files are not corrupted during upload

### Hardware Not Found
If hardware isn't detected:
- Check I2C wiring (SCL, SDA, VCC, GND)
- Verify I2C addresses (default: 0x40 for both)
- Try lower I2C frequency in config.py
- Run I2C scan: `i2c.scan()`

### Permission Denied
On some systems, you may need to add your user to the dialout group:
```bash
sudo usermod -a -G dialout $USER
```

## Development Deployment

For development, you can work directly on the files:

1. Edit files locally
2. Upload changed files only
3. Reset Pico (Ctrl+D in REPL)
4. Test changes

## Production Deployment

For production use:

1. Test thoroughly in development
2. Set `DEBUG_MODE = False` in config.py
3. Disable verbose output
4. Upload complete, tested firmware
5. Configure boot.py for auto-start
6. Test all safety features

## Backup

Always keep a backup of your working configuration:

```python
# In REPL
import os
import json

# Save current config
with open('config_backup.json', 'w') as f:
    # Export your settings
    pass
```

## Updates

To update firmware:

1. Download new version
2. Backup current config
3. Upload new files
4. Restore config settings
5. Test before production use

## Safety Checklist

Before deploying:
- ✓ Safety limits configured correctly
- ✓ Hardware connections verified
- ✓ Test with known loads
- ✓ Monitor temperature during initial tests
- ✓ Emergency stop procedures in place
- ✓ Documentation up to date

## Support

For issues:
1. Check hardware connections
2. Review logs and error messages
3. Consult documentation in `firmware/docs/`
4. Open an issue on GitHub
