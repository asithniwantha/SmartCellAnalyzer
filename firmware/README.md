# Firmware Directory Structure

This directory contains all the firmware code for the Smart Cell Analyzer.

## Directory Structure

```
firmware/
├── src/                      # Source code
│   ├── controllers/         # Battery charger control logic
│   ├── drivers/             # Hardware drivers (INA3221, PCA9685)
│   ├── utils/               # Utility functions
│   └── config.py            # Central configuration file
├── examples/                # Example code and usage demos
├── tests/                   # Test suite
├── docs/                    # Documentation
├── main.py                  # Main entry point
└── boot.py                  # Boot configuration
```

## Quick Start

1. **Upload to your Pico:**
   - Upload the entire `src/` folder to your Pico
   - Upload `main.py` and `boot.py`

2. **Run the program:**
   ```python
   import main
   main.run()
   ```

3. **Configure settings:**
   Edit `src/config.py` to customize hardware pins and parameters

## Important Files

- **main.py**: Main entry point with asyncio support
- **src/config.py**: Central configuration (pins, limits, profiles)
- **src/controllers/battery_charger_controller.py**: Main controller logic
- **src/drivers/**: Hardware abstraction layers
- **examples/**: Working examples to get started
- **docs/**: Comprehensive documentation

## Development

See `examples/` for usage examples and `docs/` for detailed documentation.

For development guidelines, see the main project's `ARCHITECTURE.md`.
