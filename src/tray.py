#!/usr/bin/env python3

import sys
import base64
import signal
import argparse

# =============================================================================
# Make Qt6 compatible with Qt5
# =============================================================================

def make_qt5_compatible():
    setattr(Qt,              'AlignCenter', Qt.AlignmentFlag.AlignCenter)
    setattr(Qt,              'Popup',       Qt.WindowType.Popup)
    setattr(Qt,              'Vertical',    Qt.Orientation.Vertical)
    setattr(Qt,              'Checked',     Qt.CheckState.Checked)
    setattr(QSystemTrayIcon, 'Trigger',     QSystemTrayIcon.ActivationReason.Trigger)

# =============================================================================
# NBFC-Qt-Tray Command Line Options
# =============================================================================

#include qt_help.py

argp = argparse.ArgumentParser(
    prog='nbfc-qt-tray',
    description='Qt-based tray app for NBFC-Linux',
    epilog=QT_HELP_TEXT,
    formatter_class=argparse.RawDescriptionHelpFormatter)

argp.add_argument('--version', action='version', version='%(prog)s 0.4.0')

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
        from PyQt6.QtCore import Qt, QPoint
        from PyQt6.QtGui import QAction, QIcon, QCursor, QPixmap
        make_qt5_compatible()
    except ImportError:
        try:
            from PyQt5.QtWidgets import *
            from PyQt5.QtCore import Qt, QPoint
            from PyQt5.QtGui import QIcon, QCursor, QPixmap
        except ImportError:
            print("Please install Python Qt bindings (PyQt5 or PyQt6)")
            sys.exit(1)

elif opts.qt_version == 5:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import Qt, QPoint
    from PyQt5.QtGui import QIcon, QCursor, QPixmap

elif opts.qt_version == 6:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import Qt, QPoint
    from PyQt6.QtGui import QAction, QIcon, QCursor, QPixmap
    make_qt5_compatible()

#include nbfc_client.py
#include ico.py

NBFC_CLIENT = NbfcClient()

def get_icon():
    data = base64.b64decode(ICON_BASE64)
    pix = QPixmap()
    pix.loadFromData(data)
    return QIcon(pix)

class FanWidget(QWidget):
    def __init__(self, index, fan_info):
        super().__init__()
        self.index = index
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)

        # Name label
        lbl = QLabel(fan_info["Name"])
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        # Vertical slider (0–100.0 mapped to 0–1000)
        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(0, 1000)
        initial = fan_info["RequestedSpeed"]
        self.slider.setValue(int(initial * 10))
        self.slider.setEnabled(not fan_info["AutoMode"])
        self.slider.valueChanged.connect(self._on_slider_change)
        layout.addWidget(self.slider, stretch=1)

        # Auto checkbox
        self.checkbox = QCheckBox("Auto")
        self.checkbox.setChecked(fan_info["AutoMode"])
        self.checkbox.stateChanged.connect(self._on_auto_toggle)
        layout.addWidget(self.checkbox)

    def _on_slider_change(self, val):
        speed = val / 10.0
        try:
            NBFC_CLIENT.set_fan_speed(speed, self.index)
        except Exception as e:
            print('Error:', e, file=sys.stderr)

    def _on_auto_toggle(self, state):
        auto = self.checkbox.isChecked()
        self.slider.setEnabled(not auto)
        try:
            NBFC_CLIENT.set_fan_speed("auto" if auto else self.slider.value() / 10.0, self.index)
        except Exception as e:
            print('Error:', e, file=sys.stderr)


class FanControlWidget(QWidget):
    def __init__(self):
        super().__init__(flags=Qt.Popup)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)
        self.fan_widgets = []

    def load(self):
        # Attempt to retrieve status
        try:
            status = NBFC_CLIENT.get_status()
        except Exception as e:
            QMessageBox.warning(None, "Failed to get fan status", str(e))
            return False

        # Clear old widgets
        for widget in self.fan_widgets:
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.fan_widgets.clear()

        # Create new FanWidgets
        for idx, fan_info in enumerate(status.get("Fans", [])):
            widget = FanWidget(idx, fan_info)
            self.layout.addWidget(widget)
            self.fan_widgets.append(widget)

        self.adjustSize()
        return True

    def show_at_cursor(self):
        if not self.load():
            return  # do not show popup, but application keeps running
        cursor = QCursor.pos()
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = self.width(), self.height()
        x = cursor.x() - w // 2
        y = cursor.y() - h - 10
        # clamp to screen bounds
        x = max(screen.left(), min(x, screen.right() - w))
        y = max(screen.top(), min(y, screen.bottom() - h))
        self.move(x, y)
        self.show()


class TrayApp:
    def __init__(self):
        self.app = QApplication([sys.argv[0]] + qt_args)
        self.app.setQuitOnLastWindowClosed(False)
        self.ctrl = FanControlWidget()

        # Tray icon
        self.tray = QSystemTrayIcon(get_icon(), self.app)
        self.tray.setToolTip("Fan Controller")

        # Right-click menu
        menu = QMenu()
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)

        # Left-click toggles popup
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # left click
            if self.ctrl.isVisible():
                self.ctrl.hide()
            else:
                self.ctrl.show_at_cursor()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    # Make CTLR+C work
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    TrayApp().run()
