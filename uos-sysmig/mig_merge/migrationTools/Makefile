prefix ?= /usr
modules = migrationTools
cmd = utmtc
pythonfile = utmtc.py
bin_dir = $(DESTDIR)$(prefix)/bin
pyinstaller = $(HOME)/.local/bin/pyinstaller

.PHONY: install uninstall build frontend bin
.DEFAULT_GOAL := build

build: frontend frontend-esc bin

frontend:
	cd ./frontend; make build
	cp -rf frontend/dist/* data/report-template/resource/
	cp -rf frontend/dist/index.html data/report-template/

frontend-esc:
	cd ./frontend-exportSysConf; make build
	cp -rf frontend-exportSysConf/dist/* exportSysConf/static/
bin:
	$(pyinstaller) --onefile --noconsole --name $(cmd) \
	--runtime-tmpdir /var/tmp/ \
	--paths ./  \
	--add-data utils/pygrok:${modules}/utils/pygrok \
	--add-data data:$(modules)/data \
	--add-data exportSysConf:$(modules)/exportSysConf \
	$(pythonfile)


install:
	mkdir -p $(bin_dir)
	install -m 755 dist/$(cmd) $(bin_dir)/$(cmd)
uninstall:
	rm -f $(bin_dir)/$(cmd)

clean:
	cd ./frontend; make clean
	rm -rf build/ dist/ __pycache__/ $(cmd).spec
