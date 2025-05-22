class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Title and Geometry
        # =====================================================================

        self.setWindowTitle("NBFC Client")
        self.resize(400, 400)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.tab_widget = QTabWidget(self)

        # =====================================================================
        # Tabs
        # =====================================================================

        self.widgets = {}
        self.widgets['service'] = ServiceControlWidget()
        self.widgets['fans']    = FanControlWidget()
        self.widgets['basic']   = BasicConfigWidget()
        self.widgets['sensors'] = TemperatureSourcesWidget()
        self.widgets['update']  = UpdateWidget()

        self.tab_widget.addTab(self.widgets['service'], "Service")
        self.tab_widget.addTab(self.widgets['fans'],    "Fans")
        self.tab_widget.addTab(self.widgets['basic'],   "Basic Configuration")
        self.tab_widget.addTab(self.widgets['sensors'], "Sensors")
        self.tab_widget.addTab(self.widgets['update'],  "Update")

        self.tab_widget.currentChanged.connect(self.tab_widget_changed)
        self.tab_widget_changed(0)

        # =====================================================================
        # Set widget
        # =====================================================================

        self.setCentralWidget(self.tab_widget)

        # =====================================================================
        # Menu
        # =====================================================================

        menuBar = self.menuBar()
        applicationMenu = menuBar.addMenu("&Application")

        aboutAction = QAction("&About", self)
        aboutAction.triggered.connect(self.about_menu_clicked)
        applicationMenu.addAction(aboutAction)

        quitAction = QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(lambda: QApplication.quit())
        applicationMenu.addAction(quitAction)

    # =========================================================================
    # Public functions
    # =========================================================================

    def setTabById(self, id_):
        self.tab_widget.setCurrentWidget(self.widgets[id_])

    # =========================================================================
    # Signal functions
    # =========================================================================

    def about_menu_clicked(self):
        QMessageBox.about(self, "About NBFC-Linux", ABOUT_NBFC_LINUX)

    def tab_widget_changed(self, current_index):
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if i == current_index:
                widget.start()
            else:
                widget.stop()
