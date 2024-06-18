# uos-sysmig-export-html

有易迁移工具迁移分析导出下载页面，在此工程中有三个导出页面，分别为：

1. rc (replace check) 存量替换-迁移检查，对应为 A 版的迁移前检查
1. ra (replace analysis) 存量替换-迁移分析，对应为 A 版的迁移后分析
1. ec (expansion check) 新增扩容-迁移检查，对应为 E 版的检查分析

开发时，通过执行 `npm run dev` 后可以通过以下三个连接打开对应的页面：

1. rc: http://127.0.0.1:3000/
1. ra: http://127.0.0.1:3000/ra/
1. ec: http://127.0.0.1:3000/ec/

**注意打开链接时， 链接中的最后一个`/`不要忘写了**

前后端交互的 json 数据结构在代码中有示例。

**注意 json 代码中不要加 `//` 注释**

---

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
