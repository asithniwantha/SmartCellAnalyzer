# 🎯 Hybrid Mode - Testing Checklist

## Pre-Testing Setup

### Hardware Check
- [ ] Pico connected via USB
- [ ] INA3221 connected to I2C0 (GP20 SDA, GP21 SCL)
- [ ] PCA9685 connected to I2C1 (GP18 SDA, GP19 SCL)
- [ ] XL4015 buck converter connected
- [ ] Power supply ready (12-15V input)
- [ ] Test battery ready (Li-ion 2S: 6.5-8.4V)
- [ ] Multimeter available for verification

### Software Check
- [ ] VS Code with MicroPico extension installed
- [ ] All firmware files saved locally
- [ ] Git repository up to date
- [ ] Backup of working code made (just in case!)

---

## Phase 1: Upload Code (5 minutes)

### Step 1: Upload to Pico
- [ ] Open VS Code
- [ ] Navigate to firmware folder
- [ ] Right-click on `firmware/` → "Upload project to Pico"
- [ ] Wait for upload to complete (~30 seconds)
- [ ] Check for "Upload successful" message

### Step 2: Connect to REPL
- [ ] Press `Ctrl+Shift+P`
- [ ] Type "MicroPico: Connect"
- [ ] Select your Pico's COM port
- [ ] See `>>>` prompt

### Step 3: Run the Code
```python
>>> import main
>>> main.run()
```

**Expected Output:**
```
============================================================
Multi-Controller Battery Charger System
*** PERFORMANCE MONITORING ENABLED (Development Mode) ***
============================================================
```

**✅ CHECKPOINT:** Did you see the startup banner?
- Yes → Continue to Step 4
- No → Check USB connection, try soft reset: `import machine; machine.soft_reset()`

---

## Phase 2: Verify Hybrid Mode (2 minutes)

### Step 4: Look for Hybrid Mode Message

**Expected Output:**
```
========================================
Starting cc_cv mode
HYBRID MODE: Sensor=10.0ms, PWM=1.0ms  ← LOOK FOR THIS LINE!
Target: V=8.4V, I=700mA
Press Ctrl+C to stop
```

**✅ CHECKPOINT:** Do you see "HYBRID MODE: Sensor=10.0ms, PWM=1.0ms"?
- ✅ Yes → SUCCESS! Hybrid mode is active
- ❌ No → Check main.py configuration (see troubleshooting)

### Step 5: Verify All 3 Controllers Start

**Expected Output:**
```
Battery-1: Starting regulation
========================================
Starting cc_cv mode
HYBRID MODE: Sensor=10.0ms, PWM=1.0ms
Target: V=8.4V, I=700mA

Battery-2: Starting regulation
========================================
Starting cc_cv mode
HYBRID MODE: Sensor=10.0ms, PWM=1.0ms
Target: V=8.4V, I=700mA

Battery-3: Starting regulation
========================================
Starting cc_cv mode
HYBRID MODE: Sensor=10.0ms, PWM=1.0ms
Target: V=8.4V, I=700mA

LED blinking started (every 50ms)
Performance monitoring started (updates every 5 seconds)
```

**✅ CHECKPOINT:** Did all 3 controllers start with hybrid mode?
- Yes → Continue to Phase 3
- No → Check error messages, verify I2C devices

---

## Phase 3: CPU Performance Check (10 seconds)

### Step 6: Wait for Performance Stats

After 5 seconds, you should see:

**Expected Output:**
```
=== Performance Statistics ===
Measurement interval: 5.00s
Busy time: 1.02s (20.4%)
Idle time: 3.98s (79.6%)
Available process time: 79.6%
Cycles processed: ~5000
Average cycle time: 1.0ms
```

**✅ CHECKPOINT:** What's your CPU usage?
- 15-20% → ✅ **EXCELLENT!** (Expected range)
- 20-25% → ✅ Good (acceptable)
- 25-35% → ⚠️ Higher than expected (check for background tasks)
- >35% → ❌ Too high (something wrong, see troubleshooting)

### Performance Target Reference

