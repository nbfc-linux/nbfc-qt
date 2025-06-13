bindir = /usr/bin

all: nbfc-qt.py nbfc-qt-tray.py nbfc-qt-config.py

nbfc-qt.py: \
	src/common/about.py \
	src/common/nbfc_client.py \
	src/common/version.py \
	src/client/common.py \
	src/client/subprocess_worker.py \
	src/client/widgets/apply_button_widget.py \
	src/client/widgets/service_control_widget.py \
	src/client/widgets/basic_config_widget.py \
	src/client/widgets/fan_control_widget.py \
	src/client/widgets/fan_widget.py \
	src/client/widgets/main_window.py \
	src/client/widgets/temperature_sources_widget.py \
	src/client/widgets/temperature_source_widget.py \
	src/client/widgets/update_widget.py \
	src/client/main.py
	python3 ./src/preprocessor.py --chdir src client/main.py > nbfc-qt.py
	chmod +x nbfc-qt.py

nbfc-qt-config.py: \
	src/common/about.py \
	src/common/nbfc_client.py \
	src/config/defaults.py \
	src/config/limits.py \
	src/config/main.py \
	src/config/widgets/my_table_widget.py \
	src/config/widgets/basic_config_widget.py \
	src/config/widgets/basic_fan_configuration_widget.py \
	src/config/widgets/fan_temperature_thresholds_widget.py \
	src/config/widgets/fan_speed_percentage_overrides_widget.py \
	src/config/widgets/fan_configuration_widget.py \
	src/config/widgets/fan_configurations_widget.py \
	src/config/widgets/register_write_configurations_widget.py \
	src/config/widgets/main_window.py
	python3 ./src/preprocessor.py --chdir src config/main.py > nbfc-qt-config.py
	chmod +x nbfc-qt-config.py

nbfc-qt-tray.py: \
	src/common/nbfc_client.py \
	src/tray/main.py \
	src/ico.py
	python3 ./src/preprocessor.py --chdir src tray/main.py > nbfc-qt-tray.py
	chmod +x nbfc-qt-tray.py

src/ico.py:
	echo "ICON_BASE64 = '''"  > src/ico.py
	base64 fan.ico      		 >> src/ico.py
	echo "'''"               >> src/ico.py

README.md: .force
	./tools/update_readme.py README.md.in > README.md

pkgbuilds/nbfc-qt/PKGBUILD: .force
	./tools/update_pkgbuild.py pkgbuilds/nbfc-qt/PKGBUILD.in > pkgbuilds/nbfc-qt/PKGBUILD

install:
	install -Dm 755 nbfc-qt.py $(DESTDIR)$(bindir)/nbfc-qt
	install -Dm 755 nbfc-qt-tray.py $(DESTDIR)$(bindir)/nbfc-qt-tray
	install -Dm 755 nbfc-qt-config.py $(DESTDIR)$(bindir)/nbfc-qt-config

uninstall:
	rm -f $(DESTDIR)$(bindir)/nbfc-qt
	rm -f $(DESTDIR)$(bindir)/nbfc-qt-tray
	rm -f $(DESTDIR)$(bindir)/nbfc-qt-config
	
clean:
	rm -rf __pycache__
	rm -f  nbfc-qt.py nbfc-qt-tray.py nbfc-qt-config.py
	rm -f  src/ico.py

.force:
	@true
