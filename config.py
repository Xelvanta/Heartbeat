# config.py

LOG_FILE = 'system_metrics.log'
LOG_LEVEL = 'INFO'
OVERLAY_ENABLED = True  # Set to False to disable overlay
FLASK_ENABLED = True  # Set to False to disable the Heartbeat Dashboard
WARNING_THRESHOLD = 90  # Memory warning threshold (%)
CRITICAL_THRESHOLD = 95  # Memory critical threshold (%)
FATAL_THRESHOLD = 99  # Memory fatal threshold (%)
LOG_FREQUENCY = 0.5  # Log frequency (s)