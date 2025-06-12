NBFC-Qt - GUI for NBFC-Linux
============================

**nbfc-qt** is a simple Qt-based graphical user interface for [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux).

**nbfc-qt-tray** is a simple system tray application for controlling fan speeds.

**nbfc-qt-config** is a GUI for creating and editing model configuration files. (**NOT YET RELEASED**)

ALl programs support both PyQt5 and PyQt6.

Installation
------------

- Arch Linux:
  - [Download Latest Version 0.4.1](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.4.1/nbfc-qt-git-0.4.1-1-any.pkg.tar.zst)
  - Install one of the following dependencies (PyQt6 is recommended):
    - PyQt6: `pacman -S python-pyqt6`
    - PyQt5: `pacman -S python-pyqt5`
  - Install package: `pacman -U ./nbfc-qt-git-0.4.1-1-any.pkg.tar.zst`

- Debian / Ubuntu:
  - [Download Latest Version 0.4.1](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.4.1/nbfc-qt_0.4.1_amd64.deb)
  - Install one of the following dependencies (PyQt6 is recommended):
    - PyQt5: `apt install python3-pyqt5`
    - PyQt6: `apt install python3-pyqt6`
  - Install package: `dpkg -i ./nbfc-qt_0.4.1_amd64.deb`

- Fedora:
  - [Download Latest Version 0.4.1](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.4.1/fedora-nbfc-qt-0.4.1-1.x86_64.rpm)
  - Install PyQt5: `dnf install python3-qt5`
  - Install package: `dnf install ./fedora-nbfc-qt-0.4.1-1.x86_64.rpm`

- OpenSuse (Tumbleweed):
  - [Download Latest Version 0.4.1](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.4.1/opensuse-nbfc-qt-0.4.1-1.x86_64.rpm)
  - Install PyQt5: `zypper install python3-qt5`
  - Install package: `zypper install ./opensuse-nbfc-qt-0.4.1-1.x86_64.rpm`

- In general:
  - make && sudo make install

Usage
-----

For **configuring** and **starting** the NBFC service, run `sudo nbfc-qt`.

For **controlling** the fans using the system tray app, run `nbfc-qt-tray`. This does not required root privileges.

For **editing** model configuration files, use `nbfc-qt-config`.

Screenshots
-----------

## NBFC-Qt

![Screenshot NBFC-Qt Service control](http://nbfc-linux.github.io/img/nbfc-qt/nbfc-qt-service.png)

![Screenshot NBFC-Qt Fan Control](http://nbfc-linux.github.io/img/nbfc-qt/nbfc-qt-fans.png)

![Screenshot NBFC-Qt Basic Configuration](http://nbfc-linux.github.io/img/nbfc-qt/nbfc-qt-basic.png)

![Screenshot NBFC-Qt Sensor Configuration](http://nbfc-linux.github.io/img/nbfc-qt/nbfc-qt-sensors.png)

![Screenshot NBFC-Qt Update](http://nbfc-linux.github.io/img/nbfc-qt/nbfc-qt-update.png)

## NBFC-Qt-Config

![Screenshot of NBFC-Qt-Config Basic Configuration](http://nbfc-linux.github.io/img/nbfc-qt-config/nbfc-qt-config-basic.png)

![Screenshot of NBFC-Qt-Config Basic Fan Configuration](http://nbfc-linux.github.io/img/nbfc-qt-config/nbfc-qt-config-fan-basic.png)

![Screenshot of NBFC-Qt-Config Fan Temperature Thresholds](http://nbfc-linux.github.io/img/nbfc-qt-config/nbfc-qt-config-fan-temperature-thresholds.png)

![Screenshot of NBFC-Qt-Config Fan Speed Overrides](http://nbfc-linux.github.io/img/nbfc-qt-config/nbfc-qt-config-fan-speed-overrides.png)

![Screenshot of NBFC-Qt-Config Register Write Configurations](http://nbfc-linux.github.io/img/nbfc-qt-config/nbfc-qt-config-register-write-configurations.png)

