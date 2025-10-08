# Project Structure

## Directory Layout

```
SmartCellAnalyzer/
│
├── 📄 README.md                      # Project overview
├── 📄 LICENSE                        # MIT License
├── 📄 ARCHITECTURE.md                # Architecture and development guide
├── 📄 PROJECT_STRUCTURE.md           # This file
├── 📄 .gitignore                     # Git ignore rules
├── 📄 SmartCellAnalyzer.code-workspace  # VS Code workspace
│
├── 📁 docs/                          # Project resources
│   └── 🖼️ Logo Smart cell analyzer.png
│
├── 📁 firmware/                      # Firmware code
│   ├── 📄 README.md                  # Firmware overview
│   ├── 📄 main.py                    # Main entry point
│   ├── 📄 boot.py                    # Boot configuration
│   │
│   ├── 📁 src/                       # Source code
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py              # Central configuration
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
│   │   └── 📁 utils/                 # Utilities
│   │       ├── 📄 __init__.py
│   │       └── 📄 performance_monitor.py
│   │
│   ├── 📁 examples/                  # Example code
│   │   ├── 📄 README.md
│   │   └── 📄 multi_module_example.py
│   │
│   ├── 📁 tests/                     # Test suite
│   │   ├── 📄 README.md
│   │   └── 📄 test_asyncio.py
│   │
│   └── 📁 docs/                      # Documentation
│       ├── 📄 QUICK_START.md
│       ├── 📄 README_ASYNCIO.md
│       └── 📄 MULTI_MODULE_GUIDE.md
│
└── 📁 hardware/                      # Hardware design
    ├── 📄 README.md
    └── 📁 schematics/                # KiCad files
        ├── 📄 SmartCellAnalyzer.kicad_pro
        ├── 📄 SmartCellAnalyzer.kicad_sch
        ├── 📄 SmartCellAnalyzer.kicad_pcb
        ├── 📄 a.pdf
        └── 📄 b.pdf
```

## Key Components

### Firmware (`firmware/`)
The main application code for the RP2040 microcontroller.

- **src/**: Production code organized by function
  - **controllers/**: Battery charging control logic
  - **drivers/**: Hardware abstraction layer
  - **utils/**: Helper functions and utilities
  - **config.py**: Centralized configuration

- **examples/**: Working code examples
- **tests/**: Test suite for validation
- **docs/**: User and technical documentation

### Hardware (`hardware/`)
KiCad schematics and PCB design files.

## Import Structure

```python
# Import from organized structure
from src.controllers import BatteryChargerController
from src.drivers import INA3221Sensor, PCA9685
from src.config import *
```

## Benefits

- 📦 **Modular**: Easy to extend and maintain
- 🔧 **Organized**: Clear separation of concerns
- 📚 **Documented**: Comprehensive guides and examples
- 🧪 **Testable**: Dedicated test structure
- 🚀 **Scalable**: Ready for future features
- 🤝 **Professional**: Industry-standard layout
