RATE_CONFIG_HELP_TEXT = """\
The rating feature analyzes whether a configuration can be executed safely on the current system. A positive rating does not necessarily mean that the configuration will work correctly, only that it appears reasonable and non-destructive.<br />
<br />
Configurations that reference the same registers and ACPI methods are grouped together.<br />
<br />
<b>FULL MATCH</b><br />
Indicates that the register is a known fan register.<br />
<br />
<b>PARTIAL MATCH</b><br />
Indicates that the register name contains <b>FAN</b>, <b>RPM</b>, or <b>PWM</b>.<br />
<br />
<b>MINIMAL MATCH</b><br />
Indicates that the register name starts with the letter '<b>F</b>'.<br />
<br />
<b>BAD REGISTER</b><br />
Indicates that the register name is a known bad register (likely a battery-related register).<br />
<br />
<b>NO MATCH</b><br />
Indicates that none of the matching rules apply.<br />
<br />
<b>NOT FOUND</b><br />
Indicates that the register is not named in the firmware and additional information could not be retrieved.<br />
<br />
For fan registers, at least a <b>MINIMAL MATCH</b> is required to consider a configuration usable.<br />
<br />
For RegisterWriteConfiguration registers, some registers may not yet be present in the rule database. In these cases, a <b>NO MATCH</b> result may still be acceptable.<br />
<br />
If in doubt, it is recommended to dump the firmware using <b>sudo nbfc acpi-dump dsl</b> and manually analyze the registers used by the configuration file. This requires some technical knowledge."""

class RateConfigsHelpWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NBFC Rated Configs Help")
        self.resize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        label = QLabel(RATE_CONFIG_HELP_TEXT)
        label.setWordWrap(True)
        scroll_area.setWidget(label)

        button = QPushButton("Close")
        button.clicked.connect(self.close_clicked)
        layout.addWidget(button)

    def close_clicked(self):
        self.close()
