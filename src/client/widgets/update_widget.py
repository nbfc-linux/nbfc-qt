class UpdateWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Description
        # =====================================================================

        label = QLabel("Fetch new configuration files from the internet", self)
        layout.addWidget(label)

        # =====================================================================
        # Log
        # =====================================================================

        self.log = QPlainTextEdit(self)
        self.log.setReadOnly(True)
        self.log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.log)

        # =====================================================================
        # Error message
        # =====================================================================

        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # =====================================================================
        # Update button
        # =====================================================================

        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_button_clicked)
        layout.addWidget(self.update_button)

        # =====================================================================
        # Init code
        # =====================================================================

        if GLOBALS.is_root:
            self.error_label.setVisible(False)
        else:
            self.update_button.setEnabled(False)
            self.error_label.setText("You cannot update the configurations because you are not root")
            self.error_label.setVisible(True)

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        pass

    def stop(self):
        pass

    # =========================================================================
    # Signal functions
    # =========================================================================

    def update_button_clicked(self):
        self.log.clear()
        self.update_button.setEnabled(False)

        # We need to attach the worker thread to the class instance
        # because it would get destroyed otherwise
        self.worker = SubprocessWorker(['nbfc', 'update'])
        self.worker.output_line.connect(self.handle_output)
        self.worker.error_line.connect(self.handle_output)
        self.worker.finished.connect(self.command_finished)
        self.worker.start()

    def handle_output(self, line):
        self.log.appendPlainText(line.rstrip())

    def command_finished(self, exitstatus):
        self.update_button.setEnabled(True)
