<template>
  <el-main>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane>
        <template #label>
          <span>硬件兼容性评估</span>
        </template>
        <HardwareTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span>配置兼容性评估</span>
        </template>
        <ConfigScanTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span> RPM 兼容性评估 </span>
        </template>
        <RpmScanTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span>系统修改配置</span>
        </template>
        <SysConfFileTabs :tabsData="sysConfFileTabsData" />
      </el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
import HardwareTabs from "./HardwareTabs.vue";
import ConfigScanTabs from "./ConfigScanTabs.vue";
import RpmScanTabs from "./RpmScanTabs.vue";
import SysConfFileTabs from "./SysConfFileTabs.vue";

export default {
  name: "BaseTabs",
  compantnets: {
    HardwareTabs,
    ConfigScanTabs,
    RpmScanTabs,
    SysConfFileTabs,
  },
  data() {
    return {
      ActiveName: "",
    };
  },
  computed: {
    sysConfFileTabsData() {
      return this.$root.data.sysconffile_tabs;
    },
  },
  created() {
    console.log("created @ BaseTabs.vue");
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
  components: { HardwareTabs, ConfigScanTabs, RpmScanTabs, SysConfFileTabs },
};
</script>

<style scoped>
.el-main {
  min-height: calc(100vh - 120px);
}
</style>
