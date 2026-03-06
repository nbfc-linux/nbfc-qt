#define RECOMMENDED_THRESHOLD_MIN 9.0

def RegisterType_To_HumanReadable(s):
    if s == 'FanReadRegister':
        return 'Fan read register'

    if s == 'FanWriteRegister':
        return 'Fan write register'

    if s == 'RegisterWriteConfigurationRegister':
        return 'Misc register'

    return '?'

def RegisterScore_To_HumanReadable(s):
    if s == 'FullMatch':
        return 'FULL MATCH'

    if s == 'PartialMatch':
        return 'PARTIAL MATCH'

    if s == 'MinimalMatch':
        return 'MINIMAL MATCH'

    if s == 'NoMatch':
        return 'NO MATCH'

    if s == 'NotFound':
        return 'NOT FOUND'

    if s == 'BadRegister':
        return 'BAD REGISTER'

    return '?'

def MethodScore_To_HumanReadable(s):
    if s == 'Found':
        return 'FOUND'

    if s == 'NotFound':
        return 'NOT FOUND'

    return '?'

class RegisterRating(QWidget):
    def __init__(self, data):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # =====================================================================
        # Info
        # =====================================================================

        off = data['offset']
        grid_layout.addWidget(QLabel("Register Offset"),        0, 0)
        grid_layout.addWidget(QLabel("%d (0x%X)" % (off, off)), 0, 1)

        typ = RegisterType_To_HumanReadable(data['type'])
        grid_layout.addWidget(QLabel("Type"), 1, 0)
        grid_layout.addWidget(QLabel(typ),    1, 1)

        score = RegisterScore_To_HumanReadable(data['score'])
        grid_layout.addWidget(QLabel("Score"), 2, 0)
        grid_layout.addWidget(QLabel(score),   2, 1)

        if 'info' in data:
            name = data['info']['name']
            grid_layout.addWidget(QLabel("Name"), 3, 0)
            grid_layout.addWidget(QLabel(name),   3, 1)

class MethodRating(QWidget):
    def __init__(self, data):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # =====================================================================
        # Info
        # =====================================================================

        call = data['call']
        grid_layout.addWidget(QLabel("Method call"), 0, 0)
        grid_layout.addWidget(QLabel(call),          0, 1)

        score = MethodScore_To_HumanReadable(data['score'])
        grid_layout.addWidget(QLabel("Score"), 1, 0)
        grid_layout.addWidget(QLabel(score),   1, 1)

class RateConfigDetails(QWidget):
    def __init__(self, data):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Register ratings
        # =====================================================================

        for rating in data['rating']['register_ratings']:
            layout.addWidget(RegisterRating(rating))

        # =====================================================================
        # Method ratings
        # =====================================================================

        for rating in data['rating']['method_ratings']:
            layout.addWidget(MethodRating(rating))

class RateConfigDetailsWindow(QWidget):
    def __init__(self, data):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Score
        # =====================================================================

        label = QLabel("Score: %.2f / 10" % data['rating']['score'], self)
        layout.addWidget(label)

        # =====================================================================
        # Files
        # =====================================================================

        self.files_combobox = QComboBox()
        self.files_combobox.addItems(data['files'])
        layout.addWidget(self.files_combobox)

        # =====================================================================
        # ScrollArea
        # =====================================================================

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # =====================================================================
        # RateConfigDetails
        # =====================================================================

        self.rate_config_details = RateConfigDetails(data)
        self.scroll_area.setWidget(self.rate_config_details)

        # =====================================================================
        # Apply buttons widget
        # =====================================================================

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.clicked.connect(self.save_button_clicked)
        self.apply_buttons_widget.apply_button.clicked.connect(self.apply_button_clicked)
        self.apply_buttons_widget.enable()
        layout.addWidget(self.apply_buttons_widget)

    # =========================================================================
    # Signal functions
    # =========================================================================

    def save_button_clicked(self):
        selected_config = self.files_combobox.currentText()
        GLOBALS.set_model_config(selected_config)

    def apply_button_clicked(self):
        selected_config = self.files_combobox.currentText()
        read_only = self.apply_buttons_widget.read_only_checkbox.isChecked()
        GLOBALS.set_model_config_and_restart(selected_config, read_only)

class RateConfigsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.configs = []

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Threshold spin box + Load button + Help button
        # =====================================================================

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        self.threshold_label = QLabel("Minimum score")

        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(0.0, 10.0)
        self.threshold_spin.setDecimals(2)
        self.threshold_spin.setSingleStep(0.10)
        self.threshold_spin.setValue(RECOMMENDED_THRESHOLD_MIN)
        self.threshold_spin.valueChanged.connect(self.threshold_spin_changed)

        self.load_button = QPushButton("Load configs")
        self.load_button.clicked.connect(self.load_button_clicked)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.help_button_clicked)

        hbox.addWidget(self.threshold_label)
        hbox.addWidget(self.threshold_spin)
        hbox.addWidget(self.load_button)
        hbox.addWidget(self.help_button)

        # =====================================================================
        # Warning label
        # =====================================================================

        self.warning_label = QLabel("Warning! Unsafe configurations are shown")
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet("""
            background-color: #cc0000;
            color: white;
            font-weight: bold""")
        self.warning_label.setVisible(False)
        layout.addWidget(self.warning_label)

        # =====================================================================
        # Rated Configs
        # =====================================================================

        self.rated_configs_list = QListWidget(self)
        self.rated_configs_list.currentItemChanged.connect(self.rate_configs_item_changed)
        self.rated_configs_list.itemActivated.connect(self.rate_configs_item_activated)
        layout.addWidget(self.rated_configs_list)

        # =====================================================================
        # Buttons
        # =====================================================================

        button_layout = QHBoxLayout()
        self.show_button = QPushButton("Show Details", self)
        self.show_button.clicked.connect(self.show_button_clicked)
        self.show_button.setEnabled(False)
        button_layout.addWidget(self.show_button)
        layout.addLayout(button_layout)

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        pass

    def stop(self):
        pass

    # =========================================================================
    # Helper functions
    # =========================================================================

    def load_rated_configs_list(self):
        try:
            configs = GLOBALS.nbfc_client.rate_configs()
        except NbfcClientError as e:
            show_error_message(self, "Error", str(e))
            return

        configs = sorted(configs, key=lambda o: o['rating']['priority'], reverse=True)
        configs = sorted(configs, key=lambda o: o['rating']['score'], reverse=True)
        self.configs = configs
        self.show_rated_configs_list()

    def show_rated_configs_list(self):
        self.rated_configs_list.clear()
        min_score = self.threshold_spin.value()

        for data in self.configs:
            if data['rating']['score'] < min_score:
                continue

            item = QListWidgetItem('%s (%.2f / 10)' % (data['files'][0], data['rating']['score']))
            self.rated_configs_list.addItem(item)

    def show_details(self, data):
        self.details_widget = RateConfigDetailsWindow(data)
        self.details_widget.setWindowTitle("Rating Details")
        self.details_widget.resize(400, 400)
        self.details_widget.show()

    # =========================================================================
    # Signal functions
    # =========================================================================

    def rate_configs_item_changed(self, current, previous):
        self.show_button.setEnabled(bool(current))

    def rate_configs_item_activated(self, item):
        self.show_details(self.configs[self.rated_configs_list.row(item)])

    def load_button_clicked(self):
        self.load_rated_configs_list()

    def help_button_clicked(self):
        self.help_widget = RateConfigsHelpWidget()
        self.help_widget.show()

    def threshold_spin_changed(self):
        self.warning_label.setVisible(self.threshold_spin.value() < RECOMMENDED_THRESHOLD_MIN)
        self.show_rated_configs_list()

    def show_button_clicked(self):
        cur = self.rated_configs_list.currentRow()
        if cur == -1:
            return

        self.show_details(self.configs[cur])
