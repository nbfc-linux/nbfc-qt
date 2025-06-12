#!/usr/bin/env python3

import os
import sys
import signal
import argparse
import threading

# =============================================================================
# Make Qt6 compatible with Qt5
# =============================================================================

def make_qt5_compatible():
    setattr(Qt,          'AlignCenter', Qt.AlignmentFlag.AlignCenter)
    setattr(Qt,          'UserRole',    Qt.ItemDataRole.UserRole)
    setattr(Qt,          'Horizontal',  Qt.Orientation.Horizontal)
    setattr(QMessageBox, 'Ok',          QMessageBox.StandardButton.Ok)

# =============================================================================
# NBFC-Qt Command Line Options
# =============================================================================

#include common/qt_help.py

argp = argparse.ArgumentParser(
    prog='nbfc-qt',
    description='Qt-based GUI for NBFC-Linux',
    epilog=QT_HELP_TEXT,
    formatter_class=argparse.RawDescriptionHelpFormatter)

argp.add_argument('--version', action='version', version='%(prog)s 0.4.1')

grp = argp.add_argument_group(title='Widgets')

grp.add_argument('--service',
    help='Start with service widget',
    dest='widget', action='store_const', const='service')

grp.add_argument('--fans',
    help='Start with fans widget',
    dest='widget', action='store_const', const='fans')

grp.add_argument('--basic',
    help='Start with basic configuration widget',
    dest='widget', action='store_const', const='basic')

grp.add_argument('--sensors',
    help='Start with sensors widget',
    dest='widget', action='store_const', const='sensors')

grp.add_argument('--update',
    help='Start with update widget',
    dest='widget', action='store_const', const='update')

grp = argp.add_argument_group(title='Qt version')

grp.add_argument('--qt5',
    help='Use PyQt5',
    dest='qt_version', action='store_const', const=5)

grp.add_argument('--qt6',
    help='Use PyQt6',
    dest='qt_version', action='store_const', const=6)

opts, qt_args = argp.parse_known_args()

# =============================================================================
# Import Qt5/Qt6
# =============================================================================

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

# =============================================================================
# Program
# =============================================================================

#include client/common.py
#include client/errors.py
#include common/about.py
#include common/nbfc_client.py
#include common/version.py

class Globals(QObject):
    model_config_changed = pyqtSignal()
    restart_service = pyqtSignal(bool)

    is_root = (os.geteuid() == 0)
    nbfc_client = None

    def init(self):
        self.nbfc_client = NbfcClient()

REQUIRED_NBFC_VERSION = '0.3.16'
GITHUB_URL = 'https://github.com/nbfc-linux/nbfc-linux'
GLOBALS = Globals()

def show_error_message(parent, title, message):
    QMessageBox.critical(parent, title, message, QMessageBox.Ok)

#include client/subprocess_worker.py
#include client/widgets/apply_button_widget.py
#include client/widgets/service_control_widget.py
#include client/widgets/fan_widget.py
#include client/widgets/fan_control_widget.py
#include client/widgets/basic_config_widget.py
#include client/widgets/temperature_source_widget.py
#include client/widgets/temperature_sources_widget.py
#include client/widgets/update_widget.py
#include client/widgets/main_window.py

# Make CTLR+C work
signal.signal(signal.SIGINT, signal.SIG_DFL)

app = QApplication([sys.argv[0]] + qt_args)

try:
    GLOBALS.init()
except Exception as e:
    show_error_message(None, "Error", str(e))
    sys.exit(1)

try:
    current_version = GLOBALS.nbfc_client.get_version()
except Exception as e:
    show_error_message(None, "Error", f"Could not get version of NBFC client: {e}")
    sys.exit(1)

if make_version_tuple(current_version) < make_version_tuple(REQUIRED_NBFC_VERSION):
    errmsg = f'''\
NBFC-Linux version <b>{REQUIRED_NBFC_VERSION}</b> or newer is required to run this program. <br />
<br />
You can get the latest version from <a href="{GITHUB_URL}">GitHub.com</a>'''
    show_error_message(None, "Version Error", errmsg)
    sys.exit(1)

main_window = MainWindow()
main_window.show()
if opts.widget:
    main_window.setTabById(opts.widget)
sys.exit(app.exec())
