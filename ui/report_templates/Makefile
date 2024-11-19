SHELL := /bin/bash
RELEASE_DIR = release
.ONESHELL:

all:  build dist

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
# 把APP.vue 文件中用于开发模式的 json 文件导入语句注释掉
	find src/ -name "App.vue" | xargs -I {} sed -i '/dataPlaceholder/s|import|// import|g' {}
# 编译的时候，需要把所有的资源都打包到 html 文件中，最终只输出对应的 html 文件
# 通过 vite 插件 vite-plugin-singlefile 实现的此功能
# 但是这个插件对多页面的项目无效， https://github.com/richardtallent/vite-plugin-singlefile/issues/17
# 所以只能一个页面一个页面的编译了, 编译完成后将结果拷贝到 $(RELEASE_DIR) 目录下

	[ -d $(RELEASE_DIR) ] && rm -rf $(RELEASE_DIR)
	mkdir  $(RELEASE_DIR)
# 报告模板命令： https://doc.uniontech.com/docs/JHJv9ywpYGk8tKgV
	declare -A pages=(
		[rc]="stock_replace_check"
		[ra]="stock_replace_analysis"
		[ec]="new_expansion_check"
	)
	for key in $$(echo $${!pages[@]});do \
		value=$${pages[$$key]}; \
		sed -i '/resolve(__dirname/s|^|//|g' vite.config.js; \
		sed -i "/$$key: resolve/s|//||g" vite.config.js; \
		npm run build; \
		mkdir -p "$(RELEASE_DIR)/$${key}"; \
		find dist/ -name "index.html" | xargs -I {} mv {} "$(RELEASE_DIR)/$${key}"; \
		mv ${RELEASE_DIR}/$${key}/index.html ${RELEASE_DIR}/$${value}.html; \
		sed -i '/resolve(__dirname/s|//||g' vite.config.js; \
	done
# 最终结果发布到 dist 目录下
	rm -rf dist/*
	mv ${RELEASE_DIR}/*.html dist/
	rm -rf ${RELEASE_DIR}

# 把APP.vue 文件中用于开发模式的 json 文件导入语句反注释掉,方便开发时，开箱即用
	find src/ -name "App.vue" | xargs -I {} sed -i '/dataPlaceholder/s|// import|import|g' {}

dev:
# 开发模式，用户编译打包后替换 html 文件中的 dataPlaceholder 变量，查看网页是否正常
# 报告模板命令： https://doc.uniontech.com/docs/JHJv9ywpYGk8tKgV
	declare -A pages=(
		[rc]="stock_replace_check"
		[ra]="stock_replace_analysis"
		[ec]="new_expansion_check"
	)
	for key in $$(echo $${!pages[@]});do \
		value=$${pages[$$key]}; \
		jq -c . src/data/$${value}.json > ./.$${value}.json; \
		scripts/replace_string_with_file.py -s "dataPlaceholder" -f1 dist/$${value}.html -f2 ./.$${value}.json -o dist/$${value}-dev.html; \
		rm -f ./.$${value}.json; \
	done
# 打开网页，查看网页是否正常
	python3 -m http.server -d dist

.PHONY: dist build all
.DEFAULT_GOAL := all

clean:
	rm -rf dist node_modules build
