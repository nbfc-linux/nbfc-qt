bindir = /usr/bin

all: nbfc-qt.py nbfc-qt-tray.py

nbfc-qt.py: \
	src/about.py \
	src/common.py \
	src/fs_sensors.py \
	src/nbfc_client.py \
	src/widgets/apply_button_widget.py \
	src/widgets/basic_config_widget.py \
	src/widgets/fan_control_widget.py \
	src/widgets/fan_widget.py \
	src/widgets/main_window.py \
	src/widgets/temperature_sources_widget.py \
	src/widgets/temperature_source_widget.py \
	src/main.py \
	src/ico.py
	(cd ./src; python3 ./include_files.py main.py > ../nbfc-qt.py)
	chmod +x nbfc-qt.py

nbfc-qt-tray.py: \
	src/nbfc_client.py \
	src/tray.py \
	src/ico.py
	(cd ./src; python3 ./include_files.py tray.py > ../nbfc-qt-tray.py)
	chmod +x nbfc-qt-tray.py

src/ico.py:
	echo "ICON_BASE64 = '''"  > src/ico.py
	base64 fan.ico           >> src/ico.py
	echo "'''"               >> src/ico.py

README.md: README.md.in
	./tools/update_readme.py README.md.in > README.md

install:
	install -Dm 755 nbfc-qt.py $(DESTDIR)$(bindir)/nbfc-qt
	install -Dm 755 nbfc-qt-tray.py $(DESTDIR)$(bindir)/nbfc-qt-tray

uninstall:
	rm -f $(DESTDIR)$(bindir)/nbfc-qt
	rm -f $(DESTDIR)$(bindir)/nbfc-qt-tray
	
clean:
	rm -rf __pycache__
	rm -f  nbfc-qt.py nbfc-qt-tray.py
	rm -f  src/ico.py
