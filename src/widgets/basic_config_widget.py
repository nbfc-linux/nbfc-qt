class BasicConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list_all_radio = QRadioButton("List all configurations", self)
        self.list_all_radio.clicked.connect(self.list_all_radio_checked)
        layout.addWidget(self.list_all_radio)

        self.list_recommended_radio = QRadioButton("List recommended configurations", self)
        self.list_recommended_radio.clicked.connect(self.list_recommended_radio_checked)
        layout.addWidget(self.list_recommended_radio)

        self.model_name_label = QLabel("Your laptop model: <b>%s</b>" % NBFC_CLIENT.get_model_name(), self)
        layout.addWidget(self.model_name_label)

        self.configurations_combobox = QComboBox()
        self.configurations_combobox.currentIndexChanged.connect(self.configurations_combobox_changed)
        layout.addWidget(self.configurations_combobox)

        layout.addStretch()

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.apply_button.clicked.connect(self.apply)
        self.apply_buttons_widget.apply_with_restart_button.clicked.connect(self.apply_with_restart)
        layout.addWidget(self.apply_buttons_widget)

        self.list_all_radio.setChecked(True)
        self.list_all_radio_checked()

    def start(self):
        if not IS_ROOT:
            self.apply_buttons_widget.disable(NOT_ROOT_NOTICE)
        elif self.configurations_combobox.currentIndex() == 0:
            self.apply_buttons_widget.disable("No model configuration selected")
        else:
            self.apply_buttons_widget.enable()

    def stop(self):
        pass

    def apply(self):
        config = NBFC_CLIENT.get_config()
        old_config = config.get('SelectedConfigId', '')
        config['SelectedConfigId'] = self.configurations_combobox.currentText()
        NBFC_CLIENT.set_config(config)

        if old_config != config['SelectedConfigId']:
            MODEL_CONFIG_CHANGED.changed.emit()

    def apply_with_restart(self):
        self.apply()
        NBFC_CLIENT.restart(self.apply_buttons_widget.read_only_checkbox.isChecked())

    def update_configuration_combobox(self, configs):
        self.configurations_combobox.clear()
        self.configurations_combobox.addItem("None")
        self.configurations_combobox.addItems(configs)

        config = NBFC_CLIENT.get_config()
        if 'SelectedConfigId' in config:
            selected_config = config['SelectedConfigId']
            for i in range(self.configurations_combobox.count()):
                if self.configurations_combobox.itemText(i) == selected_config:
                    self.configurations_combobox.setCurrentIndex(i)
                    break

    def configurations_combobox_changed(self, index):
        self.start()

    def list_all_radio_checked(self):
        configs = NBFC_CLIENT.list_configs()
        self.update_configuration_combobox(configs)

    def list_recommended_radio_checked(self):
        configs = NBFC_CLIENT.recommended_configs()
        self.update_configuration_combobox(configs)
