"""
Simple Performance Testing Examples
Shows different ways to measure CPU usage and available time
FOR DEVELOPMENT ONLY - Remove before final release
"""

import time
import gc
from src.utils.performance_monitor import PerformanceMonitor, SimpleTimer, time_function


# ==============================================================================
# METHOD 1: Simple Loop Timing
# ==============================================================================
def test_simple_timing():
    """Measure how much time your main loop takes."""
    print("\n" + "=" * 60)
    print("METHOD 1: Simple Loop Timing")
    print("=" * 60)
    
    loop_times = []
    
    for i in range(100):
        start = time.ticks_us()
        
        # === YOUR CODE HERE ===
        # Simulate some work (replace with your actual code)
        x = 0
        for j in range(1000):
            x += j * 2
        # === END YOUR CODE ===
        
        elapsed = time.ticks_diff(time.ticks_us(), start) / 1000  # Convert to ms
        loop_times.append(elapsed)
    
    # Calculate statistics
    avg_time = sum(loop_times) / len(loop_times)
    min_time = min(loop_times)
    max_time = max(loop_times)
    
    print(f"Loop iterations:    100")
    print(f"Average time:       {avg_time:.3f} ms")
    print(f"Min time:           {min_time:.3f} ms")
    print(f"Max time:           {max_time:.3f} ms")
    
    # Calculate how much time is available
    target_interval = 1.0  # 1ms target
    available_time = target_interval - avg_time
    available_percent = (available_time / target_interval) * 100
    
    print(f"\nTarget interval:    {target_interval:.3f} ms")
    print(f"Used time:          {avg_time:.3f} ms ({100 - available_percent:.1f}%)")
    print(f"Available time:     {available_time:.3f} ms ({available_percent:.1f}%)")
    
    if available_percent > 50:
        print("✅ Plenty of time for more features!")
    elif available_percent > 20:
        print("⚠️  Some time available, but be careful")
    else:
        print("❌ Very little time available!")


# ==============================================================================
# METHOD 2: Using SimpleTimer Class
# ==============================================================================
def test_simple_timer():
    """Use SimpleTimer to measure specific code sections."""
    print("\n" + "=" * 60)
    print("METHOD 2: Using SimpleTimer Class")
    print("=" * 60)
    
    # Time different operations
    timer1 = SimpleTimer("Operation 1")
    timer1.start()
    x = sum(range(10000))
    timer1.stop()
    timer1.print_elapsed()
    
    timer2 = SimpleTimer("Operation 2")
    timer2.start()
    y = [i**2 for i in range(1000)]
    timer2.stop()
    timer2.print_elapsed()
    
    total = timer1.elapsed_ms + timer2.elapsed_ms
    print(f"\nTotal time: {total:.3f} ms")


# ==============================================================================
# METHOD 3: Using Function Decorator
# ==============================================================================
@time_function
def my_slow_function():
    """This function will automatically print its execution time."""
    result = 0
    for i in range(50000):
        result += i
    return result


def test_decorator():
    """Use decorator to automatically time functions."""
    print("\n" + "=" * 60)
    print("METHOD 3: Using @time_function Decorator")
    print("=" * 60)
    
    result = my_slow_function()
    print(f"Result: {result}")


# ==============================================================================
# METHOD 4: CPU Usage Over Time
# ==============================================================================
def test_performance_monitor():
    """Monitor CPU usage over time."""
    print("\n" + "=" * 60)
    print("METHOD 4: Performance Monitor (CPU Usage Over Time)")
    print("=" * 60)
    
    monitor = PerformanceMonitor(sample_interval=1.0)
    
    print("Running workload for 5 seconds...\n")
    
    end_time = time.ticks_ms() + 5000  # Run for 5 seconds
    
    while time.ticks_diff(end_time, time.ticks_ms()) > 0:
        # Mark start of work
        monitor.mark_busy_start()
        
        # Do some work
        x = sum(range(1000))
        
        # Mark end of work
        monitor.mark_busy_end()
        
        # Simulate waiting (idle time)
        time.sleep_ms(2)
        
        # Update stats
        if monitor.update():
            monitor.print_stats()


# ==============================================================================
# METHOD 5: Memory Usage
# ==============================================================================
def test_memory():
    """Check available memory."""
    print("\n" + "=" * 60)
    print("METHOD 5: Memory Usage")
    print("=" * 60)
    
    gc.collect()  # Run garbage collector
    
    free = gc.mem_free()
    used = gc.mem_alloc()
    total = free + used
    
    print(f"Total RAM:          {total / 1024:.1f} KB")
    print(f"Used:               {used / 1024:.1f} KB ({used/total*100:.1f}%)")
    print(f"Free:               {free / 1024:.1f} KB ({free/total*100:.1f}%)")
    
    if free / total > 0.5:
        print("✅ Plenty of memory available")
    elif free / total > 0.3:
        print("⚠️  Moderate memory usage")
    else:
        print("❌ Low memory!")


# ==============================================================================
# METHOD 6: Quick Integration Example
# ==============================================================================
def integration_example():
    """Show how to integrate into your main loop."""
    print("\n" + "=" * 60)
    print("METHOD 6: Integration Example")
    print("=" * 60)
    print("""
To integrate into your main.py, add this to your regulation cycle:

```python
from src.utils.performance_monitor import PerformanceMonitor

# Create monitor (once at startup)
perf_monitor = PerformanceMonitor(sample_interval=2.0)

# In your main loop:
async def regulation_loop():
    while True:
        # Mark start of work
        perf_monitor.mark_busy_start()
        
        # Your actual regulation code
        await controller.update()
        
        # Mark end of work
        perf_monitor.mark_busy_end()
        
        # Check if it's time to print stats
        if perf_monitor.update():
            perf_monitor.print_stats()
        
        # Wait before next cycle (idle time)
        await asyncio.sleep(0.001)
```

The monitor will print stats every 2 seconds showing:
- CPU usage percentage
- Idle time percentage
- How much time is available for new features
""")


# ==============================================================================
# MAIN
# ==============================================================================
def main():
    """Run all performance tests."""
    print("\n" + "=" * 70)
    print(" " * 15 + "PERFORMANCE TESTING GUIDE")
    print(" " * 10 + "FOR DEVELOPMENT USE ONLY - REMOVE BEFORE RELEASE")
    print("=" * 70)
    
    try:
        # Run all tests
        test_simple_timing()
        time.sleep(1)
        
        test_simple_timer()
        time.sleep(1)
        
        test_decorator()
        time.sleep(1)
        
        test_performance_monitor()
        time.sleep(1)
        
        test_memory()
        time.sleep(1)
        
        integration_example()
        
        print("\n" + "=" * 70)
        print("✅ All performance tests completed!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")


if __name__ == "__main__":
    main()
