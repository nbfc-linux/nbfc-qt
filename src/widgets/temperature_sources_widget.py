class TemperatureSourcesWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        MODEL_CONFIG_CHANGED.changed.connect(self.setup_ui)

        # Error Widget ========================================================
        self.error_widget = QWidget()
        error_layout = QVBoxLayout()
        self.error_widget.setLayout(error_layout)
        self.error_label = QLabel("", self)
        error_layout.addWidget(self.error_label)
        button_layout = QHBoxLayout()
        self.retry_button = QPushButton("Retry", self)
        self.retry_button.clicked.connect(self.setup_ui)
        self.fix_button = QPushButton("Fix errors automatically", self)
        self.fix_button.clicked.connect(self.fix_errors)
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.fix_button)
        error_layout.addLayout(button_layout)
        self.addWidget(self.error_widget)

        # Main Widget =========================================================
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.main_widget.setLayout(main_layout)

        self.available_temperature_sources = QListWidget(self)
        self.available_temperature_sources.setMaximumHeight(100)
        main_layout.addWidget(self.available_temperature_sources)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        temperature_sources_widget = QWidget()
        self.temperature_sources_layout = QVBoxLayout()
        temperature_sources_widget.setLayout(self.temperature_sources_layout)
        self.scroll_area.setWidget(temperature_sources_widget)
        main_layout.addWidget(self.scroll_area)

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.apply_button.clicked.connect(self.apply)
        self.apply_buttons_widget.apply_with_restart_button.clicked.connect(self.apply_with_restart)
        main_layout.addWidget(self.apply_buttons_widget)
        self.addWidget(self.main_widget)

        self.setup_ui()

    def start(self):
        pass

    def stop(self):
        pass

    def apply(self):
        config = NBFC_CLIENT.get_config()
        config['FanTemperatureSources'] = self.get_fan_temperature_sources()
        if not len(config['FanTemperatureSources']):
            del config['FanTemperatureSources']
        NBFC_CLIENT.set_config(config)

    def apply_with_restart(self):
        self.apply()
        NBFC_CLIENT.restart(self.apply_buttons_widget.read_only_checkbox.isChecked())

    def find_sensor_item(self, sensor):
        for i in range(self.available_temperature_sources.count()):
            item = self.available_temperature_sources.item(i)
            if item.data(Qt.UserRole) == sensor:
                return item

        raise Exception('No sensor found for %s' % sensor)

    def fix_errors(self):
        self.setup_ui(fix_errors=True)

    def setup_ui(self, fix_errors=False):
        if not IS_ROOT:
            self.apply_buttons_widget.disable(NOT_ROOT_NOTICE)
        else:
            self.apply_buttons_widget.enable()

        # =====================================================================
        # Get model configuration
        # =====================================================================
        try:
            config = NBFC_CLIENT.get_config()
            fan_temperature_sources = config.get('FanTemperatureSources', [])
            model_config = NBFC_CLIENT.get_model_configuration()
        except Exception as e:
            self.setCurrentWidget(self.error_widget)
            self.error_label.setText(str(e))
            self.fix_button.setEnabled(False)
            self.retry_button.setEnabled(True)
            self.apply_buttons_widget.disable("")
            return

        # =====================================================================
        # Get available temperature sensors
        # =====================================================================
        available_sensors = get_sensors()

        # =====================================================================
        # Fill self.available_temperature_sources with available_sensors
        # =====================================================================
        self.available_temperature_sources.clear()

        sensor_names = set()
        for sensor in available_sensors:
            if sensor.name not in sensor_names:
                sensor_names.add(sensor.name)
                item = QListWidgetItem(sensor.name)
                item.setData(Qt.UserRole, sensor.name)
                self.available_temperature_sources.addItem(item)

        for sensor in available_sensors:
            item = QListWidgetItem("%s (%s)" % (sensor.file, sensor.name))
            item.setData(Qt.UserRole, sensor.file)
            self.available_temperature_sources.addItem(item)

        # =====================================================================
        # Ensure that the FanTemperatureSources in the config are valid.
        # Give the user the chance to fix it or fix it automatically.
        # =====================================================================
        errors = get_fan_temperature_sources_errors(
            fan_temperature_sources,
            len(model_config['FanConfigurations']),
            available_sensors)

        if errors and not fix_errors:
            self.setCurrentWidget(self.error_widget)
            self.error_label.setText('\n\n'.join(errors))
            self.fix_button.setEnabled(True)
            self.retry_button.setEnabled(True)
            self.apply_buttons_widget.disable("")
            return
        elif errors and fix_errors:
            fan_temperature_sources = fix_fan_temperature_sources(
                fan_temperature_sources,
                len(model_config['FanConfigurations']),
                available_sensors)

        self.setCurrentWidget(self.main_widget)

        # =====================================================================
        # Add widgets to self.temperature_sources_layout
        # =====================================================================
        while self.temperature_sources_layout.count() < len(model_config['FanConfigurations']):
            widget = TemperatureSourceWidget(self)
            self.temperature_sources_layout.addWidget(widget)

        while self.temperature_sources_layout.count() > len(model_config['FanConfigurations']):
            widget = self.temperature_sources_layout.itemAt(self.temperature_sources_layout.count() - 1).widget()
            self.temperature_sources_layout.removeWidget(widget)
            widget.deleteLater()

        # =====================================================================
        # Set fan names to widgets
        # =====================================================================
        for i, fan_config in enumerate(model_config['FanConfigurations']):
            widget = self.temperature_sources_layout.itemAt(i).widget()
            widget.setFanName(fan_config.get('FanDisplayName', 'Fan #%d' % i))

        # =====================================================================
        # Update TemperatureSourceWidget 
        # =====================================================================
        for fan_temperature_source in fan_temperature_sources:
            fan_index = fan_temperature_source['FanIndex']
            widget = self.temperature_sources_layout.itemAt(fan_index).widget()

            {
                'Average': widget.average_radio,
                'Max': widget.max_radio,
                'Min': widget.min_radio
            }[fan_temperature_source.get('TemperatureAlgorithmType', 'Average')].setChecked(True)

            widget.temperature_sources.clear()
            for sensor in fan_temperature_source.get('Sensors', []):
                item = self.find_sensor_item(sensor)
                new_item = QListWidgetItem(item.text())
                new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
                widget.temperature_sources.addItem(new_item)

    def get_fan_temperature_sources(self):
        # TODO: maybe set the fan index in widget

        fan_temperature_sources = []
        for i in range(self.temperature_sources_layout.count()):
            widget = self.temperature_sources_layout.itemAt(i).widget()
            fan_json = {'FanIndex': i, 'Sensors': []}

            for j in range(widget.temperature_sources.count()):
                sensor = widget.temperature_sources.item(j).data(Qt.UserRole)
                fan_json['Sensors'].append(sensor)

            if widget.average_radio.isChecked():
                fan_json['TemperatureAlgorithmType'] = 'Average'
            elif widget.max_radio.isChecked():
                fan_json['TemperatureAlgorithmType'] = 'Max'
            elif widget.min_radio.isChecked():
                fan_json['TemperatureAlgorithmType'] = 'Min'

            # If there are no sensors, delete the key
            if not len(fan_json['Sensors']):
                del fan_json['Sensors']

            # If TemperatureAlgorithmType is 'Average' (the default), delete the key
            if fan_json['TemperatureAlgorithmType'] == 'Average':
                del fan_json['TemperatureAlgorithmType']

            # If FanTemperatureSource only has 'FanIndex', don't add it
            if len(fan_json) > 1:
                fan_temperature_sources.append(fan_json)

        return fan_temperature_sources
