"""
Performance Monitor for MicroPython
Measures CPU usage and available processing time
FOR DEVELOPMENT USE ONLY - Remove before final release
"""

import time
import gc


class PerformanceMonitor:
    """Monitor CPU usage and available processing time."""
    
    def __init__(self, sample_interval=1.0):
        """
        Initialize performance monitor.
        
        Args:
            sample_interval: Time window for measuring CPU usage (seconds)
        """
        self.sample_interval = sample_interval
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        self._start_time = time.ticks_ms()
        self._last_sample_time = self._start_time
        self._busy_time = 0
        self._idle_time = 0
        self._last_tick = self._start_time
        self._is_busy = False
        
        # Statistics
        self.cpu_usage_percent = 0.0
        self.idle_percent = 0.0
        self.iterations = 0
        self.avg_iteration_time = 0.0
    
    def mark_busy_start(self):
        """Mark the start of a busy period (doing work)."""
        now = time.ticks_ms()
        if not self._is_busy:
            # We were idle, add idle time
            self._idle_time += time.ticks_diff(now, self._last_tick)
            self._is_busy = True
        self._last_tick = now
    
    def mark_busy_end(self):
        """Mark the end of a busy period (work done)."""
        now = time.ticks_ms()
        if self._is_busy:
            # We were busy, add busy time
            self._busy_time += time.ticks_diff(now, self._last_tick)
            self._is_busy = False
            self.iterations += 1
        self._last_tick = now
    
    def update(self):
        """
        Update statistics if sample interval has passed.
        
        Returns:
            bool: True if statistics were updated, False otherwise
        """
        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, self._last_sample_time)
        
        if elapsed >= self.sample_interval * 1000:
            # Calculate percentages
            total_time = self._busy_time + self._idle_time
            
            if total_time > 0:
                self.cpu_usage_percent = (self._busy_time / total_time) * 100
                self.idle_percent = (self._idle_time / total_time) * 100
            else:
                self.cpu_usage_percent = 0.0
                self.idle_percent = 100.0
            
            # Calculate average iteration time
            if self.iterations > 0:
                self.avg_iteration_time = self._busy_time / self.iterations
            
            # Reset for next sample
            self._last_sample_time = now
            self._busy_time = 0
            self._idle_time = 0
            self.iterations = 0
            
            return True
        
        return False
    
    def get_stats(self):
        """
        Get current performance statistics.
        
        Returns:
            dict: Performance statistics
        """
        return {
            'cpu_usage': self.cpu_usage_percent,
            'idle': self.idle_percent,
            'avg_iteration_ms': self.avg_iteration_time,
            'iterations_per_sec': self.iterations / self.sample_interval if self.iterations > 0 else 0,
            'free_memory_kb': gc.mem_free() / 1024,
            'used_memory_kb': gc.mem_alloc() / 1024
        }
    
    def print_stats(self):
        """Print formatted performance statistics."""
        stats = self.get_stats()
        print("\n" + "=" * 60)
        print("PERFORMANCE MONITOR (Development Only)")
        print("=" * 60)
        print(f"CPU Usage:          {stats['cpu_usage']:.1f}%")
        print(f"Idle Time:          {stats['idle']:.1f}%")
        print(f"Avg Iteration:      {stats['avg_iteration_ms']:.2f} ms")
        print(f"Iterations/sec:     {stats['iterations_per_sec']:.1f}")
        print(f"Free Memory:        {stats['free_memory_kb']:.1f} KB")
        print(f"Used Memory:        {stats['used_memory_kb']:.1f} KB")
        print("=" * 60)
        
        # Provide guidance
        if stats['idle'] > 50:
            print("✅ GOOD: >50% idle time - plenty of room for more features")
        elif stats['idle'] > 30:
            print("⚠️  MODERATE: 30-50% idle - some room for features")
        elif stats['idle'] > 10:
            print("⚠️  WARNING: 10-30% idle - limited capacity")
        else:
            print("❌ CRITICAL: <10% idle - system near capacity!")
        print()


class SimpleTimer:
    """Simple timer for measuring code execution time."""
    
    def __init__(self, name="Timer"):
        """
        Initialize timer.
        
        Args:
            name: Name for this timer (for logging)
        """
        self.name = name
        self.start_time = None
        self.elapsed_ms = 0
    
    def start(self):
        """Start timing."""
        self.start_time = time.ticks_us()
    
    def stop(self):
        """Stop timing and return elapsed time in milliseconds."""
        if self.start_time is not None:
            elapsed_us = time.ticks_diff(time.ticks_us(), self.start_time)
            self.elapsed_ms = elapsed_us / 1000
            return self.elapsed_ms
        return 0
    
    def print_elapsed(self):
        """Print elapsed time."""
        print(f"{self.name}: {self.elapsed_ms:.3f} ms")


# Quick inline timing decorator
def time_function(func):
    """
    Decorator to time function execution.
    FOR DEVELOPMENT ONLY - Remove before final release.
    
    Usage:
        @time_function
        def my_function():
            # your code
    """
    def wrapper(*args, **kwargs):
        start = time.ticks_us()
        result = func(*args, **kwargs)
        elapsed = time.ticks_diff(time.ticks_us(), start) / 1000
        print(f"⏱️  {func.__name__}(): {elapsed:.3f} ms")
        return result
    return wrapper
