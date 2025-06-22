import subprocess

class ImageLoaderWorker(QObject):
    finished = pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            import requests

            response = requests.get(self.url)
            response.raise_for_status()

            self.finished.emit(response.content)
        except Exception:
            pass

class SponsorWidget(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setVisible(False)
        self.setMaximumHeight(100)
        self.setAlignment(Qt.AlignCenter)

        try:
            sponsor = GLOBALS.nbfc_client.get_model_configuration()['Sponsor']
            self.url = sponsor['URL']

            if 'Description' in sponsor:
                self.setToolTip(f"{sponsor['Name']} - {sponsor['Description']}")
            else:
                self.setToolTip(sponsor['Name'])

            self.thread = QThread()
            self.worker = ImageLoaderWorker(sponsor['BannerURL'])
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_image_loaded)
            self.worker.finished.connect(self.thread.quit)
            self.thread.start()
        except Exception:
            pass
        
    def on_image_loaded(self, content):
        pixmap = QPixmap()
        pixmap.loadFromData(content)
        pixmap = pixmap.scaledToHeight(100, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setVisible(True)

    def mousePressEvent(self, event):
        if self.url:
            subprocess.run(['xdg-open', self.url])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Title and Geometry
        # =====================================================================

        self.setWindowTitle("NBFC Client")
        self.resize(400, 400)

        # =====================================================================
        # Container widget
        # =====================================================================

        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # =====================================================================
        # Sponsor widget
        # =====================================================================

        sponsor_widget = SponsorWidget(self)
        layout.addWidget(sponsor_widget)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

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

        self.setCentralWidget(container)

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
