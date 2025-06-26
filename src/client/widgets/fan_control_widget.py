class FanControlWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Timer
        # =====================================================================

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)

        # =====================================================================
        # Error Widget
        # =====================================================================

        self.error_widget = QWidget()
        error_layout = QVBoxLayout()
        self.error_widget.setLayout(error_layout)
        self.error_label = QLabel("", self)
        error_layout.addWidget(self.error_label)
        self.addWidget(self.error_widget)

        # =====================================================================
        # Contents (QScrollArea)
        # =====================================================================

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.addWidget(self.scroll_area)

        fans_widget = QWidget()
        self.scroll_area.setWidget(fans_widget)

        fans_container = QVBoxLayout()
        fans_widget.setLayout(fans_container)

        self.fans_layout = QVBoxLayout()
        fans_container.addLayout(self.fans_layout)
        fans_container.addStretch()

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        self.update()
        self.timer.start()

    def stop(self):
        self.timer.stop()

    # =========================================================================
    # Helper functions
    # =========================================================================

    def update(self):
        try:
            status = GLOBALS.nbfc_client.get_status()
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
