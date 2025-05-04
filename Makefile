all: nbfc-qt.py

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
	src/main.py
	(cd ./src; python3 ./include_files.py main.py > ../nbfc-qt.py)
	chmod +x nbfc-qt.py

install:
	install -Dm 755 nbfc-qt.py $(DESTDIR)$(bindir)/nbfc-qt

uninstall:
	rm -f $(DESTDIR)$(bindir)/nbfc-qt
	
clean:
	rm -rf __pycache__
	rm -f  nbfc-qt.py
