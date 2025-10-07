# Hardware

This directory contains hardware design files for the Smart Cell Analyzer.

## Directory Structure

```
hardware/
└── schematics/              # KiCad schematic and PCB files
    ├── SmartCellAnalyzer.kicad_pro
    ├── SmartCellAnalyzer.kicad_sch
    ├── SmartCellAnalyzer.kicad_pcb
    └── SmartCellAnalyzer-backups/
```

## Components

### Main Components:
- **Microcontroller**: Raspberry Pi Pico / Pico 2 W (RP2040/RP2350)
- **Current/Voltage Sensor**: INA3221 (3-channel)
- **PWM Controller**: PCA9685 (16-channel)
- **Buck Converter**: XL4015 (per channel)

### Connections:
- INA3221 → I2C0 (GP20/GP21)
- PCA9685 → I2C1 (GP18/GP19)

## Design Files

Open the schematic files with [KiCad](https://www.kicad.org/) version 6.0 or later.

## Bill of Materials (BOM)

See the schematic for component values and part numbers.

## Assembly Notes

1. Program the Pico before final assembly
2. Test each channel independently
3. Calibrate current sensing with known loads
4. Set appropriate PWM frequency for buck converters

## Safety

⚠️ **Warning**: This device handles battery charging which can be dangerous if not properly implemented. Always:
- Use appropriate fuses
- Implement temperature monitoring
- Never leave unattended during initial testing
- Follow battery manufacturer's charging specifications
