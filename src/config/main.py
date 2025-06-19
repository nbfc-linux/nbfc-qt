#!/usr/bin/env python3

import os
import sys
import json
import signal
import argparse

# =============================================================================
# Make Qt6 compatible with Qt5
# =============================================================================

def make_qt5_compatible():
    setattr(Qt,          'UserRole',          Qt.ItemDataRole.UserRole)
    setattr(Qt,          'ItemIsEditable',    Qt.ItemFlag.ItemIsEditable)
    setattr(QMessageBox, 'Ok',                QMessageBox.StandardButton.Ok)
    setattr(QMessageBox, 'No',                QMessageBox.StandardButton.No)
    setattr(QMessageBox, 'Yes',               QMessageBox.StandardButton.Yes)

# =============================================================================
# NBFC-Qt Command Line Options
# =============================================================================

#include common/qt_help.py

argp = argparse.ArgumentParser(
    prog='nbfc-qt',
    description='Qt-based GUI for NBFC-Linux',
    epilog=QT_HELP_TEXT,
    formatter_class=argparse.RawDescriptionHelpFormatter)

argp.add_argument('--version', action='version', version='%(prog)s 0.4.2')

argp.add_argument('--import',
    help='Import a existing configuration file',
    dest='import_file')

#ifeq QT_VERSION 0
grp = argp.add_argument_group(title='Qt version')

grp.add_argument('--qt5',
    help='Use PyQt5',
    dest='qt_version', action='store_const', const=5)

grp.add_argument('--qt6',
    help='Use PyQt6',
    dest='qt_version', action='store_const', const=6)
#endif

opts, qt_args = argp.parse_known_args()

# =============================================================================
# Import Qt5/Qt6
# =============================================================================

#ifeq QT_VERSION 0
if opts.qt_version is None:
    try:
        from PyQt6.QtWidgets import *
        from PyQt6.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
        from PyQt6.QtGui import QAction
        make_qt5_compatible()
    except ImportError:
        try:
            from PyQt5.QtWidgets import *
            from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
        except ImportError:
            print("Please install Python Qt bindings (PyQt5 or PyQt6)")
            sys.exit(1)

elif opts.qt_version == 5:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal

elif opts.qt_version == 6:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
    from PyQt6.QtGui import QAction
    make_qt5_compatible()
#endif

#ifeq QT_VERSION 5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
#endif

#ifeq QT_VERSION 6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
from PyQt6.QtGui import QAction
make_qt5_compatible()
#endif

# =============================================================================
# Program
# =============================================================================

#include common/about.py
#include common/nbfc_client.py

class Globals(QObject):
    read_write_words_changed = pyqtSignal(bool)
    legacy_temperature_thresholds_behaviour_changed = pyqtSignal(bool)

    nbfc_client = None

    def init(self):
        self.nbfc_client = NbfcClient()

GLOBALS = Globals()

def show_error_message(parent, title, message):
    QMessageBox.critical(parent, title, message, QMessageBox.Ok)

#include config/trace.py
#include config/limits.py
#include config/defaults.py
#include config/widgets/my_table_widget.py
#include config/widgets/basic_config_widget.py
#include config/widgets/basic_fan_configuration_widget.py
#include config/widgets/fan_temperature_thresholds_widget.py
#include config/widgets/fan_speed_percentage_overrides_widget.py
#include config/widgets/fan_configuration_widget.py
#include config/widgets/fan_configurations_widget.py
#include config/widgets/register_write_configurations_widget.py
#include config/widgets/main_window.py

# Make CTLR+C work
signal.signal(signal.SIGINT, signal.SIG_DFL)

app = QApplication([sys.argv[0]] + qt_args)

try:
    GLOBALS.init()
except Exception as e:
    show_error_message(None, "Error", str(e))
    sys.exit(1)

main_window = MainWindow()
main_window.show()
if opts.import_file:
    main_window.import_file(opts.import_file)
sys.exit(app.exec())
