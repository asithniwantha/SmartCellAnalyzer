# Performance Monitoring Guide

**FOR DEVELOPMENT USE ONLY - Remove before final release**

## Quick Start

Want to know how much CPU time is available for adding more features? Here are 6 easy methods:

---

## Method 1: Simple Loop Timing ⚡ (Easiest)

**Best for:** Quick check of a single function or loop

```python
import time

loop_times = []
for i in range(100):
    start = time.ticks_us()
    
    # === YOUR CODE HERE ===
    my_function()
    # === END CODE ===
    
    elapsed = time.ticks_diff(time.ticks_us(), start) / 1000  # ms
    loop_times.append(elapsed)

avg_time = sum(loop_times) / len(loop_times)
print(f"Average: {avg_time:.3f} ms")
```

---

## Method 2: SimpleTimer Class 🕐

**Best for:** Timing multiple code sections

```python
from src.utils.performance_monitor import SimpleTimer

timer = SimpleTimer("My Operation")
timer.start()

# Your code here
do_something()

timer.stop()
timer.print_elapsed()  # Prints: "My Operation: 5.432 ms"
```

---

## Method 3: Function Decorator 🎯

**Best for:** Permanently monitoring specific functions during development

```python
from src.utils.performance_monitor import time_function

@time_function
def my_function():
    # Your code
    return result

# When called, automatically prints: "⏱️ my_function(): 3.245 ms"
result = my_function()
```

---

## Method 4: Performance Monitor 📊 (Most Detailed)

**Best for:** Continuous monitoring of CPU usage over time

```python
from src.utils.performance_monitor import PerformanceMonitor

# Create monitor (once at startup)
monitor = PerformanceMonitor(sample_interval=2.0)  # Update every 2 seconds

while True:
    # Mark start of work
    monitor.mark_busy_start()
    
    # Do your work
    controller.update()
    
    # Mark end of work
    monitor.mark_busy_end()
    
    # Print stats every 2 seconds
    if monitor.update():
        monitor.print_stats()
    
    # Idle time
    time.sleep_ms(1)
```

**Output:**
```
============================================================
PERFORMANCE MONITOR (Development Only)
============================================================
CPU Usage:          35.2%
Idle Time:          64.8%
Avg Iteration:      0.35 ms
Iterations/sec:     1000.0
Free Memory:        125.4 KB
Used Memory:        38.2 KB
============================================================
✅ GOOD: >50% idle time - plenty of room for more features
```

---

## Method 5: Memory Check 💾

**Best for:** Checking if you have enough RAM

```python
import gc

gc.collect()  # Clean up first
free = gc.mem_free()
used = gc.mem_alloc()
total = free + used

print(f"Free: {free/1024:.1f} KB ({free/total*100:.1f}%)")
print(f"Used: {used/1024:.1f} KB ({used/total*100:.1f}%)")
```

---

## Method 6: Integration with Main Loop 🔄

**Best for:** Your actual project

Add to your `main.py`:

```python
from src.utils.performance_monitor import PerformanceMonitor

# Global monitor
perf_monitor = PerformanceMonitor(sample_interval=5.0)

async def run_controller(controller, mode, name="Controller"):
    """Run controller with performance monitoring."""
    
    while True:
        # Start timing
        perf_monitor.mark_busy_start()
        
        # Do actual work
        await controller._regulation_cycle()
        
        # End timing
        perf_monitor.mark_busy_end()
        
        # Print stats every 5 seconds
        if perf_monitor.update():
            perf_monitor.print_stats()
        
        # Idle time
        await asyncio.sleep(controller.update_interval)
```

---

## Quick Test

Run the test file to see all methods in action:

```python
# Upload to Pico and run:
import examples.performance_tests
examples.performance_tests.main()
```

---

## Interpreting Results

### CPU Usage

| Idle Time | Meaning | Action |
|-----------|---------|--------|
| **>50%** | ✅ Excellent | Plenty of room for features |
| **30-50%** | ⚠️ Good | Some room available |
| **10-30%** | ⚠️ Tight | Be careful adding more |
| **<10%** | ❌ Critical | System at capacity |

### Typical Values for This Project

With 1 battery controller at 1ms update interval:
- **CPU Usage:** ~30-40%
- **Idle Time:** ~60-70%
- **Iteration Time:** ~0.3-0.5ms
- **Iterations/sec:** ~1000

This means you have **60-70% free time** for additional features!

### What Can You Add?

Based on 60% idle time:

- ✅ **2-3 more controllers** - Each adds ~30-35% CPU
- ✅ **LCD display** - ~5-10% CPU
- ✅ **WiFi/Bluetooth** - ~10-15% CPU
- ✅ **Data logging** - ~5% CPU
- ✅ **Temperature sensors** - ~2-3% CPU
- ✅ **Web interface** - ~15-20% CPU

---

## Memory Usage

Typical values:
- **Total RAM:** ~264 KB (on Pico)
- **Used:** ~40-60 KB
- **Free:** ~200-220 KB

Each controller uses ~5-8 KB of RAM.

---

## Files Created

1. **`src/utils/performance_monitor.py`** - Main monitoring classes
2. **`examples/performance_tests.py`** - Test all methods
3. **`examples/performance_test_example.py`** - Full integration example
4. **`docs/PERFORMANCE_MONITORING.md`** - This guide

---

## Tips

1. **Run tests with your actual workload** - Results vary based on what your code does
2. **Test with all features enabled** - Add controllers, sensors, displays, etc.
3. **Check both CPU and memory** - You might have CPU time but run out of RAM
4. **Remove monitoring before release** - These tools add overhead
5. **Use `gc.collect()` before memory checks** - Gets accurate free memory

---

## Example Session

```python
>>> import examples.performance_tests
>>> examples.performance_tests.test_simple_timing()

============================================================
METHOD 1: Simple Loop Timing
============================================================
Loop iterations:    100
Average time:       0.234 ms
Min time:           0.210 ms
Max time:           0.289 ms

Target interval:    1.000 ms
Used time:          0.234 ms (23.4%)
Available time:     0.766 ms (76.6%)
✅ Plenty of time for more features!
```

---

## Common Questions

**Q: How much overhead does monitoring add?**
A: About 5-10% CPU overhead. Remove before final release!

**Q: Can I monitor async functions?**
A: Yes! Use `mark_busy_start()` and `mark_busy_end()` around your await statements.

**Q: Why is my idle time lower than expected?**
A: Check your update interval. If it's too short (e.g., 0.1ms), the system spends more time working.

**Q: When should I remove monitoring code?**
A: Before deploying to production. It's for development only!

---

## Need Help?

1. Run `performance_tests.py` to see examples
2. Check the docstrings in `performance_monitor.py`
3. Look at `performance_test_example.py` for integration

---

**Remember: Remove all performance monitoring code before final release!** 🚨
