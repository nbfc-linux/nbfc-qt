class TemperatureSourcesWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        GLOBALS.model_config_changed.connect(self.setup_ui)

        # =====================================================================
        # Error Widget
        # =====================================================================

        self.error_widget = QWidget()

        error_layout = QVBoxLayout()
        self.error_widget.setLayout(error_layout)

        self.error_label = QLabel("", self)
        error_layout.addWidget(self.error_label)

        button_layout = QHBoxLayout()
        error_layout.addLayout(button_layout)

        self.retry_button = QPushButton("Retry", self)
        self.retry_button.clicked.connect(self.retry_button_clicked)
        button_layout.addWidget(self.retry_button)

        self.fix_button = QPushButton("Fix errors automatically", self)
        self.fix_button.clicked.connect(self.fix_button_clicked)
        button_layout.addWidget(self.fix_button)

        self.addWidget(self.error_widget)

        # =====================================================================
        # Main Widget
        # =====================================================================

        self.main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.main_widget.setLayout(main_layout)

        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.clicked.connect(self.save_button_clicked)
        self.apply_buttons_widget.apply_button.clicked.connect(self.apply_button_clicked)
        main_layout.addWidget(self.apply_buttons_widget)
        self.addWidget(self.main_widget)

        self.setup_ui()

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        pass

    def stop(self):
        pass

    # =========================================================================
    # Helper functions
    # =========================================================================

    def save(self):
        config = GLOBALS.nbfc_client.get_service_config()
        config['FanTemperatureSources'] = self.get_fan_temperature_sources()
        if not len(config['FanTemperatureSources']):
            del config['FanTemperatureSources']
        GLOBALS.nbfc_client.set_service_config(config)

    def setup_ui(self, fix_errors=False):
        if not GLOBALS.is_root:
            self.apply_buttons_widget.disable(CANNOT_CONFIGURE_MSG)
        else:
            self.apply_buttons_widget.enable()

        # =====================================================================
        # Get model configuration
        # =====================================================================

        try:
            config = GLOBALS.nbfc_client.get_service_config()
            fan_temperature_sources = config.get('FanTemperatureSources', [])
            model_config = GLOBALS.nbfc_client.get_model_configuration()
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

        available_sensors = GLOBALS.nbfc_client.get_available_sensors()

        # =====================================================================
        # Ensure that the FanTemperatureSources in the config are valid.
        # Give the user the chance to fix it or fix it automatically.
        # =====================================================================

        errors = validate_fan_temperature_sources(
            fan_temperature_sources,
            len(model_config['FanConfigurations']))

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
                len(model_config['FanConfigurations']))

        self.setCurrentWidget(self.main_widget)

        # =====================================================================
        # Add widgets to self.tab_widget
        # =====================================================================

        while self.tab_widget.count() < len(model_config['FanConfigurations']):
            widget = TemperatureSourceWidget()
            self.tab_widget.addTab(widget, "")

        while self.tab_widget.count() > len(model_config['FanConfigurations']):
            last_index = self.tab_widget.count() - 1
            widget = self.tab_widget.widget(last_index)
            self.tab_widget.removeTab(last_index)
            widget.deleteLater()

        # =====================================================================
        # Set fan names to tabs
        # =====================================================================

        for i, fan_config in enumerate(model_config['FanConfigurations']):
            widget = self.tab_widget.widget(i)
            self.tab_widget.setTabText(i, fan_config.get('FanDisplayName', 'Fan #%d' % i))
            widget.set_available_sensors(available_sensors)
            widget.set_fan_index(i)

        # =====================================================================
        # Update TemperatureSourceWidget 
        # =====================================================================

        for fan_temperature_source in fan_temperature_sources:
            fan_index = fan_temperature_source['FanIndex']
            widget = self.tab_widget.widget(fan_index)
            widget.update(fan_temperature_source)

    def get_fan_temperature_sources(self):
        fan_temperature_sources = []

        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            config = widget.get_config()

            # If FanTemperatureSource only has 'FanIndex', don't add it
            if len(config) > 1:
                fan_temperature_sources.append(config)

        return fan_temperature_sources

    # =========================================================================
    # Signal functions
    # =========================================================================

    def save_button_clicked(self):
        try:
            self.save()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def apply_button_clicked(self):
        try:
            self.save()
            GLOBALS.restart_service.emit(self.apply_buttons_widget.read_only_checkbox.isChecked())
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def fix_button_clicked(self):
        self.setup_ui(fix_errors=True)

    def retry_button_clicked(self):
        self.setup_ui(fix_errors=False)
