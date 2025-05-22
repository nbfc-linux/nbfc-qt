def validate_fan_index(fan_temperature_source, fan_count):
    if 'FanIndex' not in fan_temperature_source:
        return ['Missing field: FanIndex']

    fan_index = fan_temperature_source['FanIndex']

    if not isinstance(fan_index, int):
        return ['FanIndex: Invalid type (expected integer)']

    if fan_index < 0:
        return ['FanIndex: Cannot be negative']

    if fan_index >= fan_count:
        return ['FanIndex: No fan found for FanIndex `%d`' % fan_index]

    return []

def validate_algorithm_type(fan_temperature_source):
    if 'TemperatureAlgorithmType' not in fan_temperature_source:
        return []

    algorithm = fan_temperature_source['TemperatureAlgorithmType']

    if not isinstance(algorithm, str):
        return ['TemperatureAlgorithmType: Invalid type (expected string)']

    if algorithm not in ('Average', 'Min', 'Max'):
        return ['TemperatureAlgorithmType: Invalid value: %s' % algorithm]

    return []

def validate_sensors(fan_temperature_source):
    if 'Sensors' not in fan_temperature_source:
        return []

    sensors = fan_temperature_source['Sensors']

    if not isinstance(sensors, list):
        return ['Sensors: Invalid type (expected array)']

    errs = []

    for i, sensor in enumerate(fan_temperature_source['Sensors']):
        if not isinstance(sensor, str):
            errs.append('Sensors[%d]: Invalid type (expected string)' % i)

    return errs

def validate_fan_temperature_sources(fan_temperature_sources, fan_count):
    '''
    Checks `fan_temperature_sources` for errors.

    Args:
        fan_temperature_sources (list): A list of FanTemperatureSource objects.
        fan_count (int): The fan count of the service.

    Returns:
        list: A list of error strings describing what's wrong. This list is
              empty if no errors are found.
    '''

    errors = []

    for i, fan_temperature_source in enumerate(fan_temperature_sources):

        for err in validate_fan_index(fan_temperature_source, fan_count):
            errors.append('FanTemperatureSources[%d]: %s' % (i, err))

        for err in validate_algorithm_type(fan_temperature_source):
            errors.append('FanTemperatureSources[%d]: %s' % (i, err))

        for err in validate_sensors(fan_temperature_source):
            errors.append('FanTemperatureSources[%d]: %s' % (i, err))

        # Check for invalid fields
        for field in fan_temperature_source:
            if field not in ('FanIndex', 'TemperatureAlgorithmType', 'Sensors'):
                errors.append('FanTemperatureSources[%d]: Unknown field: %s' % (i, field))

    return errors

def fix_fan_temperature_source(fan_temperature_source, fan_count):
    # =========================================================================
    # Fix FanIndex
    #
    # - Drop configuration completely if FanIndex is invalid
    # =========================================================================

    if 'FanIndex' not in fan_temperature_source:
        return None

    fan_index = fan_temperature_source.get('FanIndex', None)

    if not isinstance(fan_index, int):
        return None

    if fan_index < 0:
        return None

    if fan_index >= fan_count:
        return None

    # =========================================================================
    # Fix TemperatureAlgorithmType
    #
    # - Unset the value if TemperatureAlgorithmType is invalid
    # =========================================================================

    algorithm = None

    if 'TemperatureAlgorithmType' in fan_temperature_source:
        algorithm = fan_temperature_source['TemperatureAlgorithmType']

        if algorithm not in ('Average', 'Min', 'Max'):
            algorithm = None

    # =========================================================================
    # Fix Sensors
    #
    # - Drop sensors that are not string
    # =========================================================================

    sensors = []

    if 'Sensors' in fan_temperature_source:
        if isinstance(fan_temperature_source['Sensors'], list):
            for sensor in fan_temperature_source['Sensors']:
                if not isinstance(sensor, str):
                    continue

                sensors.append(sensor)

    # =========================================================================
    # Return the object
    # =========================================================================

    obj = {'FanIndex': fan_index}

    if algorithm:
        obj['TemperatureAlgorithmType'] = algorithm

    if sensors:
        obj['Sensors'] = sensors

    return obj

def fix_fan_temperature_sources(fan_temperature_sources, fan_count):
    '''
    Fixes an invalid FanTemperatureSources config.

    Args:
        fan_temperature_sources (list): A list of FanTemperatureSource objects.
        fan_count (int): The fan count of the service.

    Returns:
        list: A list of fixed FanTemperatureSource objects.
    '''

    result = []

    for fan_temperature_source in fan_temperature_sources:
        o = fix_fan_temperature_source(fan_temperature_source, fan_count)
        if o:
            result.append(o)

    return result

