from collections import OrderedDict

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Data
        # =====================================================================

        self.file_path = None

        # =====================================================================
        # Title and Geometry
        # =====================================================================

        self.setWindowTitle("NBFC Config Editor")
        self.resize(500, 400)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.tab_widget = QTabWidget(self)

        # =====================================================================
        # Tabs
        # =====================================================================

        self.basic                         = BasicConfigWidget()
        self.fans                          = FanConfigurationsWidget()
        self.register_write_configurations = RegisterWriteConfigurationsWidget()

        self.tab_widget.addTab(self.basic,                         "Basic Configuration")
        self.tab_widget.addTab(self.fans,                          "Fan Configurations")
        self.tab_widget.addTab(self.register_write_configurations, "Register write configurations")

        # =====================================================================
        # Set widget
        # =====================================================================

        self.setCentralWidget(self.tab_widget)

        # =====================================================================
        # Menu
        # =====================================================================

        menuBar = self.menuBar()

        # Application menu ====================================================
        applicationMenu = menuBar.addMenu("&Application")

        aboutAction = QAction("&About", self)
        aboutAction.triggered.connect(self.about_menu_clicked)
        applicationMenu.addAction(aboutAction)

        quitAction = QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.quit_menu_clicked)
        applicationMenu.addAction(quitAction)

        # File menu ===========================================================
        fileMenu = menuBar.addMenu("&File")

        importAction = QAction("&Import", self)
        importAction.triggered.connect(self.import_menu_clicked)
        fileMenu.addAction(importAction)

        saveAction = QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save_menu_clicked)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("&Save as", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.triggered.connect(self.save_as_menu_clicked)
        fileMenu.addAction(saveAsAction)

    # =========================================================================
    # Helper functions
    # =========================================================================

    def get_config(self):
        r = OrderedDict()

        basic_cfg                     = self.basic.get_config()
        fan_configurations            = self.fans.get_config()
        register_write_configurations = self.register_write_configurations.get_config()

        order = [
            'LegacyTemperatureThresholdsBehaviour',
            'NotebookModel',
            'Author',
            'EcPollInterval',
            'CriticalTemperature',
            'CriticalTemperatureOffset',
            'ReadWriteWords',
        ]

        for key in order:
            r[key] = basic_cfg[key]

        r['FanConfigurations'] = fan_configurations

        r['RegisterWriteConfigurations'] = register_write_configurations

        if not r['RegisterWriteConfigurations']:
            del r['RegisterWriteConfigurations']

        return r

    def from_config(self, config, trace, errors):
        self.basic.from_config(config, trace, errors)
        self.fans.from_config(config, trace, errors)
        self.register_write_configurations.from_config(config, trace, errors)

    def import_file(self, file):
        try:
            with open(file, 'r', encoding='UTF-8') as fh:
                cfg = json.load(fh)
        except Exception as e:
            show_error_message(self, "Error", str(e))
            return

        trace = Trace()
        errors = []

        with trace.trace(file):
            self.from_config(cfg, trace, errors)

        if errors:
            errmsg =  'Errors were encountered while importing the configuration.\n\n'
            errmsg += 'The configuration can still be edited despite these errors:\n\n'
            errmsg += '\n\n'.join(errors)
            show_error_message(self, "Error while importing file", errmsg)

    def save_file(self, file):
        cfg = self.get_config()

        try:
            with open(file, 'w', encoding='UTF-8') as fh:
                json.dump(cfg, fh, indent=4)
        except Exception as e:
            show_error_message(self, "Error", str(e))

    # =========================================================================
    # Signal functions
    # =========================================================================

    def about_menu_clicked(self):
        QMessageBox.about(self, "About NBFC-Linux", ABOUT_NBFC_LINUX)

    def quit_menu_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Do you really want to quit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()

    def import_menu_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose Configuration File", "", "JSON Files (*.json)")
        if not path:
            return

        self.import_file(path)

    def save_menu_clicked(self):
        if not self.file_path:
            self.save_as_menu_clicked()
        else:
            self.save_file(self.file_path)

    def save_as_menu_clicked(self):
        path, _ = QFileDialog.getSaveFileName(self, "Choose Configuration File", "", "JSON Files (*.json)")
        if not path:
            return

        self.file_path = path
        self.save_file(self.file_path)
