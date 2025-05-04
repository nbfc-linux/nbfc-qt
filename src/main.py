#!/usr/bin/env python3

import os
import sys
import json
import signal

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal

#include about.py
#include common.py
#include fs_sensors.py
#include nbfc_client.py

IS_ROOT = (os.geteuid() == 0)
NBFC_CLIENT = NbfcClient()
NOT_ROOT_NOTICE = "You cannot change the configuration because you are not root"

class ModelConfigChanged(QObject):
    changed = pyqtSignal()

MODEL_CONFIG_CHANGED = ModelConfigChanged()

#include widgets/apply_button_widget.py
#include widgets/fan_widget.py
#include widgets/fan_control_widget.py
#include widgets/basic_config_widget.py
#include widgets/temperature_source_widget.py
#include widgets/temperature_sources_widget.py
#include widgets/main_window.py

if __name__ == '__main__':
    # Make CTLR+C work
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
