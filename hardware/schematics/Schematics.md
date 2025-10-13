## Smart Cell Analyzer – Wiring & Module Reference

### System Overview
- **Target**: Multi-channel Li-ion/LiFePO₄ battery analysis and charging
- **Controller**: Raspberry Pi Pico / Pico 2 W (RP2040 / RP2350)
- **Measurement**: Up to four INA3221 3-channel current/voltage sensor modules (12 channels total)
- **Control**: PCA9685 16-channel PWM expander driving XL4015 buck converters or MOSFET-based loads
- **Telemetry**: Optional UART/USB serial link to host computer
- **Power Rails**: 5 V supply for buck converters, regulated 3.3 V for logic

### Revision Snapshot (Rev 0.9 — October 2025)
- Migrated the design set to KiCad 9.0 with replicated `ChrgerDischarger.kicad_sch` sheets for each battery lane.
- Added explicit per-lane charge (`ChgrGate`) and discharge (`DisGate`) high-side PMOS stages (IRFP9540N) plus a dedicated `FeedBack` return into the RP2040 ADC block.
- Documented hierarchical ports, recommended pin-out, and PCA9685 channel groupings so firmware and harness updates can stay in lockstep with the schematic.
- Exported an updated manufacturing snapshot (`SmartCellAnalyzer.pdf`) and refreshed this guide to match the new symbol references and net names.

### block diagram
![alt text](<../block diagram.jpg>)

### Rendered Schematic Snapshots
- Top-level overview (Rev 0.9):
	![Top-level schematic overview (Rev 0.9)](<scaMain.jpg>)
- Charger/discharger lane sheet:
	![Charger/Discharger hierarchical sheet](<SCAChrgerDischarger.jpg>)
- Stand-alone discharger concept board:
	![Discharger sheet reference](<SCAdischarger.jpg>)

### Schematic Artifacts
- `SmartCellAnalyzer.kicad_sch` — top-level sheet covering RP2040, dual I²C buses, INA3221 array, PCA9685, and sheet instantiations for each power lane.
- `ChrgerDischarger.kicad_sch` — hierarchical sub-sheet replicated per channel that hosts the XL4015 buck, dual PMOS gating, shunt network, and feedback ladder.
- `discharger.kicad_sch` — companion concept for a stand-alone electronic load (kept for experimentation; not instantiated on Rev 0.9).
- `SmartCellAnalyzer.pdf` — generated reference PDF for quick browsing/printing (rev 0.9, generated Oct 2025).

### Sheet Map & Replicated Ports
| Sheet | Description | External Ports | Notes |
|-------|-------------|----------------|-------|
| `SmartCellAnalyzer.kicad_sch` (Top) | RP2040 controller, dual I²C fabric, power regulation, and sheet connectors | Feeds I²C0/1, PWM fan/LED spares, ADC GPIO26–29, VSYS/3V3 rails | Requires KiCad 9.0+ to render hierarchical sheet array correctly |
| `ChrgerDischarger.kicad_sch` (×3 instances) | Combined charger/discharger leg for each battery lane | `Battery±`, `INA±`, `PWM`, `ChgrGate`, `DisGate`, `FeedBack`, `GND` | Instances appear as “Charger Discharger”, “…1”, “…2” on schematic pages 2 → 6 |
| `discharger.kicad_sch` | Optional constant-current sink with separate MOSFET+shunt | `PWM`, `Sense+/-`, `GND`, `Thermal` | Keep in sync if adding a dedicated discharge board |

### Hierarchical Port Reference (Per Lane)
| Port | Direction (at sheet) | Consumes / Drives | Purpose |
|------|----------------------|--------------------|---------|
| `Battery+` | Passive | Battery positive terminal → XL4015 `OUT+` | Positive pole to DUT; route via appropriately rated connector/fuse |
| `Battery-` | Passive | Battery negative → shunt → ground star | Enforces low-side shunt path; never bypass the shunt trace |
| `INA+` | Passive | INA3221 channel `IN+` | Kelvin sense of battery positive for bus voltage |
| `INA-` | Passive | INA3221 channel `IN-` | Kelvin sense of shunt low reference |
| `PWM` | Input | PCA9685 channel (per lane) | Modulates XL4015 EN/COMP node for CC/CV regulation |
| `ChgrGate` | Input | PCA9685 channel (per lane) | Drives PMOS high-side enabling charge path; idle-high keeps MOSFET off |
| `DisGate` | Input | PCA9685 channel (per lane) | Drives PMOS/NMOS discharge stack; allows electronic load engagement |
| `FeedBack` | Output | RP2040 ADC (GPIO26/27/28 depending on lane) | Reports scaled output voltage for closed-loop firmware sanity |
| `GND` | Passive | Local star ground to main plane | Tie at shunt reference; share with sense return |

