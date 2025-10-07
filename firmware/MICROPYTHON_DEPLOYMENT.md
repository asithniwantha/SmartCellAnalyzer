# MicroPython Deployment Fix

## The Problem

MicroPython on the Pico has simpler import requirements than standard Python. The structured folders work great for development, but need to be flattened for deployment.

## Solution: Two Options

### Option 1: Simple Deployment (Recommended for Now)

Upload files to Pico's root directory in a flat structure:

```
Pico root:
├── main.py
├── boot.py
├── battery_charger_controller.py
├── ina3221_wrapper.py
├── adafruit_ina3221.py
└── pca9685.py
```

**Steps:**
1. Copy these files from `firmware/src/controllers/` and `firmware/src/drivers/` to Pico root
2. Use the original main.py with simple imports:
   ```python
   from battery_charger_controller import BatteryChargerController
   ```

### Option 2: Keep Structure (Advanced)

If you want to keep the folder structure on the Pico:

```
Pico root:
├── main.py
├── boot.py
└── src/
    ├── controllers/
    │   └── battery_charger_controller.py
    └── drivers/
        ├── ina3221_wrapper.py
        ├── adafruit_ina3221.py
        └── pca9685.py
```

**Update main.py:**
```python
import sys
sys.path.insert(0, '/src/controllers')
sys.path.insert(0, '/src/drivers')

from battery_charger_controller import BatteryChargerController
```

The imports in battery_charger_controller.py should remain simple:
```python
from ina3221_wrapper import INA3221Sensor
from pca9685 import PCA9685
```

## Current Fix Applied

I've updated main.py to use:
```python
sys.path.insert(0, '/src/controllers')
sys.path.insert(0, '/src/drivers')
```

This tells MicroPython to look in these directories for imports.

## Testing

After uploading, test in REPL:
```python
import sys
print(sys.path)  # Should show /src/controllers and /src/drivers

import main
```

## Recommendation

For now, use **Option 1** (flat structure) until you're ready for more complex deployment. The folder structure in your repo is still valuable for:
- Development
- Version control  
- Documentation
- Code organization

You can have a deployment script that copies files to the right places.
