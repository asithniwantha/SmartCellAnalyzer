# Project Structure

```
SmartCellAnalyzer/
│
├── 📄 README.md                      # Project overview and introduction
├── 📄 LICENSE                        # MIT License
├── 📄 ARCHITECTURE.md                # Architecture guidelines and roadmap
├── 📄 DEPLOYMENT.md                  # Deployment instructions
├── 📄 .gitignore                     # Git ignore rules
│
├── 📁 docs/                          # Project-level documentation
│   └── 🖼️ Logo Smart cell analyzer.png
│
├── 📁 firmware/                      # All firmware code
│   ├── 📄 README.md                  # Firmware overview
│   ├── 📄 main.py                    # Main entry point
│   ├── 📄 boot.py                    # Boot configuration
│   │
│   ├── 📁 src/                       # Source code (production)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py              # ⭐ Central configuration
│   │   │
│   │   ├── 📁 controllers/           # Control logic
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 battery_charger_controller.py
│   │   │
│   │   ├── 📁 drivers/               # Hardware drivers
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 ina3221_wrapper.py
│   │   │   ├── 📄 adafruit_ina3221.py
│   │   │   └── 📄 pca9685.py
│   │   │
│   │   └── 📁 utils/                 # Utilities (future)
│   │       └── 📄 __init__.py
│   │
│   ├── 📁 examples/                  # Example code
│   │   ├── 📄 README.md
│   │   ├── 📄 charger_example.py
│   │   └── 📄 multi_controller_example.py
│   │
│   ├── 📁 tests/                     # Test suite
│   │   ├── 📄 README.md
│   │   └── 📄 test_asyncio.py
│   │
│   └── 📁 docs/                      # Firmware documentation
│       ├── 📄 QUICK_START.md
│       ├── 📄 README_ASYNCIO.md
│       └── 📄 BEFORE_AFTER.md
│
└── 📁 hardware/                      # Hardware design files
    ├── 📄 README.md
    └── 📁 schematics/                # KiCad files
        ├── 📄 SmartCellAnalyzer.kicad_pro
        ├── 📄 SmartCellAnalyzer.kicad_sch
        ├── 📄 SmartCellAnalyzer.kicad_pcb
        ├── 📄 SmartCellAnalyzer.net
        ├── 📄 a.pdf
        └── 📄 b.pdf
```

## Key Improvements

### ✅ Modular Structure
- **src/**: Production code organized by function
- **examples/**: Separate from production code
- **tests/**: Dedicated testing directory
- **docs/**: Documentation at appropriate levels

### ✅ Clear Separation of Concerns
- **controllers/**: Business logic
- **drivers/**: Hardware abstraction
- **utils/**: Helper functions
- **config.py**: Centralized configuration

### ✅ Better Documentation
- README in every major directory
- Architecture and deployment guides
- Quick start and reference docs

### ✅ Professional Organization
- Hardware files separate from firmware
- Examples separate from production code
- Clean import structure with __init__.py files
- Proper .gitignore coverage

## Import Structure

```python
# New import style
from src.controllers.battery_charger_controller import BatteryChargerController
from src.drivers import INA3221Sensor, PCA9685
from src.config import *

# Or using package imports
from src.controllers import BatteryChargerController
from src.drivers import INA3221Sensor
```

## Configuration Management

All configuration is now centralized in `src/config.py`:

```python
# Hardware pins
INA3221_SCL_PIN = 21
PCA9685_SCL_PIN = 19

# Safety limits
MAX_VOLTAGE = 30.0
MAX_CURRENT = 5000

# Battery profiles
BATTERY_PROFILES = {
    'li_ion_single': {'voltage': 4.2, 'current': 1000},
    # ... more profiles
}
```

## File Count Summary

- **Total files**: 32 (renamed/moved/created)
- **New structure files**: 10+ new files
- **Moved files**: 15+ files relocated
- **Documentation files**: 8+ README/guide files
- **Removed obsolete**: 2 files deleted

## Benefits

1. 📦 **Scalability**: Easy to add new features
2. 🔧 **Maintainability**: Clear code organization
3. 📚 **Documentation**: Comprehensive guides
4. 🧪 **Testability**: Dedicated test structure
5. 🚀 **Deployment**: Clear deployment process
6. 🤝 **Collaboration**: Easy for others to contribute
7. ⚙️ **Configuration**: Centralized settings
8. 🏗️ **Professional**: Industry-standard structure
