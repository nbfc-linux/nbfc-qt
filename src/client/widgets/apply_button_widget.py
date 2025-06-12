class ApplyButtonsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Read-only checkbox
        # =====================================================================

        self.read_only_checkbox = QCheckBox("(Re-)start in read-only mode", self)
        layout.addWidget(self.read_only_checkbox)

        # =====================================================================
        # Save and Apply buttons
        # =====================================================================

        hbox_layout = QHBoxLayout()
        layout.addLayout(hbox_layout)

        self.save_button = QPushButton("Save", self)
        hbox_layout.addWidget(self.save_button)

        self.apply_button = QPushButton("Apply with (re-)start", self)
        hbox_layout.addWidget(self.apply_button)

        # =====================================================================
        # Error label
        # =====================================================================

        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

    def enable(self):
        self.error_label.setHidden(True)
        self.read_only_checkbox.setEnabled(True)
        self.save_button.setEnabled(True)
        self.apply_button.setEnabled(True)

    def disable(self, reason):
        self.error_label.setText(reason)
        self.error_label.setHidden(False)
        self.read_only_checkbox.setEnabled(False)
        self.save_button.setEnabled(False)
        self.apply_button.setEnabled(False)