| Metric | Target | Your Result | Status |
|--------|--------|-------------|--------|
| CPU Usage | 15-20% | _____ % | [ ] |
| Available Time | 80-85% | _____ % | [ ] |
| Cycle Time | 1.0ms | _____ ms | [ ] |

---

## Phase 4: Voltage Regulation Test (30 seconds)

### Step 7: Connect Battery and Monitor

**Setup:**
- [ ] Connect test battery (2S Li-ion, 6.5-8.4V)
- [ ] Multimeter on battery terminals
- [ ] Watch REPL output

**Expected Behavior:**
```
[CC-CV] V=6.52V (Target: 8.40V) I=698mA (700mA) Mode:CC Duty:1024/4095 ↑
[CC-CV] V=7.85V (Target: 8.40V) I=702mA (700mA) Mode:CC Duty:2048/4095 ↑
[CC-CV] V=8.25V (Target: 8.40V) I=695mA (700mA) Mode:CC Duty:2560/4095 ↑
[CC-CV] V=8.39V (Target: 8.40V) I=688mA (700mA) Mode:CC Duty:2720/4095 ↑
[CC-CV] V=8.41V (Target: 8.40V) I=645mA (700mA) Mode:CV Duty:2724/4095 ↑
[CC-CV] V=8.40V (Target: 8.40V) I=625mA (700mA) Mode:CV Duty:2724/4095 →
```

**✅ CHECKPOINT:** Response Time Test
- [ ] Started from voltage: _____ V
- [ ] Time to reach 8.4V: _____ ms (expected: <100ms)
- [ ] Final voltage accuracy: _____ V (expected: ±0.05V)
- [ ] CC to CV transition smooth? (yes/no)
- [ ] Voltage stable after reaching target? (yes/no)

### Response Time Targets

| Battery Start | Expected Time | Your Result | Status |
|---------------|--------------|-------------|--------|
| 6.5V → 8.4V | 80-100ms | _____ ms | [ ] |
| 7.0V → 8.4V | 50-70ms | _____ ms | [ ] |
| 7.5V → 8.4V | 30-50ms | _____ ms | [ ] |
| 8.0V → 8.4V | 15-30ms | _____ ms | [ ] |

---

## Phase 5: Stability Test (5 minutes)

### Step 8: Monitor for Oscillations

**Watch for:**
- [ ] Voltage stays within ±0.05V of 8.4V
- [ ] No rapid duty cycle changes (±10 counts)
- [ ] Current drops smoothly in CV mode
- [ ] No safety shutdowns

**Expected Behavior (after reaching target):**
```
[CC-CV] V=8.40V (Target: 8.40V) I=625mA (700mA) Mode:CV Duty:2724/4095 →
[CC-CV] V=8.40V (Target: 8.40V) I=618mA (700mA) Mode:CV Duty:2724/4095 →
[CC-CV] V=8.41V (Target: 8.40V) I=612mA (700mA) Mode:CV Duty:2720/4095 ↓
[CC-CV] V=8.40V (Target: 8.40V) I=605mA (700mA) Mode:CV Duty:2720/4095 →
```

**✅ CHECKPOINT:** Stability Metrics (measure for 5 minutes)

| Metric | Target | Your Result | Status |
|--------|--------|-------------|--------|
| Voltage variation | <±0.05V | ±_____ V | [ ] |
| Duty cycle jitter | <±10 counts | ±_____ counts | [ ] |
| Oscillations seen? | None | Yes/No | [ ] |
| Safety shutdowns? | None | Yes/No | [ ] |

---

## Phase 6: Memory Stability (Optional, 10 minutes)

### Step 9: Monitor Free Memory

**In a separate REPL session or after stopping:**
```python
>>> import gc
>>> for i in range(120):  # 10 minutes
...     time.sleep(5)
...     gc.collect()
...     print(f"{i*5}s: {gc.mem_free()} bytes free")
```

**Expected Output:**
```
0s: 10752 bytes free
5s: 10688 bytes free
10s: 10720 bytes free
... (should remain stable around 10-11 KB)
```

