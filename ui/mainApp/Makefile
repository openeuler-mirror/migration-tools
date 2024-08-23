SHELL := /bin/bash
.ONESHELL:

all: build dist

build:
	[ -f ~/.bashrc ] && source ~/.bashrc
	if node -v ;then
		echo "node is installed"
	else
		touch ~/.bashrc
		curl -o- https://ghproxy.com/https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh| \
		sed -e 's|https://github.com|https://ghproxy.com/https://github.com|g' \
		-e 's|https://raw.githubusercontent.com|https://ghproxy.com/https://raw.githubusercontent.com|g'\
		| bash
		source ~/.bashrc
		export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node/
		nvm install --no-progress --latest-npm --lts
		nvm use --lts
	fi
		source ~/.bashrc
		npm config set registry 'https://registry.npmmirror.com';
		npm i

dist:
		[ -f ~/.bashrc ] && source ~/.bashrc
		npm run build


.PHONY: build dist all
.DEFAULT_GOAL := all

clean:
	rm -rf dist node_modules build
