# Smart Cell Analyzer 🔋

![Smart Cell Analyzer Logo](<docs/Logo Smart cell analyzer.png>)

**Smart Cell Analyzer** is an open-source hardware + firmware project for testing and monitoring rechargeable batteries.  
It combines **XL4015 buck converters**, **INA3221 current/voltage sensing**, and **PCA9685 PWM control** under the supervision of an **RP2040 microcontroller** running MicroPython.

## ✨ Features
- **Multi-channel charging**: Up to 12 batteries simultaneously (4× INA3221 modules)
- **Async operation**: Non-blocking concurrent control with asyncio
- **Multiple modes**: CC, CV, CC/CV charging and regulation
- **Real-time monitoring**: Current, voltage, and power measurements
- **Safety features**: Configurable OVP, OCP, timeout limits
- **Flexible configuration**: Profile-based battery settings
- **Professional architecture**: Modular, maintainable codebase

## 🚀 Quick Start

1. **Hardware Setup**: Connect INA3221, PCA9685, and XL4015 modules
2. **Upload Firmware**: Use MicroPico or Thonny to upload `firmware/` directory
3. **Configure**: Edit `firmware/src/config.py` for your setup
4. **Run**: Execute `import main` in REPL

See [`firmware/docs/QUICK_START.md`](firmware/docs/QUICK_START.md) for detailed instructions.

## 📂 Project Structure
```
SmartCellAnalyzer/
├── firmware/           # MicroPython firmware
│   ├── src/           # Source code
│   │   ├── controllers/   # Battery control logic
│   │   ├── drivers/       # Hardware drivers
│   │   └── config.py      # Configuration
│   ├── examples/      # Usage examples
│   ├── tests/         # Test suite
│   └── docs/          # Documentation
├── hardware/          # KiCad schematics and PCB
└── docs/             # Project resources
```

## 📚 Documentation

- **[Quick Start Guide](firmware/docs/QUICK_START.md)** - Get up and running
- **[Asyncio Guide](firmware/docs/README_ASYNCIO.md)** - Understanding async operation
- **[Multi-Module Guide](firmware/docs/MULTI_MODULE_GUIDE.md)** - Using multiple INA3221 modules
- **[Architecture](ARCHITECTURE.md)** - System design and development guide
- **[Project Structure](PROJECT_STRUCTURE.md)** - Directory organization

## 🔧 System Capabilities

| Component | Capacity |
|-----------|----------|
| **INA3221 modules** | 4 max (addresses 0x40-0x43) |
| **Monitoring channels** | 12 total (3 per module) |
| **PCA9685 channels** | 16 PWM outputs |
| **Simultaneous batteries** | Up to 12 |
| **Update rate** | Configurable (default 10ms) |

## 🛠️ Hardware Requirements

- Raspberry Pi Pico or Pico W
- INA3221 current/voltage sensor(s)
- PCA9685 PWM controller
- XL4015 buck converter(s)
- Power supply and wiring

See [`hardware/README.md`](hardware/README.md) for detailed schematics.

## 🎯 Goals
- Reliable, low-cost platform for battery health analysis
- Support for multiple battery chemistries (NiMH, Li-ion, etc.)
- Professional-grade code quality and documentation
- Easy to expand and customize

## � License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please check [ARCHITECTURE.md](ARCHITECTURE.md) for development guidelines.