### Core Modules & Interfaces
| Module | Function | Interface | Notes |
|--------|----------|-----------|-------|
| Raspberry Pi Pico / Pico 2 W | Main MCU, runs MicroPython firmware | — | Provides I²C0 (INA32xx) & I²C1 (PCA9685) buses |
| INA3221 (×1–4) | 3-channel current/voltage measurement | I²C0 @ 0x40–0x43 | A0 pin selects address per module |
| PCA9685 | 16-channel 12-bit PWM output | I²C1 @ 0x40 (default) | Drives MOSFET gates, buck converter control, and fan/indicator spares |
| XL4015 (per channel) | Buck converter for CC/CV charging | PWM input + power | PWM gate via PCA9685 channel, feedback via INA3221 |
| Shunt Resistors | Current sensing | — | 0.1 Ω (typ) per channel tied to INA3221 inputs |
| Cooling Fan (optional) | Thermal management | PCA9685 PWM | Share 5 V rail, assign spare PWM channel |
| Temperature Sensor (optional) | Pack temperature | ADC or 1-Wire | Connect to Pico GP26–28 or compatible pin |

### MCU Pin Allocation
| Pico Pin | Signal | Connected To | Notes |
|----------|--------|--------------|-------|
| GP21 (I²C0 SCL) | `INA_SCL` | INA3221 SCL (all modules) | 4.7 kΩ pull-up to 3.3 V (fit once) |
| GP20 (I²C0 SDA) | `INA_SDA` | INA3221 SDA (all modules) | Keep trace short (<30 cm wiring) |
| GP19 (I²C1 SDA) | `PCA_SDA` | PCA9685 SDA | 4.7 kΩ pull-up to 3.3 V |
| GP18 (I²C1 SCL) | `PCA_SCL` | PCA9685 SCL | Share pull-up with SDA |
| GP0/GP1 | UART0 | Host serial console (optional) | Use for debug logging |
| GP26–28 | ADC0–2 | Temp sensors / auxiliary analog inputs | Optional expansion |
| VSYS | Main 5 V input | XL4015 VIN, fan, auxiliaries | Feed via fused input |
| 3V3(OUT) | Logic rail | INA3221, PCA9685 | Max 300 mA; budget modules (~30 mA each) |

### INA3221 Address Map
Connect the **A0** pin on each module to set unique I²C addresses:

| Module | A0 Tie | Address |
|--------|--------|---------|
| 1 | GND | 0x40 |
| 2 | VS+ | 0x41 |
| 3 | SDA | 0x42 |
| 4 | SCL | 0x43 |

All modules share SCL/SDA lines and 3.3 V/GND. Ensure shunt resistor sense lines are routed as Kelvin connections to minimise measurement error.

### PCA9685 PWM Channel Allocation (Updated Suggestion)
| PCA Chan | Signal Name | Routed To | Notes |
|----------|-------------|-----------|-------|
| 0 | `PWM_CH0` | `PWM` port, Charger/Discharger lane 0 | Primary CC/CV modulation for channel 0 |
| 1 | `CHG_GATE_CH0` | `ChgrGate`, lane 0 | Pull low to enable charge MOSFET (IRFP9540N); keep high-Z/high to isolate |
| 2 | `DIS_GATE_CH0` | `DisGate`, lane 0 | Enables discharge MOSFET/load when asserted |
| 3 | `PWM_CH1` | `PWM` port, lane 1 | — |
| 4 | `CHG_GATE_CH1` | `ChgrGate`, lane 1 | — |
| 5 | `DIS_GATE_CH1` | `DisGate`, lane 1 | — |
| 6 | `PWM_CH2` | `PWM` port, lane 2 | — |
| 7 | `CHG_GATE_CH2` | `ChgrGate`, lane 2 | — |
| 8 | `DIS_GATE_CH2` | `DisGate`, lane 2 | — |
| 9 | `FAN_PWM` | Cooling fan MOSFET | Optional thermal management |
| 10 | `STATUS_LED` | Indicator strip | Optional |
| 11–15 | Spare | Future expansion | Reserve for lane 3 or auxiliary relays |

> _Tip_: When scaling beyond three lanes, repeat the 3-channel grouping (`PWM`, `CHG_GATE`, `DIS_GATE`) and update both the PCA9685 register map and firmware configuration (`firmware/src/config.py`).

