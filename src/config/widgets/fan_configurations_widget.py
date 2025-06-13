class FanConfigurationsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_close_clicked)
        self.tab_widget.tabBar().tabMoved.connect(self.tab_moved)
        layout.addWidget(self.tab_widget)

        # =====================================================================
        # Button
        # =====================================================================

        add_widget = QWidget()
        add_layout = QHBoxLayout()
        add_layout.setContentsMargins(4, 4, 4, 4)
        add_widget.setLayout(add_layout)

        self.add_button = QPushButton("", self)
        self.add_button.setText("Add fan")
        self.add_button.clicked.connect(self.add_button_clicked)
        add_layout.addWidget(self.add_button)

        self.tab_widget.setCornerWidget(add_widget)

        # =====================================================================
        # Fan widget
        # =====================================================================

        widget = FanConfigurationWidget()
        self.tab_widget.addTab(widget, "Fan 1")

    # =========================================================================
    # Public methods
    # =========================================================================

    def get_config(self):
        r = []

        for i in range(self.tab_widget.count()):
            r.append(self.tab_widget.widget(i).get_config())

        return r

    def from_config(self, cfg, trace, errors):
        self.tab_widget.clear()

        if 'FanConfigurations' not in cfg:
            widget = FanConfigurationWidget()
            self.tab_widget.addTab(widget, "Fan 1")
            return

        if not isinstance(cfg['FanConfigurations'], list):
            errors.append(trace.get_trace('FanConfigurations: Invalid type'))
            return

        for i, fan_cfg in enumerate(cfg['FanConfigurations']):
            with trace.trace(f'FanConfigurations[{i}]'):
                widget = FanConfigurationWidget()
                self.tab_widget.addTab(widget, "Fan %i" % (i + 1))
                widget.from_config(fan_cfg, trace, errors)

        del cfg['FanConfigurations']

    # =========================================================================
    # Helper functions
    # =========================================================================

    def rename_tabs(self):
        for i in range(self.tab_widget.count()):
            self.tab_widget.setTabText(i, "Fan %i" % (i + 1))

    # =========================================================================
    # Signals
    # =========================================================================

    def add_button_clicked(self):
        widget = FanConfigurationWidget()
        self.tab_widget.addTab(widget, "Fan %i" % (self.tab_widget.count() + 1))

    def tab_close_clicked(self, index):
        reply = QMessageBox.question(self, "Close fan tab", "Do you really want to delete this fan?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply != QMessageBox.Yes:
            return

        self.tab_widget.removeTab(index)
        self.rename_tabs()

    def tab_moved(self, from_index, to_index):
        self.rename_tabs()
