class BasicConfigWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Model label
        # =====================================================================

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        label = QLabel("Your laptop model:", self)
        hbox.addWidget(label)

        self.model_name_label = QLabel("", self)
        hbox.addWidget(self.model_name_label)

        # =====================================================================
        # Selected config input + Reset
        # =====================================================================

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        self.selected_config_input = QLineEdit(self)
        self.selected_config_input.textChanged.connect(self.update_apply_buttons)
        self.selected_config_input.setPlaceholderText("Configuration File")
        hbox.addWidget(self.selected_config_input)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_button_clicked)
        hbox.addWidget(self.reset_button)

        # =====================================================================
        # Radio Buttons
        # =====================================================================

        self.list_all_radio = QRadioButton("List all configurations", self)
        self.list_all_radio.clicked.connect(self.list_all_radio_checked)
        layout.addWidget(self.list_all_radio)

        self.list_recommended_radio = QRadioButton("List recommended configurations", self)
        self.list_recommended_radio.clicked.connect(self.list_recommended_radio_checked)
        layout.addWidget(self.list_recommended_radio)

        self.custom_file_radio = QRadioButton("Custom file")
        self.custom_file_radio.clicked.connect(self.custom_file_radio_checked)
        layout.addWidget(self.custom_file_radio)

        # =====================================================================
        # Model selection combo box + Set button
        # =====================================================================

        hbox = QHBoxLayout()

        self.configurations_combobox = QComboBox()
        hbox.addWidget(self.configurations_combobox)

        self.set_button = QPushButton("Set", self)
        self.set_button.clicked.connect(self.set_button_clicked)
        hbox.addWidget(self.set_button)

        layout.addLayout(hbox)

        # =====================================================================
        # File selection
        # =====================================================================

        self.select_file_button = QPushButton("Select file ...", self)
        self.select_file_button.clicked.connect(self.select_file_button_clicked)
        layout.addWidget(self.select_file_button)

        # =====================================================================
        # Stretch
        # =====================================================================

        layout.addStretch()

        # =====================================================================
        # Apply buttons
        # =====================================================================

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.clicked.connect(self.save_button_clicked)
        self.apply_buttons_widget.apply_button.clicked.connect(self.apply_button_clicked)
        layout.addWidget(self.apply_buttons_widget)

        # =====================================================================
        # Initialization
        # =====================================================================

        self.list_all_radio.setChecked(True)
        self.list_all_radio_checked()
        self.update_apply_buttons()

        try:
            self.reset_config()
        except:
            pass

        try:
            model = GLOBALS.nbfc_client.get_model_name()
            self.model_name_label.setText(f"<b>{model}</b>")
        except:
            self.model_name_label.setText("<b>Could not get model name</b>")

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

    def update_apply_buttons(self):
        if not GLOBALS.is_root:
            self.apply_buttons_widget.disable(CANNOT_CONFIGURE_MSG)
        elif not self.selected_config_input.text():
            self.apply_buttons_widget.disable("No model configuration selected")
        else:
            self.apply_buttons_widget.enable()

    def reset_config(self):
        '''
        Reset the `SelectedConfigId` field to its original value.

        This may raise an exception.
        '''

        config = GLOBALS.nbfc_client.get_service_config()

        SelectedConfigId = config.get('SelectedConfigId', '')

        self.selected_config_input.setText(SelectedConfigId)

    def save_config(self):
        '''
        Save the selected configuration to the service configuration file.

        This may raise an exception.
        '''

        config = GLOBALS.nbfc_client.get_service_config()

        old_config = config.get('SelectedConfigId', '')

        config['SelectedConfigId'] = self.selected_config_input.text()

        GLOBALS.nbfc_client.set_service_config(config)

        if old_config != config['SelectedConfigId']:
            GLOBALS.model_config_changed.emit()

    # =========================================================================
    # Signal functions
    # =========================================================================

    def reset_button_clicked(self):
        try:
            self.reset_config()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def save_button_clicked(self):
        try:
            self.save_config()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def apply_button_clicked(self):
        try:
            self.save_config()
            GLOBALS.restart_service.emit(self.apply_buttons_widget.read_only_checkbox.isChecked())
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def update_configuration_combobox(self, available_configs):
        self.configurations_combobox.clear()
        self.configurations_combobox.addItems(available_configs)

        if self.configurations_combobox.count():
            self.set_button.setEnabled(True)
        else:
            self.set_button.setEnabled(False)

    def list_all_radio_checked(self):
        self.select_file_button.setVisible(False)
        self.configurations_combobox.setVisible(True)
        self.set_button.setVisible(True)

        configs = GLOBALS.nbfc_client.list_configs()
        self.update_configuration_combobox(configs)

    def list_recommended_radio_checked(self):
        self.select_file_button.setVisible(False)
        self.configurations_combobox.setVisible(True)
        self.set_button.setVisible(True)

        configs = GLOBALS.nbfc_client.recommended_configs()
        self.update_configuration_combobox(configs)

    def custom_file_radio_checked(self):
        self.select_file_button.setVisible(True)
        self.set_button.setVisible(False)
        self.configurations_combobox.setVisible(False)

    def set_button_clicked(self):
        selected = self.configurations_combobox.currentText()
        if selected:
            self.selected_config_input.setText(selected)

    def select_file_button_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose Configuration File", "", "JSON Files (*.json)")
        if path:
            self.selected_config_input.setText(path)
