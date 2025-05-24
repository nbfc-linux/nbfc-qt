class TemperatureSourceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.fan_index = None

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Algorithm type
        # =====================================================================

        algorithm_label = QLabel("Algorithm:", self)
        layout.addWidget(algorithm_label)

        algorithm_layout = QHBoxLayout()
        self.default_radio = QRadioButton("Default", self)
        self.average_radio = QRadioButton("Average", self)
        self.max_radio = QRadioButton("Max", self)
        self.min_radio = QRadioButton("Min", self)
        algorithm_layout.addWidget(self.default_radio)
        algorithm_layout.addWidget(self.average_radio)
        algorithm_layout.addWidget(self.max_radio)
        algorithm_layout.addWidget(self.min_radio)
        self.default_radio.setChecked(True)
        layout.addLayout(algorithm_layout)

        # =====================================================================
        # Temperature Sources
        # =====================================================================

        temperature_sources_label = QLabel("Temperature Sources", self)
        layout.addWidget(temperature_sources_label)

        self.temperature_sources = QListWidget(self)
        layout.addWidget(self.temperature_sources)

        # =====================================================================
        # Sensors
        # =====================================================================

        self.sensors = QComboBox(self)
        self.sensors.currentIndexChanged.connect(self.sensors_changed)
        layout.addWidget(self.sensors)

        # =====================================================================
        # Custom sensor
        # =====================================================================

        self.custom_sensor = QLineEdit(self)
        self.custom_sensor.setVisible(False)
        layout.addWidget(self.custom_sensor)

        # =====================================================================
        # Buttons
        # =====================================================================

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add", self)
        self.del_button = QPushButton("Delete", self)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.del_button.clicked.connect(self.del_button_clicked)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.del_button)
        layout.addLayout(button_layout)

    def set_fan_index(self, index):
        self.fan_index = index

    def set_available_sensors(self, available_sensors):
        for sensor in available_sensors:
            self.sensors.addItem("%s (%s)" % (sensor.name, sensor.description), sensor.name)

        self.sensors.addItem("Custom Shell Command",  "<command>")
        self.sensors.addItem("Custom Sensor or File", "<custom>")

    def update(self, fan_temperature_source):
        {
            'Default': self.default_radio,
            'Average': self.average_radio,
            'Max':     self.max_radio,
            'Min':     self.min_radio
        }[fan_temperature_source.get('TemperatureAlgorithmType', 'Default')].setChecked(True)

        self.temperature_sources.clear()

        for sensor in fan_temperature_source.get('Sensors', []):
            try:
                item = self.find_sensor_item(sensor)
                new_item = QListWidgetItem(item.text())
                new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
            except:
                new_item = QListWidgetItem(sensor)
                new_item.setData(Qt.UserRole, sensor)

            self.temperature_sources.addItem(new_item)

    def find_sensor_item(self, sensor):
        for i in range(self.sensors.count()):
            item = self.sensors.item(i)
            if item.data(Qt.UserRole) == sensor:
                return item

        raise Exception('No sensor found for %s' % sensor)

    def sensors_changed(self, index):
        data  = self.sensors.itemData(index, Qt.UserRole)

        if data == '<custom>':
            self.custom_sensor.setVisible(True)
            self.custom_sensor.setPlaceholderText("Sensor Name or File")
        elif data == '<command>':
            self.custom_sensor.setVisible(True)
            self.custom_sensor.setPlaceholderText("Shell Command")
        else:
            self.custom_sensor.setVisible(False)

    def add_button_clicked(self):
        index = self.sensors.currentIndex()
        text  = self.sensors.itemText(index)
        data  = self.sensors.itemData(index, Qt.UserRole)

        if data == '<custom>':
            text = self.custom_sensor.text()
            if not text.strip():
                return

            data = text
        elif data == '<command>':
            text = '$ %s' % self.custom_sensor.text()
            if not text.strip():
                return

            data = text

        new_item = QListWidgetItem(text)
        new_item.setData(Qt.UserRole, data)
        self.temperature_sources.addItem(new_item)

    def del_button_clicked(self):
        self.temperature_sources.takeItem(self.temperature_sources.currentRow())

    def get_config(self):
        sensors = []
        for i in range(self.temperature_sources.count()):
            sensor = self.temperature_sources.item(i).data(Qt.UserRole)
            sensors.append(sensor)

        algorithm = None
        if self.average_radio.isChecked():
            algorithm = 'Average'
        elif self.max_radio.isChecked():
            algorithm = 'Max'
        elif self.min_radio.isChecked():
            algorithm = 'Min'

        cfg = {'FanIndex': self.fan_index}

        if algorithm:
            cfg['TemperatureAlgorithmType'] = algorithm

        if sensors:
            cfg['Sensors'] = sensors

        return cfg
