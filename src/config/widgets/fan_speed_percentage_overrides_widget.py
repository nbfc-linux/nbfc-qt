from collections import OrderedDict

class FanSpeedPercentageOverrideEditWidget(QWidget):
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

        label = QLabel("Fan speed value:", self)
        self.fan_speed_value = QSpinBox(self)
        self.fan_speed_value.setRange(0, UINT16_MAX) # TODO: may be byte

        l0.addWidget(label)
        l0.addWidget(self.fan_speed_value)

        # =====================================================================
        # Down threshold
        # =====================================================================

        l0 = QHBoxLayout()
        layout.addLayout(l0)

        label = QLabel("Fan speed percentage:", self)
        self.fan_speed_percentage = QDoubleSpinBox(self)
        self.fan_speed_percentage.setRange(0, 100)

        l0.addWidget(label)
        l0.addWidget(self.fan_speed_percentage)

        # =====================================================================
        # Fan speed
        # =====================================================================

        l0 = QHBoxLayout()
        layout.addLayout(l0)

        label = QLabel("Applied to:", self)
        self.target_operation_input = QComboBox(self)
        self.target_operation_input.addItems(["Read", "Write", "ReadWrite"])

        l0.addWidget(label)
        l0.addWidget(self.target_operation_input)

    # =========================================================================
    # Public functions
    # =========================================================================

    def set_fan_speed(self, value):
        self.fan_speed_value.setValue(value)

    def set_fan_percentage(self, value):
        self.fan_speed_percentage.setValue(value)

    def set_target_operation(self, value):
        self.target_operation_input.setCurrentText(value)

    def set_all(self, dictionary):
        self.set_fan_speed(dictionary['FanSpeedValue'])
        self.set_fan_percentage(dictionary['FanSpeedPercentage'])
        self.set_target_operation(dictionary['TargetOperation'])

class FanSpeedPercentageOverrides(QWidget):
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
        self.table.setHorizontalHeaderLabels(["Fan speed value", "Fan speed percentage", "Applied to"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setItemFlagCallback(lambda f: f & ~Qt.ItemIsEditable)

        fan_speed_value_column = MyTableFieldDefinition('FanSpeedValue')
        fan_speed_value_column.setTypes((int,))
        fan_speed_value_column.setDefault(0)

        fan_speed_percentage_column = MyTableFieldDefinition('FanSpeedPercentage')
        fan_speed_percentage_column.setTypes((float, int))
        fan_speed_percentage_column.setDefault(0.0)
        fan_speed_percentage_column.setDisplay(lambda v: f'{v}%')

        target_operation_column = MyTableFieldDefinition('TargetOperation')
        target_operation_column.setDefault('ReadWrite')
        target_operation_column.setValidate(lambda v: v in ('Read', 'Write', 'ReadWrite'))

        self.table.setColumnFields([
            fan_speed_value_column,
            fan_speed_percentage_column,
            target_operation_column
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

        # =====================================================================
        # Edit
        # =====================================================================

        self.edit = FanSpeedPercentageOverrideEditWidget()
        self.edit.setVisible(False)
        layout.addWidget(self.edit)

        # =====================================================================
        # Init
        # =====================================================================

        self.table.selectionModel().selectionChanged.connect(self.table_selection_changed)
        self.edit.fan_speed_value.valueChanged.connect(self.fan_speed_value_changed)
        self.edit.fan_speed_percentage.valueChanged.connect(self.fan_speed_percentage_changed)
        self.edit.target_operation_input.currentTextChanged.connect(self.target_operation_changed)

    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        r = []

        for row in range(self.table.rowCount()):
            r.append(self.table.get_row_as_dict(row))

        return r

    def from_config(self, cfg, trace, errors):
        if 'FanSpeedPercentageOverrides' not in cfg:
            return

        if not isinstance(cfg['FanSpeedPercentageOverrides'], list):
            errors.append(trace.get_trace('FanSpeedPercentageOverrides: Invalid type'))
            return

        for i, fspo_cfg in enumerate(cfg['FanSpeedPercentageOverrides']):
            with trace.trace(f'FanSpeedPercentageOverrides[{i}]'):
                if not isinstance(fspo_cfg, dict):
                    errors.append(trace.get_trace('Invalid type'))
                    continue

                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.set_row_defaults(row_position)

                for key, error in self.table.update_row(row_position, fspo_cfg):
                    with trace.trace(key):
                        if error is KeyError:
                            if key != 'TargetOperation':
                                errors.append(trace.get_trace("Missing field"))
                        if error is ValueError:
                            errors.append(trace.get_trace("Invalid value"))
                        if error is TypeError:
                            errors.append(trace.get_trace("Invalid type"))

        del cfg['FanSpeedPercentageOverrides']

    # =========================================================================
    # Signals
    # =========================================================================

    def fan_speed_value_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'FanSpeedValue': value})

    def fan_speed_percentage_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'FanSpeedPercentage': value})

    def target_operation_changed(self, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {'TargetOperation': value})

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
