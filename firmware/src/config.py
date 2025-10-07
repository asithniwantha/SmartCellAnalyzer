# Smart Cell Analyzer - Configuration File
# Central configuration for all hardware and control parameters

# ============================================================================
# Hardware Pin Configuration
# ============================================================================

# INA3221 Current/Voltage Sensor (I2C0)
INA3221_SCL_PIN = 21
INA3221_SDA_PIN = 20
INA3221_I2C_FREQ = 400000
INA3221_ADDRESS = 0x40

# PCA9685 PWM Controller (I2C1)
PCA9685_SCL_PIN = 19
PCA9685_SDA_PIN = 18
PCA9685_I2C_FREQ = 400000
PCA9685_ADDRESS = 0x40
PCA9685_DEFAULT_FREQ = 1526  # PWM frequency in Hz

# ============================================================================
# Safety Limits
# ============================================================================

# Voltage Limits (Volts)
MAX_VOLTAGE = 30.0
MIN_VOLTAGE = 0.1
DEFAULT_TARGET_VOLTAGE = 7.2

# Current Limits (mA)
MAX_CURRENT = 5000
MIN_CURRENT = 0
DEFAULT_TARGET_CURRENT = 1000

# Power Limits (Watts)
MAX_POWER = 150.0

# Temperature Limits (Celsius) - if temperature monitoring is added
MAX_TEMPERATURE = 85.0
WARNING_TEMPERATURE = 70.0

# ============================================================================
# Control Parameters
# ============================================================================

# PWM Control
MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 4095
DEFAULT_DUTY_STEP = 2

# Control Loop Timing
DEFAULT_UPDATE_INTERVAL = 0.001  # 1ms (1000 Hz)
FAST_UPDATE_INTERVAL = 0.0005    # 0.5ms (2000 Hz)
SLOW_UPDATE_INTERVAL = 0.010     # 10ms (100 Hz)

# Regulation Tolerances
DEFAULT_VOLTAGE_TOLERANCE = 0.05  # ±50mV
DEFAULT_CURRENT_TOLERANCE = 50    # ±50mA

# ============================================================================
# Battery Profiles
# ============================================================================

BATTERY_PROFILES = {
    'li_ion_single': {
        'name': 'Li-ion Single Cell',
        'voltage': 4.2,
        'current': 1000,
        'min_voltage': 3.0,
        'max_voltage': 4.2
    },
    'li_ion_2s': {
        'name': 'Li-ion 2S Pack',
        'voltage': 8.4,
        'current': 2000,
        'min_voltage': 6.0,
        'max_voltage': 8.4
    },
    'li_ion_3s': {
        'name': 'Li-ion 3S Pack',
        'voltage': 12.6,
        'current': 2000,
        'min_voltage': 9.0,
        'max_voltage': 12.6
    },
    'lead_acid_6v': {
        'name': '6V Lead Acid',
        'voltage': 7.2,
        'current': 1500,
        'min_voltage': 5.5,
        'max_voltage': 7.5
    },
    'lead_acid_12v': {
        'name': '12V Lead Acid',
        'voltage': 14.4,
        'current': 3000,
        'min_voltage': 11.0,
        'max_voltage': 15.0
    },
    'nimh_6cell': {
        'name': 'NiMH 6-Cell',
        'voltage': 8.4,
        'current': 1000,
        'min_voltage': 6.0,
        'max_voltage': 9.0
    }
}

# ============================================================================
# Shunt Resistor Configuration
# ============================================================================

# Shunt resistance values in ohms for each INA3221 channel
SHUNT_RESISTANCES = [0.1, 0.1, 0.1]  # Channel 0, 1, 2

# ============================================================================
# Logging Configuration
# ============================================================================

# Logging intervals
LOG_INTERVAL = 1.0  # Log every 1 second
STATUS_PRINT_INTERVAL = 500  # Print status every 500 cycles

# Log levels
LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3
DEFAULT_LOG_LEVEL = LOG_LEVEL_INFO

# ============================================================================
# Data Storage
# ============================================================================

# File paths (if SD card is available)
DATA_LOG_PATH = "/sd/logs/"
PROFILE_PATH = "/sd/profiles/"
CONFIG_PATH = "/sd/config/"

# ============================================================================
# Display Configuration (if display is added)
# ============================================================================

DISPLAY_UPDATE_INTERVAL = 0.5  # Update display every 500ms
DISPLAY_BRIGHTNESS = 128  # 0-255

# ============================================================================
# Network Configuration (if WiFi is added)
# ============================================================================

WIFI_ENABLED = False
WIFI_SSID = "SmartCellAnalyzer"
WIFI_PASSWORD = ""
WEB_SERVER_PORT = 80
API_ENABLED = False

# ============================================================================
# Advanced Features
# ============================================================================

# Enable/disable features
ENABLE_TEMPERATURE_MONITORING = False
ENABLE_DATA_LOGGING = False
ENABLE_WEB_INTERFACE = False
ENABLE_CALIBRATION_MODE = False

# Calibration
VOLTAGE_CALIBRATION_OFFSET = 0.0  # Volts
CURRENT_CALIBRATION_OFFSET = 0.0  # mA
VOLTAGE_CALIBRATION_SCALE = 1.0
CURRENT_CALIBRATION_SCALE = 1.0

# ============================================================================
# System Information
# ============================================================================

FIRMWARE_VERSION = "1.0.0"
HARDWARE_VERSION = "1.0"
DEVICE_NAME = "Smart Cell Analyzer"

# ============================================================================
# Debug Configuration
# ============================================================================

DEBUG_MODE = False
VERBOSE_OUTPUT = False
SIMULATE_HARDWARE = False  # For testing without hardware
