# Tests

This directory contains the test suite for the Smart Cell Analyzer firmware.

## Available Tests

### test_asyncio.py
Comprehensive async functionality tests including:
- Single controller operation
- Task cancellation
- Status monitoring
- Dynamic parameter changes
- Multi-controller scenarios

## Running Tests

Upload tests to your Pico and run:

```python
import tests.test_asyncio as test
# Tests will run automatically on import
```

## Test Coverage

Current test coverage:
- ✓ Asyncio controller operation
- ✓ Cancellation and cleanup
- ✓ Status monitoring
- ✓ Dynamic configuration
- ✓ Multi-channel operation

## Adding Tests

When adding new features, please add corresponding tests following the existing pattern.

Test structure:
1. Test description
2. Setup
3. Test execution
4. Verification
5. Cleanup
6. Result reporting
