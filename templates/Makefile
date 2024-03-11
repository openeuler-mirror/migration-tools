SHELL := /bin/bash
NODE_VERSION = 16.14.0
.ONESHELL:
build:
# config nodejs with nvm
	touch ~/.bashrc
	curl -o- https://ghproxy.com/https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh| \
	sed -e 's|https://github.com|https://ghproxy.com/https://github.com|g' \
	-e 's|https://raw.githubusercontent.com|https://ghproxy.com/https://raw.githubusercontent.com|g'\
	| bash
	source ~/.bashrc
	export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node/
	nvm install $(NODE_VERSION)
	nvm use $(NODE_VERSION)
	npm config set registry 'https://registry.npmmirror.com';
	#export NODE_HOME=/usr/local/n/versions/node/$(NODE_VERSION)/
	#export PATH=$(NODE_HOME)/bin:$(PATH)
	npm install -g npm@6.14.15
	npm i
	npm run build
SHELL := /bin/bash
run:
	ifeq ($(shell uname -m), x86_64)
		mkdir -p build/node
		tar -xf $(wildcard node-v*-linux-x64.tar.xz) -C build/node
		mv -f build/node/node-v*-linux-x64 build/node/node
	endif
	ifeq ($(shell uname -m), aarch64)
		mkdir -p build/node
		tar -xf $(wildcard node-v*-linux-arm64.tar.xz) -C build/node
		mv -f build/node/node-v*-linux-arm64 build/node/node
	endif
	export PATH=$(PWD)/build/node/node/bin:$$PATH;
	npm run serve
.PHONY: build
clean:
	rm -rf dist node_modules build
