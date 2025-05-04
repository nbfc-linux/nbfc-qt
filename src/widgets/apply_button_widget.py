class ApplyButtonsWidget(QWidget):
    def __init__(self):
        super().__init__()

        vbox_layout = QVBoxLayout()
        #vbox_layout.addStretch() TODO
        self.setLayout(vbox_layout)

        self.error_label = QLabel("", self)
        vbox_layout.addWidget(self.error_label)

        self.read_only_checkbox = QCheckBox("(Re-)start in read-only mode", self)
        vbox_layout.addWidget(self.read_only_checkbox)

        hbox_layout = QHBoxLayout()
        vbox_layout.addLayout(hbox_layout)

        self.apply_button = QPushButton("Apply", self)
        hbox_layout.addWidget(self.apply_button)

        self.apply_with_restart_button = QPushButton("Apply with (re-)start", self)
        hbox_layout.addWidget(self.apply_with_restart_button)

    def enable(self):
        self.error_label.setHidden(True)
        self.read_only_checkbox.setEnabled(True)
        self.apply_button.setEnabled(True)
        self.apply_with_restart_button.setEnabled(True)

    def disable(self, reason):
        self.error_label.setText(reason)
        self.error_label.setHidden(False)
        self.read_only_checkbox.setEnabled(False)
        self.apply_button.setEnabled(False)
        self.apply_with_restart_button.setEnabled(False)