**✅ CHECKPOINT:** Memory Stability
- [ ] Starting free RAM: _____ KB
- [ ] Ending free RAM (after 10 min): _____ KB
- [ ] Memory leak detected? (yes/no)
- [ ] Variation within ±500 bytes? (yes/no)

---

## Phase 7: Feature Test (Optional)

### Step 10: Test Adaptive Steps

**Test large error response:**
1. [ ] Disconnect battery
2. [ ] Set duty to 0: `controller1.pca9685.set_duty_cycle(0, 0)`
3. [ ] Reconnect battery (starts from 0V output)
4. [ ] Watch for 8× steps (large voltage error)
5. [ ] Time to reach target: _____ ms (should be <100ms)

**Test fine tuning:**
1. [ ] Manually set voltage to 8.3V
2. [ ] Watch for 1× steps (small error, 0.1V)
3. [ ] Time to correct: _____ ms (should be <50ms)

**✅ CHECKPOINT:** Adaptive Steps Working?
- [ ] Large errors (>1V) use 8× steps
- [ ] Medium errors (0.5-1V) use 4× steps
- [ ] Small errors (0.2-0.5V) use 2× steps
- [ ] Fine tuning (<0.2V) uses 1× steps

---

## Final Checklist

### ✅ All Tests Pass?

**Core Functionality:**
- [ ] Hybrid mode activates (sees "HYBRID MODE" message)
- [ ] CPU usage 15-25% (down from 45%)
- [ ] Response time <100ms (was ~300ms)
- [ ] Voltage regulation stable (±0.05V)
- [ ] No oscillations or instability
- [ ] Memory stable (no leaks)

**Performance Targets Met:**
- [ ] 10× faster response time
- [ ] 30% less CPU usage
- [ ] 3× faster PWM updates
- [ ] Adaptive steps working

**If ALL boxes checked:** 🎉 **SUCCESS!** Hybrid mode is working perfectly!

**If ANY boxes unchecked:** See troubleshooting section below

---

## Troubleshooting

### Problem: No "HYBRID MODE" message

**Diagnosis:**
```python
>>> c = controller1  # Or controller2, controller3
>>> print(f"Hybrid: {c.hybrid_mode}")
>>> print(f"Sensor interval: {c.sensor_read_interval}")
>>> print(f"PWM interval: {c.pwm_update_interval}")
```

**Expected:**
```
Hybrid: True
Sensor interval: 0.01
PWM interval: 0.001
```

**If Hybrid is False:**
1. Check `main.py` has both parameters:
   ```python
   sensor_read_interval=0.010,
   pwm_update_interval=0.001
   ```
2. Re-upload code to Pico
3. Soft reset: `import machine; machine.soft_reset()`

### Problem: High CPU Usage (>30%)

**Diagnosis:**
```python
>>> print(f"Perf monitoring: {ENABLE_PERFORMANCE_MONITOR}")
>>> print(f"Controllers running: {controller1.is_running + controller2.is_running + controller3.is_running}")
```

**Solutions:**
1. Disable performance monitoring in `main.py`:
   ```python
   ENABLE_PERFORMANCE_MONITOR = False
   ```
2. Increase sensor interval to 15ms:
   ```python
   sensor_read_interval=0.015
   ```
3. Check for other running tasks

### Problem: Voltage Oscillates

**Diagnosis:**
- Voltage jumps above/below target
- Duty cycle rapidly changes
- Unstable regulation

**Solutions:**
1. Reduce adaptive step multipliers in `battery_charger_controller.py`:
   ```python
   # Change from 8×/4×/2× to 4×/2×/1.5×
   if abs(voltage_error) > 1.0:
       step_multiplier = 4  # Was 8
   ```
2. Increase PWM update interval:
   ```python
   pwm_update_interval=0.002  # 2ms instead of 1ms
   ```

### Problem: ImportError or AttributeError

**Check file structure:**
```python
>>> import os
>>> os.listdir('/firmware/src/controllers')
# Should show: ['battery_charger_controller.py']
```

