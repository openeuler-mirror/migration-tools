<template>
  <el-main>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane>
        <template #label>
          <span>{{ $root.data.general_tabs.name }}</span>
        </template>
        <GeneralTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span>{{ $root.data.packages_tabs.name }}</span>
        </template>
        <PackagesTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span>{{ $root.data.rpm_tabs.name }}</span>
        </template>
        <RPMTabs />
      </el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
import GeneralTabs from "./GeneralTabs.vue";
import PackagesTabs from "./PackagesTabs.vue";
import RPMTabs from "./RPMTabs.vue";
export default {
  name: "BaseTabs",
  components: {
    GeneralTabs,
    PackagesTabs,
    RPMTabs,
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
