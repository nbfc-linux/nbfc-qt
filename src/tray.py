#!/usr/bin/env python3

import sys
import base64

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QCheckBox, QLabel, QSystemTrayIcon,
    QMenu, QAction, QMessageBox
)

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QCursor, QPixmap

#include nbfc_client.py
#include ico.py

NBFC_CLIENT = NbfcClient()

def get_icon():
    data = base64.b64decode(ICON_BASE64)
    pix = QPixmap()
    pix.loadFromData(data)
    return QIcon(pix)

class FanWidget(QWidget):
    def __init__(self, fan_info: dict, index: int):
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
        except Exception:
            pass  # ignore failures

    def _on_auto_toggle(self, state):
        auto = (state == Qt.Checked)
        self.slider.setEnabled(not auto)
        try:
            NBFC_CLIENT.set_fan_speed("auto" if auto else self.slider.value() / 10.0, self.index)
        except Exception:
            pass  # ignore failures


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
        for fw in self.fan_widgets:
            self.layout.removeWidget(fw)
            fw.deleteLater()
        self.fan_widgets.clear()

        # Create new FanWidgets
        for idx, fan_info in enumerate(status.get("Fans", [])):
            fw = FanWidget(fan_info, idx)
            self.layout.addWidget(fw)
            self.fan_widgets.append(fw)

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
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.ctrl = FanControlWidget()

        # Tray icon
        icon = QIcon.fromTheme("preferences-system")
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
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    TrayApp().run()
