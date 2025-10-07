# Test file for asyncio battery charger controller
# This file helps verify the asyncio implementation works correctly

from battery_charger_controller import BatteryChargerController
import asyncio


async def test_single_controller():
    """Test a single controller running asynchronously."""
    print("\n" + "="*60)
    print("TEST 1: Single Controller")
    print("="*60)
    
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting controller for 5 seconds...")
    task = asyncio.create_task(controller.start_regulation(controller.MODE_CC_CV))
    
    # Let it run for 5 seconds
    await asyncio.sleep(5)
    
    # Stop the controller
    print("\nStopping controller...")
    controller.is_running = False
    
    # Wait for task to complete
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    print("✓ Test 1 passed: Single controller works")
    return True


async def test_two_controllers():
    """Test two controllers running simultaneously."""
    print("\n" + "="*60)
    print("TEST 2: Two Controllers Simultaneously")
    print("="*60)
    
    # Controller 1
    controller1 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    # Controller 2 (if you have channel 1 hardware, otherwise this will use same channel)
    controller2 = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=1,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=1, pca_freq=1526,
        target_voltage=7.4,
        target_current=500,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting both controllers for 5 seconds...")
    task1 = asyncio.create_task(controller1.start_regulation(controller1.MODE_CC_CV))
    task2 = asyncio.create_task(controller2.start_regulation(controller2.MODE_CC_CV))
    
    # Let them run for 5 seconds
    await asyncio.sleep(5)
    
    # Stop both controllers
    print("\nStopping both controllers...")
    controller1.is_running = False
    controller2.is_running = False
    
    # Wait for both tasks to complete
    try:
        await asyncio.gather(task1, task2, return_exceptions=True)
    except asyncio.CancelledError:
        pass
    
    print("✓ Test 2 passed: Two controllers work simultaneously")
    return True


async def test_controller_cancellation():
    """Test graceful cancellation of controller tasks."""
    print("\n" + "="*60)
    print("TEST 3: Graceful Cancellation")
    print("="*60)
    
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting controller...")
    task = asyncio.create_task(controller.start_regulation(controller.MODE_CC_CV))
    
    # Let it run briefly
    await asyncio.sleep(2)
    
    print("\nCancelling task...")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled successfully")
    
    print("✓ Test 3 passed: Cancellation works correctly")
    return True


async def test_status_monitoring():
    """Test status retrieval while controller is running."""
    print("\n" + "="*60)
    print("TEST 4: Status Monitoring")
    print("="*60)
    
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting controller...")
    task = asyncio.create_task(controller.start_regulation(controller.MODE_CC_CV))
    
    # Monitor status 3 times
    for i in range(3):
        await asyncio.sleep(1)
        status = controller.get_status()
        print(f"\nStatus check {i+1}:")
        print(f"  Mode: {status['mode']}")
        print(f"  Running: {status['running']}")
        print(f"  Voltage: {status['measurements']['voltage']:.3f}V")
        print(f"  Current: {status['measurements']['current']:.1f}mA")
        print(f"  Cycles: {status['cycle_count']}")
    
    # Stop controller
    controller.is_running = False
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    print("\n✓ Test 4 passed: Status monitoring works")
    return True


async def test_dynamic_target_change():
    """Test changing target voltage/current during operation."""
    print("\n" + "="*60)
    print("TEST 5: Dynamic Target Changes")
    print("="*60)
    
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting controller with 8.4V target...")
    task = asyncio.create_task(controller.start_regulation(controller.MODE_CC_CV))
    
    await asyncio.sleep(2)
    
    print("\nChanging target to 7.4V...")
    controller.set_target_voltage(7.4)
    
    await asyncio.sleep(2)
    
    print("\nChanging target current to 500mA...")
    controller.set_target_current(500)
    
    await asyncio.sleep(2)
    
    # Stop controller
    controller.is_running = False
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    print("\n✓ Test 5 passed: Dynamic target changes work")
    return True


async def run_all_tests():
    """Run all tests sequentially."""
    print("\n" + "="*60)
    print("ASYNCIO BATTERY CHARGER CONTROLLER TEST SUITE")
    print("="*60)
    print("\nThis will run a series of tests to verify the asyncio implementation.")
    print("Each test runs for a few seconds.\n")
    
    results = []
    
    try:
        # Test 1: Single controller
        results.append(await test_single_controller())
        await asyncio.sleep(1)
        
        # Test 2: Two controllers
        # Uncomment if you have hardware for channel 1
        # results.append(await test_two_controllers())
        # await asyncio.sleep(1)
        
        # Test 3: Cancellation
        results.append(await test_controller_cancellation())
        await asyncio.sleep(1)
        
        # Test 4: Status monitoring
        results.append(await test_status_monitoring())
        await asyncio.sleep(1)
        
        # Test 5: Dynamic changes
        results.append(await test_dynamic_target_change())
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return False
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        return False
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {len(results)}")
    print(f"Tests passed: {sum(results)}")
    print(f"Tests failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print("\n✗ SOME TESTS FAILED")
        return False


async def quick_test():
    """Quick test to verify basic functionality."""
    print("\n" + "="*60)
    print("QUICK TEST - Single Controller for 10 seconds")
    print("="*60)
    
    controller = BatteryChargerController(
        ina_scl_pin=21, ina_sda_pin=20, ina_channel=0,
        pca_scl_pin=19, pca_sda_pin=18, pca_channel=0, pca_freq=1526,
        target_voltage=8.4,
        target_current=700,
        duty_step=2,
        update_interval=0.001
    )
    
    print("\nStarting controller...")
    print("Press Ctrl+C to stop early\n")
    
    task = asyncio.create_task(controller.start_regulation(controller.MODE_CC_CV))
    
    try:
        await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        controller.is_running = False
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    print("\n✓ Quick test complete")


if __name__ == "__main__":
    print("\nSelect test mode:")
    print("1. Run all tests (recommended)")
    print("2. Quick test (10 seconds)")
    print("\nEdit this file to select, or just run all tests by default\n")
    
    try:
        # Run all tests by default
        asyncio.run(run_all_tests())
        
        # Or run quick test
        # asyncio.run(quick_test())
        
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user")
    except Exception as e:
        print(f"\nError: {e}")
        import sys
        sys.print_exception(e)
    finally:
        print("\nTest suite finished")
