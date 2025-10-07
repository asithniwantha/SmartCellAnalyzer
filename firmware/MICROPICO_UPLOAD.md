# MicroPico Upload Configuration

This file marks the firmware folder for MicroPico extension.

## How MicroPico Works

When you upload the project using MicroPico:
1. Everything in the `firmware/` folder gets uploaded to Pico
2. The folder structure is preserved on the Pico
3. You get the full `src/` structure on the device

## Upload Instructions

### Using MicroPico Extension:

1. **Connect to Pico:**
   - Press `Ctrl+Shift+P`
   - Select "MicroPico: Connect"

2. **Upload Project:**
   - Press `Ctrl+Shift+P`
   - Select "MicroPico: Upload project to Pico"
   - Wait for upload to complete

3. **Run:**
   - Open `main.py`
   - Press `Ctrl+Shift+P`
   - Select "MicroPico: Run current file"

### What Gets Uploaded:

```
Pico root:
├── main.py
├── boot.py
└── src/
    ├── config.py
    ├── controllers/
    │   └── battery_charger_controller.py
    ├── drivers/
    │   ├── ina3221_wrapper.py
    │   ├── adafruit_ina3221.py
    │   └── pca9685.py
    └── utils/
```

## Path Configuration

The `main.py` file adds these paths:
```python
sys.path.insert(0, 'src/controllers')
sys.path.insert(0, 'src/drivers')
```

This allows simple imports:
```python
from battery_charger_controller import BatteryChargerController
from ina3221_wrapper import INA3221Sensor
```

## No Deploy Folder Needed!

Since MicroPico preserves folder structure, you don't need the `deploy/` folder. The structured approach works directly!

## Benefits

✅ Edit files in organized structure
✅ Upload with one command
✅ Structure preserved on Pico
✅ No manual file copying
✅ Easy updates and changes

## Quick Commands

- **Upload:** `Ctrl+Shift+P` → "Upload project to Pico"
- **Run:** `Ctrl+Shift+P` → "Run current file"
- **REPL:** `Ctrl+Shift+P` → "MicroPico: Open REPL"
- **Reset:** `Ctrl+D` in REPL
