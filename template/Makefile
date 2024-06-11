
SHELL := /bin/bash
.ONESHELL:
build:
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
	npm config set registry 'https://registry.npmmirror.com';
	npm install;
	npm run build
	npm i
	rm -rf build


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
