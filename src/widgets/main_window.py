class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NBFC Client")
        self.resize(400, 400)

        self.tab_widget = QTabWidget(self)

        basic_config_widget = BasicConfigWidget()
        fan_control_widget = FanControlWidget()
        temperature_sources_widget = TemperatureSourcesWidget()

        self.tab_widget.addTab(fan_control_widget, "Fans")
        self.tab_widget.addTab(basic_config_widget, "Basic Configuration")
        self.tab_widget.addTab(temperature_sources_widget, "Temperature Sources")

        self.tab_widget.currentChanged.connect(self.tabChanged)
        self.tabChanged(0)

        self.setCentralWidget(self.tab_widget)

        menuBar = self.menuBar()
        applicationMenu = menuBar.addMenu("&Application")
        quitAction = QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(lambda: QApplication.quit())
        applicationMenu.addAction(quitAction)
        aboutAction = QAction("&About", self)
        aboutAction.triggered.connect(self.showAbout)
        applicationMenu.addAction(aboutAction)

    def showAbout(self):
        QMessageBox.about(self, "About NBFC-Linux", ABOUT_NBFC_LINUX_QT)

    def tabChanged(self, current_index):
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if i == current_index:
                widget.start()
            else:
                widget.stop()

