# Examples

This directory contains example code demonstrating various features of the Smart Cell Analyzer.

## Available Examples

### charger_example.py
Basic usage examples including:
- Single controller voltage regulation
- Interactive command-line interface
- Preset charging profiles for different battery types

### multi_controller_example.py
Advanced multi-controller examples showing:
- Running multiple controllers simultaneously
- Multi-channel battery management
- Coordinated charging operations

## Usage

Upload examples to your Pico and run them:

```python
# Example 1: Basic charger
import examples.charger_example as example
example.main()

# Example 2: Multi-controller
import examples.multi_controller_example as multi
multi.main()
```

## Customization

Feel free to modify these examples for your specific needs. They serve as templates for building your own battery charging applications.