### Battery Channel Wiring
- **Negative Path Discipline**: XL4015 modules measure current using the onboard low-side shunt between `OUT-` and the module ground pin. Route **battery negative directly to `OUT-`**, then into the shunt, and only after the shunt bond to system ground. Any common ground jumper that bypasses this shunt will defeat current limiting and INA3221 readings.
- **Sense Connections**: Run separate Kelvin sense wires from the shunt pads back to the INA3221 `CHx+`/`CHx-` inputs. Avoid sharing high-current traces with measurement leads.
- **Positive Path**: Feed battery positive from the XL4015 `OUT+` terminal. Install an inline fuse close to the converter if the pack is removable.
- **Return Reference**: Treat each channel as a semi-floating leg. Tie grounds together only at the shunt reference point to maintain accurate measurements and allow the XL4015 protection circuitry to operate.
- **Charge/Discharge Gates**: Route the `ChgrGate`/`DisGate` lines with twisted-pair returns to reduce noise injection. Default state should leave both MOSFETs open (logic high) so firmware faults fail-safe.

### Feedback & Telemetry Signals
- **Analog Scaling**: Each lane’s `FeedBack` ladder divides the output voltage into the 0–3.3 V window before returning to the RP2040 ADC header (routed in Rev 0.9 to GPIO26 → lane 0, GPIO27 → lane 1, GPIO28 → lane 2). Update `config.BATTERY_PROFILES` if scaling factors change and rerun the KiCad ERC after any remap.
- **INA3221 Mapping**: Tie `INA+/-` from each lane to successive INA3221 channels. For a fourth lane, populate the second INA3221 device (`addr 0x41`) and repeat the wiring.
- **Address Jumpers**: Set INA3221 `A0` jumpers as per the table below so multiple sensors coexist on I²C0. Validate via the firmware I²C scan routine before powering the buck modules.

### Wiring Checklist
- **Power**: Route 5 V rail through protection (fuse + reverse polarity diode). Provide local bulk capacitance near PCA9685 and buck converters.
- **Ground**: Star ground at the shunt reference node for each channel; from there, connect to the main ground plane. Do not link battery negative directly to common ground upstream of the shunt.
- **I²C**: Twist SDA/SCL with ground for external harnesses. Keep below 30 cm or drop bus speed to 100 kHz.
- **PWM / Gate Lines**: Use shielded or twisted pairs for PCA9685 outputs driving `PWM`, `ChgrGate`, and `DisGate` nets, especially when cables exceed 30 cm.
- **Thermal**: Place temperature sensor close to cell pack. Tie to Pico ADC with 10 k pull-up to 3.3 V for NTC usage.

### Module Interconnect Diagram (Textual)
```
Pico 3V3 ─┬─> INA3221 #1…#4 VCC
		  └─> PCA9685 VCC

Pico GP21 ────────────┐
					   ├─> INA3221 SCL (all)
Pico GP20 ────────────┘

Pico GP18 ────────────┐
					   └─> PCA9685 SCL
Pico GP19 ───────────────> PCA9685 SDA

PCA9685 CHx ─────────────> XL4015 EN (`PWM`), Charge Gate (`ChgrGate`), Discharge Gate (`DisGate`) per channel trio
XL4015 OUT+ ─────────────> Battery +
XL4015 OUT- ──[Shunt]───┐
						├─> Battery -
						└─> INA3221 CHx- (Kelvin sense)
INA3221 CHx+ ───────────> XL4015 OUT+

Charger `FeedBack` ──────> RP2040 GPIO26/27/28 (ADC)
```

### Optional Expansion Modules
- **Relay / Contactor Board**: Use spare PCA9685 channels with MOSFET drivers to switch high-current relays.
- **Display (I²C OLED)**: Share I²C0 (address 0x3C); ensure total bus capacitance remains within spec.
- **Data Logger (SPI Flash / SD)**: Connect to Pico SPI0 (GP2–GP5) with level shifting if required.

### Assembly Notes
1. Populate a single INA3221 module and verify readings before adding more modules.
2. Perform an I²C bus scan in firmware to confirm detected addresses (0x40–0x43, 0x40 for PCA9685).
3. Calibrate each channel by applying a known current and updating `SHUNT_RESISTANCES` in `firmware/src/config.py`.
4. Label wiring harnesses with channel numbers to avoid cross-connecting battery packs.

### Test Points & Debugging
- Provide test pads for 3.3 V, 5 V, I²C0 SDA/SCL, and I²C1 SDA/SCL.
- Add LED indicators on 5 V and 3.3 V rails to confirm power presence.
- Include a momentary reset button wired to RUN pin on Pico for convenience.

### Safety Considerations
- Keep sense wiring short to maintain accuracy and prevent oscillations in CC/CV loops.
- Use appropriately rated connectors (XT30/XT60) for battery channels.
- Integrate temperature limit logic in firmware; cut off PWM on over-temperature or over-current conditions.
- Ensure adequate heatsinking for XL4015 modules when running >3 A per channel.
- Fail-safe defaults: configure PCA9685 outputs so any watchdog reset sets `ChgrGate`/`DisGate` high (MOSFETs off) and `PWM` low, preventing unintended current flow.
