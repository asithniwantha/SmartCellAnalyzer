# Smart Cell Analyzer 🔋

![Smart Cell Analyzer Logo](<docs/Logo Smart cell analyzer.png>)

**Smart Cell Analyzer** is an open‑source hardware + firmware project for testing and monitoring rechargeable batteries.  
It combines **XL4015 buck converters**, **INA3221 current/voltage sensing**, and **PCA9685 PWM control** under the supervision of an **RP2040 microcontroller**.

## Features
- Charge and discharge profiling for NiMH and Li‑ion cells
- Real‑time current, voltage, and capacity logging
- Software‑controlled safety cutoffs (OVP, OCP, OTP, timeout)
- Modular design for multi‑channel expansion
- Data logging for capacity (mAh, Wh) and cycle analysis

# Smart Cell Analyzer 🔋

Smart Cell Analyzer is an open‑source hardware + firmware project for testing and monitoring rechargeable batteries.  
It combines **XL4015 buck converters**, **INA3221 current/voltage sensing**, and **PCA9685 PWM control** under the supervision of an **RP2040 microcontroller**.

## ✨ Features
- Charge and discharge profiling for NiMH and Li‑ion cells
- Real‑time current, voltage, and capacity logging
- Software‑controlled safety cutoffs (OVP, OCP, OTP, timeout)
- Modular design for multi‑channel expansion
- Data logging for capacity (mAh, Wh) and cycle analysis

## 🚀 Goals
- Provide a reliable, low‑cost platform for battery health analysis
- Enable hobbyists and researchers to profile cells with repeatable results
- Support future expansion into multi‑chemistry and multi‑channel testing

## 📂 Repo Structure
- `hardware/` – KiCad schematics and PCB files
- `firmware/` – RP2040 + MicroPython/C firmware
- `docs/` – Documentation, diagrams, and logo
- `logs/` – Example charge/discharge logs

## 📸 Logo
(Place your logo here once uploaded, e.g. `/docs/logo.png`)