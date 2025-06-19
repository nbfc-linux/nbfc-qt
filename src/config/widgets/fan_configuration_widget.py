class FanConfigurationWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # =====================================================================
        # Layout
        # =====================================================================

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.tab_widget = QTabWidget(self)

        self.basic_fan_config = BasicFanConfigWidget(self)
        self.temperature_thresholds = TemperatureThresholdsWidget(self)
        self.fan_speed_percentage_overrides = FanSpeedPercentageOverrides(self)

        self.tab_widget.addTab(self.basic_fan_config, "Basic Configuration")
        self.tab_widget.addTab(self.temperature_thresholds, "Temperature Thresholds")
        self.tab_widget.addTab(self.fan_speed_percentage_overrides, "Fan speed overrides")

        layout.addWidget(self.tab_widget)
        
    # =========================================================================
    # Public functions
    # =========================================================================

    def get_config(self):
        basic = self.basic_fan_config.get_config()
        temperature_thresholds = self.temperature_thresholds.get_config()
        fan_speed_percentage_overrides = self.fan_speed_percentage_overrides.get_config()

        if temperature_thresholds:
            basic['TemperatureThresholds'] = temperature_thresholds

        if fan_speed_percentage_overrides:
            basic['FanSpeedPercentageOverrides'] = fan_speed_percentage_overrides

        return basic

    def from_config(self, cfg, trace, errors):
        self.basic_fan_config.from_config(cfg, trace, errors)
        self.temperature_thresholds.from_config(cfg, trace, errors)
        self.fan_speed_percentage_overrides.from_config(cfg, trace, errors)
