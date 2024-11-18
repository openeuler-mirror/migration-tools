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
      <el-tab-pane>
        <template #label>
          <span>配置兼容性评估</span>
        </template>
        <ConfigScanTabs />
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span>RPM 兼容性评估</span>
        </template>
        <RpmScanTabs />
      </el-tab-pane>
      <el-tab-pane v-if="sysConfFileTabsData">
        <template #label>
          <span>系统修改配置</span>
        </template>
        <SysConfFileTabs :tabsData="sysConfFileTabsData" />
      </el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
import GeneralTabs from "./GeneralTabs.vue";
import PackagesTabs from "./PackagesTabs.vue";
import RPMTabs from "./RPMTabs.vue";
import ConfigScanTabs from "../ec/ConfigScanTabs.vue";
import RpmScanTabs from "../ec/RpmScanTabs.vue";
import SysConfFileTabs from "../ec/SysConfFileTabs.vue";
export default {
  name: "BaseTabs",
  components: {
    GeneralTabs,
    PackagesTabs,
    RPMTabs,
    ConfigScanTabs,
    RpmScanTabs,
    SysConfFileTabs,
  },
  data() {
    return {
      activeName: "",
    };
  },
  computed: {
    sysConfFileTabsData() {
      return this.$root.data.sysconffile_tabs;
    },
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
