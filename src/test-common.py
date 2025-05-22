#!/usr/bin/python

from common import *

def test(
    number,
    fan_temperature_sources,
    fan_count,
    expected_errors,
    expected_fixed):

    errors = validate_fan_temperature_sources(fan_temperature_sources, fan_count)

    if errors != expected_errors:
        raise Exception('Failed test: %d\nExpected: %s\nGot: %s' % (number, expected_errors, errors))

    fixed = fix_fan_temperature_sources(fan_temperature_sources, fan_count)

    if fixed != expected_fixed:
        raise Exception('Failed test: %d\nExpected: %s\nGot: %s' % (number, expected_fixed, fixed))

test(0,
     [ {} ], 1,
     ['FanTemperatureSources[0]: Missing field: FanIndex'],
     []
     )

test(1,
     [ {'FanIndex': "invalid"} ], 1,
     ['FanTemperatureSources[0]: FanIndex: Invalid type (expected integer)'],
     []
     )

test(2,
     [ {'FanIndex': -1} ], 1,
     ['FanTemperatureSources[0]: FanIndex: Cannot be negative'],
     []
     )

test(3,
     [ {'FanIndex': 1} ], 1,
     ['FanTemperatureSources[0]: FanIndex: No fan found for FanIndex `1`'],
     []
     )

test(4,
     [ {'FanIndex': 0, 'TemperatureAlgorithmType': 1} ], 1,
     ['FanTemperatureSources[0]: TemperatureAlgorithmType: Invalid type (expected string)'],
     [ {'FanIndex': 0} ]
     )

test(5,
     [ {'FanIndex': 0, 'TemperatureAlgorithmType': 'Foo'} ], 1,
     ['FanTemperatureSources[0]: TemperatureAlgorithmType: Invalid value: Foo'],
     [ {'FanIndex': 0} ]
     )

test(6,
     [ {'FanIndex': 0, 'Sensors': ['Foo', 1, 'Bar']} ], 1,
     ['FanTemperatureSources[0]: Sensors[1]: Invalid type (expected string)'],
     [ {'FanIndex': 0, 'Sensors': ['Foo', 'Bar']} ]
     )


test(7,
     [ {'FanIndex': 0, 'Sensors': 'invalid'} ], 1,
     ['FanTemperatureSources[0]: Sensors: Invalid type (expected array)'],
     [ {'FanIndex': 0} ]
     )

test(8,
     [ {'FanIndex': 0, 'Foo': 'Bar'} ], 1,
     ['FanTemperatureSources[0]: Unknown field: Foo'],
     [ {'FanIndex': 0} ]
     )
