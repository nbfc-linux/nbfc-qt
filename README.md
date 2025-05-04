NBFC-Qt - GUI for NBFC-Linux
============================

**nbfc-qt** is a simple Qt-based graphical user interface for [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux).

**nbfc-qt-tray** is a simple system tray application for controlling fan speeds.

Installation
------------

- Arch Linux:
  - [Latest Version 0.3.11](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.3.11/nbfc-qt-git-0.3.11-1-x86_64.pkg.tar.zst)
  - Install PyQt5: `pacman -S python-pyqt5`
  - Install package: `pacman -U ./nbfc-qt-git-0.3.11-1-x86_64.pkg.tar.zst`

- Debian / Ubuntu:
  - [Latest Version 0.3.11](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.3.11/nbfc-qt_0.3.11_amd64.deb)
  - Install PyQt5: `apt install python3-pyqt5`
  - Install package: `dpkg -i ./nbfc-qt_0.3.11_amd64.deb`

- Fedora:
  - [Latest Version 0.3.11](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.3.11/fedora-nbfc-qt-0.3.11-1.x86_64.rpm)
  - Install PyQt5: `dnf install python3-qt5`
  - Install package: `dnf install ./fedora-nbfc-qt-0.3.11-1.x86_64.rpm`

- OpenSuse (Tumbleweed):
  - [Latest Version 0.3.11](https://github.com/nbfc-linux/nbfc-qt/releases/download/0.3.11/opensuse-nbfc-qt-0.3.11-1.x86_64.rpm)
  - Install PyQt5: `zypper install python3-qt5`
  - Install package: `zypper install ./opensuse-nbfc-qt-0.3.11-1.x86_64.rpm`

- In general:
  - make && sudo make install

