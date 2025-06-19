from collections import OrderedDict

class TemperatureThresholdEditWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Up threshold
        # =====================================================================

        l0 = QHBoxLayout()
        layout.addLayout(l0)

        label = QLabel("Up Threshold:", self)
        self.up_threshold_input = QSpinBox(self)
        self.up_threshold_input.setRange(-32768, 32767)

        l0.addWidget(label)
        l0.addWidget(self.up_threshold_input)

        # =====================================================================
        # Down threshold
        # =====================================================================

        l0 = QHBoxLayout()
        layout.addLayout(l0)

        label = QLabel("Down Threshold:", self)
        self.down_threshold_input = QSpinBox(self)
        self.up_threshold_input.setRange(-32768, 32767)

        l0.addWidget(label)
        l0.addWidget(self.down_threshold_input)

        # =====================================================================
        # Fan speed
        # =====================================================================

        l0 = QHBoxLayout()
        layout.addLayout(l0)

        label = QLabel("Fan speed:", self)
        self.fan_speed = QDoubleSpinBox(self)
        self.fan_speed.setRange(0, 100)

        l0.addWidget(label)
        l0.addWidget(self.fan_speed)

    # =========================================================================
    # Public functions
    # =========================================================================

    def set_up_threshold(self, value):
        self.up_threshold_input.setValue(value)

    def set_down_threshold(self, value):
        self.down_threshold_input.setValue(value)

    def set_fan_speed(self, value):
        self.fan_speed.setValue(value)

    def set_all(self, dictionary):
        self.set_up_threshold(dictionary['UpThreshold'])
        self.set_down_threshold(dictionary['DownThreshold'])
        self.set_fan_speed(dictionary['FanSpeed'])

class TemperatureThresholdsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Table
        # =====================================================================

        self.table = MyTableWidget(0, 3)
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(["Up threshold", "Down Threshold", "Fan Speed"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setItemFlagCallback(lambda f: f & ~Qt.ItemIsEditable)

        up_threshold = MyTableFieldDefinition('UpThreshold')
        up_threshold.setDefault(0)
        up_threshold.setDisplay(lambda v: f"{v}°C")
        up_threshold.setTypes((int,))

        down_threshold = MyTableFieldDefinition('DownThreshold')
        down_threshold.setDefault(0)
        down_threshold.setDisplay(lambda v: f"{v}°C")
        down_threshold.setTypes((int,))

        fan_speed = MyTableFieldDefinition('FanSpeed')
        fan_speed.setDefault(0.0)
        fan_speed.setDisplay(lambda v: f"{v}%")
        fan_speed.setTypes((float, int))

        self.table.setColumnFields([
            up_threshold,
            down_threshold,
            fan_speed
        ])

        layout.addWidget(self.table)

        # =====================================================================
        # Buttons
        # =====================================================================

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.up_button = QPushButton("Move up", self)
        self.up_button.clicked.connect(self.up_button_clicked)
        btn_layout.addWidget(self.up_button)

        self.down_button = QPushButton("Move down", self)
        self.down_button.clicked.connect(self.down_button_clicked)
        btn_layout.addWidget(self.down_button)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_button_clicked)
        btn_layout.addWidget(self.add_button)

        self.del_button = QPushButton("Delete", self)
        self.del_button.clicked.connect(self.del_button_clicked)
        btn_layout.addWidget(self.del_button)

        self.set_defaults_button = QPushButton("Set defaults", self)
        self.set_defaults_button.clicked.connect(self.set_defaults_button_clicked)
        btn_layout.addWidget(self.set_defaults_button)

        # =====================================================================
        # Edit
        # =====================================================================

        self.edit = TemperatureThresholdEditWidget()
        self.edit.setVisible(False)
        layout.addWidget(self.edit)

        # =====================================================================
        # Init
        # =====================================================================

        self.table.selectionModel().selectionChanged.connect(self.table_selection_changed)
        self.edit.up_threshold_input.valueChanged.connect(self.up_threshold_changed)
        self.edit.down_threshold_input.valueChanged.connect(self.down_threshold_changed)
        self.edit.fan_speed.valueChanged.connect(self.fan_speed_changed)
        GLOBALS.legacy_temperature_thresholds_behaviour_changed.connect(self.legacy_temperature_thresholds_behaviour_changed)

    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        r = []

        for row in range(self.table.rowCount()):
            r.append(self.table.get_row_as_dict(row))

        return r

    def from_config(self, cfg, trace, errors):
        self.table.clear()

        if 'TemperatureThresholds' not in cfg:
            return

        if not isinstance(cfg['TemperatureThresholds'], list):
            errors.append(trace.get_trace('TemperatureThresholds: Invalid Type'))
            return

        for i, ts_cfg in enumerate(cfg['TemperatureThresholds']):
            with trace.trace(f'TemperatureThresholds[{i}]'):
                if not isinstance(ts_cfg, dict):
                    errors.append(trace.get_trace("Invalid type"))
                    continue

                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.set_row_defaults(row_position)

                for key, error in self.table.update_row(row_position, ts_cfg):
                    with trace.trace(key):
                        if error is KeyError:
                            errors.append(trace.get_trace("Missing key"))
                        elif error is ValueError:
                            errors.append(trace.get_trace("Invalid value"))
                        elif errors is TypeError:
                            errors.append(trace.get_trace("Invalid type"))

        del cfg['TemperatureThresholds']

    # =========================================================================
    # Signals
    # =========================================================================

    def up_threshold_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'UpThreshold': value})

    def down_threshold_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'DownThreshold': value})

    def fan_speed_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'FanSpeed': value})

    def table_selection_changed(self, selected, deselected):
        row = self.table.get_selected_row()
        if row is None:
            self.edit.setVisible(False)
            return

        self.edit.setVisible(True)

        row_as_dict = self.table.get_row_as_dict(row)
        self.edit.set_all(row_as_dict)

    def up_button_clicked(self):
        self.table.move_row_up()

    def down_button_clicked(self):
        self.table.move_row_down()

    def add_button_clicked(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.set_row_defaults(row_position)

    def del_button_clicked(self):
        self.table.remove_selected_row()

    def set_defaults_button_clicked(self):
        widget = self
        while not isinstance(widget, MainWindow):
            widget = widget.parent()

        basic_config_widget = widget.basic
        legacy_temperature_thresholds_behaviour = basic_config_widget.legacy_radio.isChecked()

        if legacy_temperature_thresholds_behaviour:
            self.from_config({'TemperatureThresholds': DEFAULT_LEGACY_TEMPERATURE_THRESHOLDS}, Trace(), [])
        else:
            self.from_config({'TemperatureThresholds': DEFAULT_TEMPERATURE_THRESHOLDS}, Trace(), [])

    def legacy_temperature_thresholds_behaviour_changed(self, enabled):
        config = self.get_config()

        if enabled:
            if config == DEFAULT_TEMPERATURE_THRESHOLDS:
                self.from_config({'TemperatureThresholds': DEFAULT_LEGACY_TEMPERATURE_THRESHOLDS}, Trace(), [])
        else:
            if config == DEFAULT_LEGACY_TEMPERATURE_THRESHOLDS:
                self.from_config({'TemperatureThresholds': DEFAULT_TEMPERATURE_THRESHOLDS}, Trace(), [])
