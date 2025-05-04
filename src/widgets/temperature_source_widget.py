class TemperatureSourceWidget(QGroupBox):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        algorithm_layout = QHBoxLayout()
        self.average_radio = QRadioButton("Average", self)
        self.max_radio = QRadioButton("Max", self)
        self.min_radio = QRadioButton("Min", self)
        algorithm_layout.addWidget(self.average_radio)
        algorithm_layout.addWidget(self.max_radio)
        algorithm_layout.addWidget(self.min_radio)
        self.average_radio.setChecked(True)
        layout.addLayout(algorithm_layout)

        self.temperature_sources = QListWidget(self)
        layout.addWidget(self.temperature_sources)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add", self)
        self.del_button = QPushButton("Delete", self)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.del_button.clicked.connect(self.del_button_clicked)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.del_button)
        layout.addLayout(button_layout)

    def setFanName(self, name):
        self.setTitle(name)

    def add_button_clicked(self):
        item = self.parent.available_temperature_sources.currentItem()
        if item:
            new_item = QListWidgetItem(item.text())
            new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
            self.temperature_sources.addItem(new_item)

    def del_button_clicked(self):
        self.temperature_sources.takeItem(self.temperature_sources.currentRow())
