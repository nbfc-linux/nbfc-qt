from collections import OrderedDict

class RegisterWriteConfigurationEdit(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # GridLayout
        # =====================================================================

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # =====================================================================
        # Description
        # =====================================================================

        label = QLabel("Description:", self)
        self.description_input = QLineEdit(self)

        grid_layout.addWidget(label, 0, 0)
        grid_layout.addWidget(self.description_input, 0, 1)

        # =====================================================================
        # Write occasion
        # =====================================================================

        label = QLabel("Write occasion:", self)
        self.write_occasion_input = QComboBox(self)
        self.write_occasion_input.addItems(["OnInitialization", "OnWriteFanSpeed"])

        grid_layout.addWidget(label, 1, 0)
        grid_layout.addWidget(self.write_occasion_input, 1, 1)

        # =====================================================================
        # Write mode
        # =====================================================================

        label = QLabel("Write mode:", self)
        self.write_mode_input = QComboBox(self)
        self.write_mode_input.addItems(["Set", "And", "Or"])

        grid_layout.addWidget(label, 2, 0)
        grid_layout.addWidget(self.write_mode_input, 2, 1)

        # =====================================================================
        # Register
        # =====================================================================

        label = QLabel("Register:", self)
        self.register_input = QSpinBox(self)
        self.register_input.setRange(0, UINT8_MAX)

        grid_layout.addWidget(label, 3, 0)
        grid_layout.addWidget(self.register_input, 3, 1)

        # =====================================================================
        # Value
        # =====================================================================

        label = QLabel("Value:", self)
        self.value_input = QSpinBox(self)
        self.value_input.setRange(0, UINT8_MAX)

        grid_layout.addWidget(label, 4, 0)
        grid_layout.addWidget(self.value_input, 4, 1)

        # =====================================================================
        # Reset On Exit 
        # =====================================================================

        self.grp_reset_required = QGroupBox("Reset on exit")
        self.grp_reset_required.setCheckable(True)
        self.grp_reset_required.setChecked(False)

        l0 = QGridLayout()
        self.grp_reset_required.setLayout(l0)

        label = QLabel("Reset write mode:", self)
        self.reset_write_mode_input = QComboBox()
        self.reset_write_mode_input.addItems(["Set", "And", "Or"])

        l0.addWidget(label, 0, 0)
        l0.addWidget(self.reset_write_mode_input, 0, 1)

        label = QLabel("Reset value:", self)
        self.reset_value_input = QSpinBox(self)
        self.reset_value_input.setRange(0, UINT8_MAX)

        l0.addWidget(label, 1, 0)
        l0.addWidget(self.reset_value_input, 1, 1)

        layout.addWidget(self.grp_reset_required)

    # =========================================================================
    # Public functions
    # =========================================================================

    def set_description(self, value):
        self.description_input.setText(value)

    def set_write_occasion(self, value):
        self.write_occasion_input.setCurrentText(value)

    def set_write_mode(self, value):
        self.write_mode_input.setCurrentText(value)

    def set_register(self, value):
        self.register_input.setValue(value)

    def set_value(self, value):
        self.value_input.setValue(value)

    def set_reset_required(self, value):
        self.grp_reset_required.setChecked(value)

    def set_reset_write_mode(self, value):
        self.reset_write_mode_input.setCurrentText(value)

    def set_reset_value(self, value):
        self.reset_value_input.setValue(value)

    def set_all(self, dictionary):
        self.set_description(dictionary['Description'])
        self.set_write_occasion(dictionary['WriteOccasion'])
        self.set_write_mode(dictionary['WriteMode'])
        self.set_register(dictionary['Register'])
        self.set_value(dictionary['Value'])
        self.set_reset_required(dictionary['ResetRequired'])
        self.set_reset_write_mode(dictionary['ResetWriteMode'])
        self.set_reset_value(dictionary['ResetValue'])

class RegisterWriteConfigurationsWidget(QWidget):
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

        self.table = MyTableWidget(0, 8)
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(["Description", "Write occasion", "Write mode", "Register", "Value", "Reset on exit", "Reset write mode", "Reset value"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setItemFlagCallback(lambda f: f & ~Qt.ItemIsEditable)

        description = MyTableFieldDefinition('Description')
        description.setDefault("None")

        write_occasion = MyTableFieldDefinition('WriteOccasion')
        write_occasion.setDefault('OnInitialization')
        write_occasion.setValidate(lambda v: v in ('OnInitialization', 'OnWriteFanSpeed'))

        write_mode = MyTableFieldDefinition('WriteMode')
        write_mode.setDefault('Set')
        write_mode.setValidate(lambda v: v in ('Set', 'And', 'Or'))

        register = MyTableFieldDefinition('Register')
        register.setDefault(0)
        register.setTypes((int,))

        value = MyTableFieldDefinition('Value')
        value.setDefault(0)
        value.setTypes((int,))

        reset_required = MyTableFieldDefinition('ResetRequired')
        reset_required.setDefault(False)
        reset_required.setTypes((bool,))

        reset_write_mode = MyTableFieldDefinition('ResetWriteMode')
        reset_write_mode.setDefault('Set')
        reset_write_mode.setValidate(lambda v: v in ('Set', 'And', 'Or'))

        reset_value = MyTableFieldDefinition('ResetValue')
        reset_value.setDefault(0)
        reset_value.setTypes((int,))

        self.table.setColumnFields([
            description,
            write_occasion,
            write_mode,
            register,
            value,
            reset_required,
            reset_write_mode,
            reset_value
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

        self.edit = RegisterWriteConfigurationEdit()
        self.edit.setVisible(False)
        layout.addWidget(self.edit)

        # =====================================================================
        # Init
        # =====================================================================

        self.table.selectionModel().selectionChanged.connect(self.table_selection_changed)
        self.edit.description_input.textChanged.connect(self.description_changed)
        self.edit.write_occasion_input.currentTextChanged.connect(self.write_occasion_changed)
        self.edit.write_mode_input.currentTextChanged.connect(self.write_mode_changed)
        self.edit.register_input.valueChanged.connect(self.register_changed)
        self.edit.value_input.valueChanged.connect(self.value_changed)
        self.edit.grp_reset_required.toggled.connect(self.reset_required_changed)
        self.edit.reset_write_mode_input.currentTextChanged.connect(self.reset_write_mode_changed)
        self.edit.reset_value_input.valueChanged.connect(self.reset_value_changed)

    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        r = []

        for row in range(self.table.rowCount()):
            r1 = self.table.get_row_as_dict(row)

            if not r1['ResetRequired']:
                del r1['ResetWriteMode']
                del r1['ResetValue']

            r.append(r1)

        return r

    def from_config(self, cfg, trace, errors):
        self.table.clear()

        if 'RegisterWriteConfigurations' not in cfg:
            return

        if not isinstance(cfg['RegisterWriteConfigurations'], list):
            errors.append(trace.get_trace('RegisterWriteConfigurations: Invalid type'))
            return

        for i, rwc_cfg in enumerate(cfg['RegisterWriteConfigurations']):
            with trace.trace(f'RegisterWriteConfigurations[{i}]'):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.set_row_defaults(row_position)

                for key, error in self.table.update_row(row_position, rwc_cfg):
                    with trace.trace(key):
                        if error is KeyError:
                            if key not in ('WriteOccasion', 'WriteMode', 'ResetRequired', 'ResetWriteMode', 'ResetValue'):
                                errors.append(trace.get_trace('Missing field'))
                        if error is ValueError:
                            errors.append(trace.get_trace('Invalid value'))
                        if error is TypeError:
                            errors.append(trace.get_trace('Invalid type'))

        del cfg['RegisterWriteConfigurations']

    # =========================================================================
    # Helper functions
    # =========================================================================

    def set_item_in_current_row(self, key, value):
        row = self.table.get_selected_row()
        if row is None:
            return

        self.table.update_row(row, {key: value})

    # =========================================================================
    # Signals
    # =========================================================================

    def description_changed(self, value):
        self.set_item_in_current_row('Description', value)

    def write_occasion_changed(self, value):
        self.set_item_in_current_row('WriteOccasion', value)

    def write_mode_changed(self, value):
        self.set_item_in_current_row('WriteMode', value)

    def register_changed(self, value):
        self.set_item_in_current_row('Register', value)

    def value_changed(self, value):
        self.set_item_in_current_row('Value', value)

    def reset_required_changed(self, checked):
        self.set_item_in_current_row('ResetRequired', checked)

    def reset_write_mode_changed(self, value):
        self.set_item_in_current_row('ResetWriteMode', value)

    def reset_value_changed(self, value):
        self.set_item_in_current_row('ResetValue', value)

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
