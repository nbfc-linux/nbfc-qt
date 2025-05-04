class FanControlWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)

        self.error_widget = QWidget()
        error_layout = QVBoxLayout()
        self.error_widget.setLayout(error_layout)
        self.error_label = QLabel("", self)
        error_layout.addWidget(self.error_label)
        self.addWidget(self.error_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        fans_widget = QWidget()
        self.fans_layout = QVBoxLayout()
        fans_widget.setLayout(self.fans_layout)
        self.scroll_area.setWidget(fans_widget)
        self.addWidget(self.scroll_area)

    def start(self):
        self.update()
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def update(self):
        try:
            status = NBFC_CLIENT.get_status()
            self.setCurrentWidget(self.scroll_area)
        except Exception as e:
            self.error_label.setText(str(e))
            self.setCurrentWidget(self.error_widget)
            return

        while self.fans_layout.count() < len(status['Fans']):
            widget = FanWidget()
            self.fans_layout.addWidget(widget)

        while self.fans_layout.count() > len(status['Fans']):
            widget = self.fans_layout.itemAt(self.fans_layout.count() - 1).widget()
            self.fans_layout.removeWidget(widget)
            widget.deleteLater()

        for fan_index, fan_data in enumerate(status['Fans']):
            widget = self.fans_layout.itemAt(fan_index).widget()
            widget.update(fan_index, fan_data)