**Solution:** Re-upload all files, ensure folder structure is correct

### Problem: I2C Devices Not Found

**Check I2C:**
```python
>>> from machine import I2C, Pin
>>> i2c0 = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
>>> i2c0.scan()
[65]  # Should show 0x41 (INA3221)
>>> i2c1 = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
>>> i2c1.scan()
[64]  # Should show 0x40 (PCA9685)
```

**Solutions:**
- Check wiring (SDA/SCL pins)
- Check power to modules
- Check I2C addresses match configuration

---

## Next Steps After Success

### Production Deployment

1. **Disable Performance Monitoring:**
   - Edit `main.py`: `ENABLE_PERFORMANCE_MONITOR = False`
   - Saves 5-10% CPU, frees 10-15 KB RAM
   - Re-upload to Pico

2. **Reduce Print Frequency:**
   - Change status print to every 5000 cycles (was 2000)
   - Saves another 1-2% CPU

3. **Test with Real Batteries:**
   - Different chemistries (Li-ion, Li-Po, Lead-acid)
   - Different capacities (500mAh to 5000mAh)
   - Document any needed adjustments

### Optional Enhancements

4. **Optimize INA3221 Averaging (Optional):**
   - In `ina3221_wrapper.py`, change:
     ```python
     averaging_mode=1  # 4 samples (was 64)
     ```
   - Reduces read time from 2.93ms to 0.85ms
   - Test for acceptable noise levels

5. **Add Display (Now Feasible):**
   - 128×64 OLED display
   - Show voltage/current/power/mode
   - Estimated: 5-10% CPU, 3-5 KB RAM

6. **Add Data Logging (Now Feasible):**
   - Log to SD card or flash
   - Store charging history
   - Estimated: 2-3% CPU, 2-3 KB RAM

### Documentation

7. **Record Your Results:**
   - Fill in performance metrics
   - Document any issues found
   - Share improvements on GitHub

8. **Update README:**
   - Add hybrid mode section
   - Include performance results
   - List any hardware-specific notes

---

## Success Criteria Summary

### Minimum Requirements (Must Pass)
- ✅ Hybrid mode activates
- ✅ CPU usage <30%
- ✅ No crashes or errors
- ✅ Voltage regulation works

### Optimal Performance (Nice to Have)
- ✅ CPU usage 15-20%
- ✅ Response time <100ms
- ✅ No oscillations
- ✅ Memory stable

### Production Ready (All Pass)
- ✅ All minimum requirements
- ✅ All optimal performance targets
- ✅ 5 minute stability test passed
- ✅ Multiple charge cycles tested

**Your Score: _____ / 12 checkboxes**

- 12/12: 🌟 **Perfect!** Production ready!
- 10-11/12: 🎉 **Excellent!** Minor tweaks needed
- 8-9/12: ✅ **Good!** Some optimization needed
- 6-7/12: ⚠️ **Acceptable** Needs more work
- <6/12: ❌ **Issues** Review troubleshooting

---

## Quick Reference Card

### Key Commands

**Start:**
```python
import main
main.run()
```

**Stop:**
```
Ctrl+C (in REPL)
```

**Check Status:**
```python
controller1.is_running  # True/False
gc.mem_free()  # Free RAM in bytes
```

**Soft Reset:**
```python
import machine
machine.soft_reset()
```

### Key Indicators

**Hybrid Mode Active:**
- See "HYBRID MODE: Sensor=10.0ms, PWM=1.0ms"

**Good Performance:**
- CPU: 15-20%
- Cycle: 1.0ms
- Available: 80-85%

**Stable Regulation:**
- Voltage: ±0.05V
- No oscillations
- Smooth CC→CV

### Key Files

- `main.py` - Entry point, controller config
- `battery_charger_controller.py` - Control logic
- `HYBRID_TESTING.md` - Full testing guide
- `HYBRID_MODE.md` - Technical details

---

**Ready? Let's test! 🚀**

*Remember: Take your time, check each step, and don't worry if something doesn't work perfectly the first time. That's what testing is for!*

**Good luck!** 🍀
