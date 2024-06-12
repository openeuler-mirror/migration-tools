<template>
  <el-container direction="vertical"></el-container>
  <TheHeader />
  <BaseTabs />
  <TheFooter />
</template>

<script>
import TheHeader from "../common/TheHeader.vue";
import TheFooter from "../common/TheFooter.vue";
import BaseTabs from "./BaseTabs.vue";

// 调试用测试数据， 编译打包时会自动注释此行
import dataPlaceholder from "@/data/new_expansion_check.json";

export default {
  name: "App",
  components: {
    TheHeader,
    TheFooter,
    BaseTabs,
  },
  data() {
    return {
      data: dataPlaceholder,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #303133;
  margin-top: 0px;
  margin-left: 20px;
  margin-right: 20px;
  padding: 30px;
}

.el-header,
.el-footer {
  background-color: #409eff;
  color: var(--el-text-color-primary);
  line-height: 60px;
  padding: 0px;
}

body > .el-container {
  margin: 40px;
  padding: 0px;
}
</style>
