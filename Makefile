prefix ?= /usr
server_cmd = UYi-server
agent_cmd = UYi-agent
views_cmd = uos-sysmig
pythonfile_views = start_webview.py
pythonfile_server = index.py
pythonfile_agent = migration-tools-client.py
bin_dir = /usr/lib
bin = $(DESTDIR)$(prefix)/bin
now_pwd = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
pyinstaller_server = $(now_pwd)server_env/bin/pyinstaller
pyinstaller_agent = $(now_pwd)agent_env/bin/pyinstaller
.PHONY: install uninstall build server agent views vue
.DEFAULT_GOAL := build

build: agent server views vue

agent:	
	cd pyinstaller-4.3;$(now_pwd)agent_env/bin/python3 setup.py install --user ;cd ..
	sed -i "1c  #! $(now_pwd)agent_env/bin/python3" $(pyinstaller_agent)
	sed -i '1s/ //g' $(pyinstaller_agent)
	$(pyinstaller_agent) -F --noconsole --name $(agent_cmd) \
        --runtime-tmpdir /var/tmp/ \
        --paths ./  \
        $(pythonfile_agent)


server:
	cd pyinstaller-4.3;$(now_pwd)server_env/bin/python3 setup.py install --user ;cd ..
	sed -i "1c  #! $(now_pwd)server_env/bin/python3" $(pyinstaller_server)
	sed -i '1s/ //g' $(pyinstaller_server)
	$(pyinstaller_server) -F --noconsole --name $(server_cmd) \
	--add-data template/src/plugins:template/src/plugins/ \
	--runtime-tmpdir /var/tmp/ \
	--paths ./  \
	$(pythonfile_server)


views:
	cd pyinstaller-4.3;$(now_pwd)server_env/bin/python3 setup.py install --user ;cd ..
	sed -i "1c  #! $(now_pwd)server_env/bin/python3" $(pyinstaller_server)
	sed -i '1s/ //g' $(pyinstaller_server)
	$(pyinstaller_server) -F --noconsole --name $(views_cmd) \
	--add-data template/:template/ \
	--runtime-tmpdir /var/tmp/ \
	--paths ./  \
	$(pythonfile_views)

vue:
	cd template;make build;cd ..;

install:
	mkdir -p $(bin_dir)/uos-sysmig-agent/ $(bin_dir)/uos-sysmig-server/ 
	install -m 755 dist/$(agent_cmd) $(bin_dir)/uos-sysmig-agent/
	install -m 755 dist/$(server_cmd) $(bin_dir)/uos-sysmig-server/
	install -m 755 dist/$(views_cmd) $(bin_dir)/uos-sysmig-server/

uninstall:
	rm -f $(bin_dir)/$(agent_cmd)
	rm -f $(bin_dir)/$(server_cmd)

clean:
	rm -rf build/ dist  __pycache__/ $(server_cmd).spec $(agent_cmd).spec $(views_cmd).spec 

