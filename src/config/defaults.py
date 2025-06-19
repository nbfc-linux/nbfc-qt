from collections import OrderedDict

#define DEFAULT_EC_POLL_INTERVAL                3000
#define DEFAULT_CRITICAL_TEMPERATURE            75
#define DEFAULT_CRITICAL_TEMPERATURE_OFFSET     15
#define DEFAULT_LEGACY_TEMPERATURE_BEHAVIOUR    False
#define DEFAULT_READ_WRITE_WORDS                False

def TemperatureThreshold(up_threshold, down_threshold, fan_speed):
    return OrderedDict([
        ('UpThreshold',   up_threshold),
        ('DownThreshold', down_threshold),
        ('FanSpeed',      fan_speed),
    ])

DEFAULT_TEMPERATURE_THRESHOLDS = [
  TemperatureThreshold(60,  0,   0),
  TemperatureThreshold(63, 48,  10),
  TemperatureThreshold(66, 55,  20),
  TemperatureThreshold(68, 59,  50),
  TemperatureThreshold(71, 63,  70),
  TemperatureThreshold(75, 67, 100),
]

DEFAULT_LEGACY_TEMPERATURE_THRESHOLDS = [
  TemperatureThreshold(0,   0,   0),
  TemperatureThreshold(60, 48,  10),
  TemperatureThreshold(63, 55,  20),
  TemperatureThreshold(66, 59,  50),
  TemperatureThreshold(68, 63,  70),
  TemperatureThreshold(71, 67, 100),
]
