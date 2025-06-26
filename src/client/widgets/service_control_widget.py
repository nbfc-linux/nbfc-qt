class ServiceControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        # =====================================================================
        # Timer
        # =====================================================================

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Service Status
        # =====================================================================

        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)

        # =====================================================================
        # Service Log
        # =====================================================================

        self.log = QPlainTextEdit(self)
        self.log.setReadOnly(True)
        self.log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.log)

        # =====================================================================
        # Read-Only Checkbox
        # =====================================================================

        self.read_only_checkbox = QCheckBox("Start in read-only mode", self)
        layout.addWidget(self.read_only_checkbox)

        # =====================================================================
        # Buttons
        # =====================================================================

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_button_clicked)
        hbox.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        hbox.addWidget(self.stop_button)

        # =====================================================================
        # Message label
        # =====================================================================

        self.message = QLabel("", self)
        self.message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message)

        # =====================================================================
        # Init
        # =====================================================================

        GLOBALS.restart_service.connect(self.service_restart)

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        self.update()
        self.timer.start()

    def stop(self):
        self.timer.stop()

    # =========================================================================
    # Helper functions
    # =========================================================================

    def update(self):
        try:
            status = GLOBALS.nbfc_client.get_status()
            if status['ReadOnly']:
                self.status_label.setText("<b>Running</b> (<i>read-only</i>)")
            else:
                self.status_label.setText("<b>Running</b> (<i>control enabled</i>)")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except Exception as e:
            self.status_label.setText("<b>Stopped</b>")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

        if not GLOBALS.is_root:
            self.read_only_checkbox.setEnabled(False)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.message.setVisible(True)
            self.message.setText(CANNOT_CONTROL_MSG)
        else:
            self.message.setVisible(False)

    def call_with_log(self, args):
        self.log.clear()

        # We need to attach the worker thread to the class instance
        # because it would get destroyed otherwise
        self.worker = SubprocessWorker(args)
        self.worker.output_line.connect(self.handle_output)
        self.worker.error_line.connect(self.handle_output)
        self.worker.start()

    def handle_output(self, line):
        self.log.appendPlainText(line.rstrip())

    def service_start(self, readonly):
        args = ['nbfc', 'start']

        if readonly:
            args.append('-r')

        self.call_with_log(args)

    def service_restart(self, readonly):
        args = ['nbfc', 'restart']

        if readonly:
            args.append('-r')

        self.call_with_log(args)

    def service_stop(self):
        GLOBALS.nbfc_client.stop()

    # =========================================================================
    # Signal functions
    # =========================================================================

    def start_button_clicked(self):
        self.service_start(self.read_only_checkbox.isChecked())

    def stop_button_clicked(self):
        self.service_stop()
