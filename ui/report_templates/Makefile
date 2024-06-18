SHELL := /bin/bash
RELEASE_DIR = release
.ONESHELL:
build:
        ifeq ($(shell uname -m), x86_64)
		mkdir -p build/node
		tar -xf $(wildcard ../3rdparty/node/node-v*-linux-x64.tar.xz) -C build/node
		mv -f build/node/node-v*-linux-x64 build/node/node
        endif

        ifeq ($(shell uname -m), aarch64)
		mkdir -p build/node
		tar -xf $(wildcard ../3rdparty/node/node-v*-linux-arm64.tar.xz) -C build/node
		mv -f build/node/node-v*-linux-arm64 build/node/node
        endif

	export PATH=$(PWD)/build/node/node/bin:$$PATH;
	npm config set registry 'https://registry.npmmirror.com';
	npm install;

release:
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
	mv ${RELEASE_DIR}/*.html dist/
	rm -rf ${RELEASE_DIR}


# 把APP.vue 文件中用于开发模式的 json 文件导入语句反注释掉,方便开发时，开箱即用
	find src/ -name "App.vue" | xargs -I {} sed -i '/dataPlaceholder/s|// import|import|g' {}

dev:
	npm run dev

.PHONY: release
.DEFAULT_GOAL := release

clean:
	rm -rf dist node_modules build
