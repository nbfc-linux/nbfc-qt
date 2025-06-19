from collections import OrderedDict

class BasicFanConfigWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # GridLayout
        # =====================================================================

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # =====================================================================
        # Fan Display Name
        # =====================================================================

        label = QLabel("Fan display name", self)
        self.fan_display_name_input = QLineEdit(self)
        grid_layout.addWidget(label, 0, 0)
        grid_layout.addWidget(self.fan_display_name_input, 0, 1)

        # =====================================================================
        # Read Register
        # =====================================================================

        label = QLabel("Read register", self)
        self.read_register_input = QSpinBox(self)
        self.read_register_input.setRange(0, UINT8_MAX)
        grid_layout.addWidget(label, 1, 0)
        grid_layout.addWidget(self.read_register_input, 1, 1)

        # =====================================================================
        # Write Register
        # =====================================================================

        label = QLabel("Write register", self)
        self.write_register_input = QSpinBox(self)
        self.write_register_input.setRange(0, UINT8_MAX)
        grid_layout.addWidget(label, 2, 0)
        grid_layout.addWidget(self.write_register_input, 2, 1)

        # =====================================================================
        # Min Fan Speed
        # =====================================================================

        label = QLabel("Min. fan speed", self)
        self.min_fan_speed_write_input = QSpinBox(self)
        self.min_fan_speed_write_input.setRange(0, UINT8_MAX)
        grid_layout.addWidget(label, 3, 0)
        grid_layout.addWidget(self.min_fan_speed_write_input, 3, 1)

        # =====================================================================
        # Max Fan Speed
        # =====================================================================

        label = QLabel("Max. fan speed", self)
        self.max_fan_speed_write_input = QSpinBox(self)
        self.max_fan_speed_write_input.setRange(0, UINT8_MAX)
        grid_layout.addWidget(label, 4, 0)
        grid_layout.addWidget(self.max_fan_speed_write_input, 4, 1)

        # =====================================================================
        # GroupBox (IndependentReadMinMaxValues)
        # =====================================================================

        self.grp_read_values = QGroupBox("Use different min/max speeds for read operations")
        self.grp_read_values.setCheckable(True)
        self.grp_read_values.setChecked(False)
        layout.addWidget(self.grp_read_values)

        grp_layout = QGridLayout()
        self.grp_read_values.setLayout(grp_layout)
        
        # =====================================================================
        # Read Min Fan Speed
        # =====================================================================

        label = QLabel("Min. fan speed", self)
        self.min_fan_speed_read_input = QSpinBox(self)
        self.min_fan_speed_read_input.setRange(0, UINT8_MAX)
        grp_layout.addWidget(label, 0, 0)
        grp_layout.addWidget(self.min_fan_speed_read_input, 0, 1)

        # =====================================================================
        # Read Max Fan Speed
        # =====================================================================

        label = QLabel("Max. fan speed", self)
        self.max_fan_speed_read_input = QSpinBox(self)
        self.max_fan_speed_read_input.setRange(0, UINT8_MAX)
        grp_layout.addWidget(label, 1, 0)
        grp_layout.addWidget(self.max_fan_speed_read_input, 1, 1)

        # =====================================================================
        # GroupBox (ResetRequired)
        # =====================================================================

        self.grp_reset_required = QGroupBox("Reset on exit")
        self.grp_reset_required.setCheckable(True)
        self.grp_reset_required.setChecked(False)
        layout.addWidget(self.grp_reset_required)

        grp_layout = QGridLayout()
        self.grp_reset_required.setLayout(grp_layout)

        # =====================================================================
        # Reset value
        # =====================================================================

        label = QLabel("Reset value")
        self.reset_value = QSpinBox(self)
        self.reset_value.setRange(0, UINT8_MAX)

        grp_layout.addWidget(label, 0, 0)
        grp_layout.addWidget(self.reset_value, 0, 1)

        # =====================================================================
        # Sensors
        # =====================================================================

        box = QHBoxLayout()
        layout.addLayout(box)

        label = QLabel("Temperature sensor", self)
        self.sensor_input = QComboBox(self)
        self.sensor_input.addItems(["@CPU", "@GPU", "@CPU + @GPU"])

        box.addWidget(label)
        box.addWidget(self.sensor_input)

        # =====================================================================
        # Temperature Algorithm Type
        # =====================================================================

        box = QHBoxLayout()
        layout.addLayout(box)

        label = QLabel("Temperature algorithm type", self)
        self.algorithm_type = QComboBox(self)
        self.algorithm_type.addItems(["Average", "Min", "Max"])

        box.addWidget(label)
        box.addWidget(self.algorithm_type)

        # =====================================================================
        # Init
        # =====================================================================

        GLOBALS.read_write_words_changed.connect(self.read_write_words_changed)

    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        r = OrderedDict()

        r['FanDisplayName']              = self.fan_display_name_input.text().strip()
        r['WriteRegister']               = self.write_register_input.value()
        r['ReadRegister']                = self.read_register_input.value()
        r['MinSpeedValue']               = self.min_fan_speed_write_input.value()
        r['MaxSpeedValue']               = self.max_fan_speed_write_input.value()
        r['IndependentReadMinMaxValues'] = self.grp_read_values.isChecked()
        r['MinSpeedValueRead']           = self.min_fan_speed_read_input.value()
        r['MaxSpeedValueRead']           = self.max_fan_speed_read_input.value()
        r['ResetRequired']               = self.grp_reset_required.isChecked()
        r['FanSpeedResetValue']          = self.reset_value.value()
        r['Sensors']                     = self.sensors_get_config()
        r['TemperatureAlgorithmType']    = self.algorithm_type.currentText()

        if not r['FanDisplayName']:
            del r['FanDisplayName']

        if not r['ResetRequired']:
            del r['FanSpeedResetValue']

        if not r['IndependentReadMinMaxValues']:
            del r['MinSpeedValueRead']
            del r['MaxSpeedValueRead']

        return r

    def from_config(self, cfg, trace, errors):
        callbacks = {
            'FanDisplayName':              self.fan_display_name_input.setText,
            'WriteRegister':               self.write_register_input.setValue,
            'ReadRegister':                self.read_register_input.setValue,
            'MinSpeedValue':               self.min_fan_speed_write_input.setValue,
            'MaxSpeedValue':               self.max_fan_speed_write_input.setValue,
            'IndependentReadMinMaxValues': self.grp_read_values.setChecked,
            'MinSpeedValueRead':           self.min_fan_speed_read_input.setValue,
            'MaxSpeedValueRead':           self.max_fan_speed_read_input.setValue,
            'ResetRequired':               self.grp_reset_required.setChecked,
            'FanSpeedResetValue':          self.reset_value.setValue,
            'Sensors':                     self.sensors_from_config,
            'TemperatureAlgorithmType':    self.algorithm_type.setCurrentText,
        }

        for key, callback in list(callbacks.items()):
            if key not in cfg:
                continue

            with trace.trace(key):
                try:
                    callback(cfg[key])
                except Exception:
                    errors.append(trace.get_trace("Invalid type"))

            del cfg[key]

    # =========================================================================
    # Helper functions
    # =========================================================================

    def sensors_from_config(self, sensors):
        have_CPU = False
        have_GPU = False

        for sensor in sensors:
            if sensor == '@CPU':
                have_CPU = True
            elif sensor == '@GPU':
                have_GPU = True

        if have_CPU and have_GPU:
            self.sensor_input.setCurrentText('@CPU + @GPU')
        elif have_CPU:
            self.sensor_input.setCurrentText('@CPU')
        elif have_GPU:
            self.sensor_input.setCurrentText('@GPU')
        else:
            self.sensor_input.setCurrentText('@CPU')

    def sensors_get_config(self):
        text = self.sensor_input.currentText()

        if text == '@CPU':
            return ['@CPU']

        if text == '@GPU':
            return ['@GPU']

        if text == '@CPU + @GPU':
            return ['@CPU', '@GPU']

    # =========================================================================
    # Signals
    # =========================================================================

    def read_write_words_changed(self, read_write_words):
        input_widgets = [
            self.min_fan_speed_write_input,
            self.max_fan_speed_write_input,
            self.min_fan_speed_read_input,
            self.max_fan_speed_read_input,
            self.reset_value
        ]

        max_range = UINT16_MAX if read_write_words else UINT8_MAX

        for input_widget in input_widgets:
            input_widget.setRange(0, max_range)
