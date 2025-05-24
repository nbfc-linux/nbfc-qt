class FanWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.fan_index = None

        # =====================================================================
        # Main Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Grid layout
        # =====================================================================

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # =====================================================================
        # Grid content
        # =====================================================================

        label = QLabel("Name", self)
        self.name_label = QLabel("", self)
        grid_layout.addWidget(label, 0, 0)
        grid_layout.addWidget(self.name_label, 0, 1)

        label = QLabel("Temperature", self)
        self.temperature_label = QLabel("", self)
        grid_layout.addWidget(label, 1, 0)
        grid_layout.addWidget(self.temperature_label, 1, 1)

        label = QLabel("Auto mode", self)
        self.auto_mode_label = QLabel("", self)
        grid_layout.addWidget(label, 2, 0)
        grid_layout.addWidget(self.auto_mode_label, 2, 1)

        label = QLabel("Critical", self)
        self.critical_label = QLabel("", self)
        grid_layout.addWidget(label, 3, 0)
        grid_layout.addWidget(self.critical_label, 3, 1)

        label = QLabel("Current speed", self)
        self.current_speed_label = QLabel("", self)
        grid_layout.addWidget(label, 4, 0)
        grid_layout.addWidget(self.current_speed_label, 4, 1)

        label = QLabel("Target speed", self)
        self.target_speed_label = QLabel("", self)
        grid_layout.addWidget(label, 5, 0)
        grid_layout.addWidget(self.target_speed_label, 5, 1)

        label = QLabel("Speed steps", self)
        self.speed_steps_label = QLabel("", self)
        grid_layout.addWidget(label, 6, 0)
        grid_layout.addWidget(self.speed_steps_label, 6, 1)

        # =====================================================================
        # Auto mode Checkbox
        # =====================================================================

        self.auto_mode_checkbox = QCheckBox("Auto mode", self)
        self.auto_mode_checkbox.stateChanged.connect(self.update_fan_speed)
        layout.addWidget(self.auto_mode_checkbox)

        # =====================================================================
        # Slider
        # =====================================================================

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.update_fan_speed)
        layout.addWidget(self.speed_slider)

    def update_fan_speed(self, *_):
        auto_mode = self.auto_mode_checkbox.isChecked()

        if auto_mode:
            GLOBALS.nbfc_client.set_fan_speed('auto', self.fan_index)
        else:
            GLOBALS.nbfc_client.set_fan_speed(self.speed_slider.value(), self.fan_index)

        self.speed_slider.setEnabled(not auto_mode)

    def update(self, fan_index, fan_data):
        self.fan_index = fan_index
        self.name_label.setText(fan_data['Name'])
        self.temperature_label.setText(str(fan_data['Temperature']))
        self.auto_mode_label.setText(str(fan_data['AutoMode']))
        self.critical_label.setText(str(fan_data['Critical']))
        self.current_speed_label.setText(str(fan_data['CurrentSpeed']))
        self.target_speed_label.setText(str(fan_data['TargetSpeed']))
        self.speed_steps_label.setText(str(fan_data['SpeedSteps']))
        self.auto_mode_checkbox.setChecked(fan_data['AutoMode'])
        self.speed_slider.setValue(int(fan_data['RequestedSpeed']))
