<template>
  <el-main>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane>
        <template #label>
          <span>{{ $root.data.packages_tabs.name }}</span>
        </template>
        <PackagesTabs />
      </el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
import PackagesTabs from "./PackagesTabs.vue";
export default {
  name: "BaseTabs",
  components: {
    PackagesTabs,
  },
  data() {
    return {
      activeName: "",
    };
  },
  created() {
    console.log("created @ Tabs.vue");
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
};
</script>

<style scoped>
.el-main {
  min-height: calc(100vh - 120px);
}
</style>
