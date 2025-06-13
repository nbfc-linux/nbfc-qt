from collections import OrderedDict

class BasicConfigWidget(QWidget):
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
        # Model name
        # =====================================================================

        label = QLabel("Model name", self)

        box = QHBoxLayout()
        self.model_input = QLineEdit(self)
        self.model_set_button = QPushButton("Insert model", self)
        self.model_set_button.clicked.connect(self.model_set_button_clicked)
        box.addWidget(self.model_input)
        box.addWidget(self.model_set_button)

        grid_layout.addWidget(label, 0, 0)
        grid_layout.addLayout(box, 0, 1)

        # =====================================================================
        # Author
        # =====================================================================

        label = QLabel("Config author", self)
        self.author_input = QLineEdit(self)
        grid_layout.addWidget(label, 1, 0)
        grid_layout.addWidget(self.author_input, 1, 1)

        # =====================================================================
        # EC Poll Interval
        # =====================================================================

        label = QLabel("EC poll interval (ms)", self)
        self.ec_poll_interval_input = QSpinBox(self)
        self.ec_poll_interval_input.setRange(0, UINT16_MAX)
        grid_layout.addWidget(label, 2, 0)
        grid_layout.addWidget(self.ec_poll_interval_input, 2, 1)

        # =====================================================================
        # Critical Temperature
        # =====================================================================

        label = QLabel("Critical temperature (°C)")
        self.critial_temperature_input = QSpinBox(self)
        self.critial_temperature_input.setRange(INT16_MIN, INT16_MAX)
        grid_layout.addWidget(label, 3, 0)
        grid_layout.addWidget(self.critial_temperature_input, 3, 1)

        # =====================================================================
        # Critical Temperature Offset
        # =====================================================================

        label = QLabel("Critical temperature offset")
        self.critial_temperature_offset_input = QSpinBox(self)
        self.critial_temperature_offset_input.setRange(0, UINT16_MAX)
        grid_layout.addWidget(label, 4, 0)
        grid_layout.addWidget(self.critial_temperature_offset_input, 4, 1)

        # =====================================================================
        # Read/Write Mode
        # =====================================================================

        label = QLabel("Read/Write mode", self)

        self.group_read_write = QButtonGroup()
        self.group_read_write.setExclusive(True)
        radio_layout = QHBoxLayout()

        self.byte_radio = QRadioButton("Byte", self)
        self.word_radio = QRadioButton("Word", self)
        self.byte_radio.clicked.connect(self.byte_radio_clicked)
        self.word_radio.clicked.connect(self.word_radio_clicked)
        radio_layout.addWidget(self.byte_radio)
        radio_layout.addWidget(self.word_radio)
        self.group_read_write.addButton(self.byte_radio)
        self.group_read_write.addButton(self.word_radio)
        
        grid_layout.addWidget(label, 5, 0)
        grid_layout.addLayout(radio_layout, 5, 1)

        # =====================================================================
        # LegacyTemperatureThreholdsBehaviour
        # =====================================================================

        label = QLabel("Temperature Threshold behaviour")

        self.group_legacy = QButtonGroup()
        self.group_legacy.setExclusive(True)
        radio_layout = QHBoxLayout()
        
        self.normal_radio = QRadioButton("Normal", self)
        self.legacy_radio = QRadioButton("Legacy", self)
        radio_layout.addWidget(self.normal_radio)
        radio_layout.addWidget(self.legacy_radio)
        self.group_legacy.addButton(self.normal_radio)
        self.group_legacy.addButton(self.legacy_radio)

        grid_layout.addWidget(label, 6, 0)
        grid_layout.addLayout(radio_layout, 6, 1)

        # =====================================================================
        # Stretch
        # =====================================================================

        layout.addStretch()

        # =====================================================================
        # Init
        # =====================================================================

        self.set_defaults()

    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        return OrderedDict([
            ('LegacyTemperatureThresholdsBehaviour', self.legacy_radio.isChecked()),
            ('NotebookModel',                        self.model_input.text()),
            ('Author',                               self.author_input.text()),
            ('EcPollInterval',                       self.ec_poll_interval_input.value()),
            ('CriticalTemperature',                  self.critial_temperature_input.value()),
            ('CriticalTemperatureOffset',            self.critial_temperature_offset_input.value()),
            ('ReadWriteWords',                       self.word_radio.isChecked()),
        ])

    def from_config(self, cfg, trace, errors):
        self.set_defaults()

        callbacks = {
            'LegacyTemperatureThresholdsBehaviour': self.set_legacy_temperature_behaviour,
            'Author':                               self.author_input.setText,
            'NotebookModel':                        self.model_input.setText,
            'EcPollInterval':                       self.ec_poll_interval_input.setValue,
            'CriticalTemperature':                  self.critial_temperature_input.setValue,
            'CriticalTemperatureOffset':            self.critial_temperature_offset_input.setValue,
            'ReadWriteWords':                       self.set_read_write_words,
        }

        for key, callback in callbacks.items():
            if key not in cfg:
                continue

            with trace.trace(key):
                try:
                    callback(cfg[key])
                except Exception as e:
                    errors.append(trace.get_trace("Invalid type"))

                del cfg[key]

    # =========================================================================
    # Helper functions
    # =========================================================================

    def set_defaults(self):
        self.ec_poll_interval_input.setValue(DEFAULT_EC_POLL_INTERVAL)
        self.critial_temperature_input.setValue(DEFAULT_CRITICAL_TEMPERATURE)
        self.critial_temperature_offset_input.setValue(DEFAULT_CRITICAL_TEMPERATURE_OFFSET)
        self.set_legacy_temperature_behaviour(DEFAULT_LEGACY_TEMPERATURE_BEHAVIOUR)
        self.set_read_write_words(DEFAULT_READ_WRITE_WORDS)

    def set_read_write_words(self, enable):
        self.byte_radio.setChecked(not enable)
        self.word_radio.setChecked(enable)

    def set_legacy_temperature_behaviour(self, enable):
        self.normal_radio.setChecked(not enable)
        self.legacy_radio.setChecked(enable)

    # =========================================================================
    # Signals
    # =========================================================================

    def model_set_button_clicked(self):
        try:
            model_name = GLOBALS.nbfc_client.get_model_name()
            self.model_input.setText(model_name)
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def byte_radio_clicked(self):
        GLOBALS.read_write_words_changed.emit(False)

    def word_radio_clicked(self):
        GLOBALS.read_write_words_changed.emit(True)
