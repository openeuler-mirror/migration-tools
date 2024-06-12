<template>
  <el-main>
    <div>
      <h1>配置兼容性评估</h1>
      <div id="headerInfo">
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">系统架构:</el-col>
          <el-col :span="18" style="margin-top: 5px">{{
            confScanResult.arch
          }}</el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">迁移类型:</el-col>
          <el-col :span="18" style="margin-top: 5px">{{
            confScanResult.desc
          }}</el-col>
        </el-row>
      </div>
    </div>
    <div id="configlist" style="margin-top: 60px">
      <div class="toolBarBox">
        <div class="left">
          <h2 id="configListHeader">系统配置列表</h2>
        </div>
      </div>
    </div>
    <div style="width: 100%" v-if="isDataLoaded">
      <el-table :data="onShowConfList" style="width: 100%">
        <el-table-column prop="oldVal" label="当前系统配置" />
        <el-table-column prop="newVal" label="对应 UnionTechOS 系统配置" />
        <el-table-column label="兼容性" width="130px" align="center">
          <template #default="scope">
            <div
              class="pkgTag"
              :class="{
                itemTagSame: scope.row.res == 'same',
                itemTagDifferent: scope.row.res == 'different',
              }"
            >
              {{ scope.row.res }}
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-button
      type="primary"
      class="loadMoreButton"
      @click="loadAllConfList()"
      v-if="!isShowingAllConf"
      >点击加载剩余数据</el-button
    >
    <el-button
      type="primary"
      class="loadMoreButton"
      @click="foldConfList()"
      v-if="isShowingAllConf"
      >点击折叠列表</el-button
    >
    <div id="servicelist" style="margin-top: 60px">
      <div class="toolBarBox">
        <div class="left">
          <h2>系统服务列表</h2>
        </div>
      </div>
    </div>
    <div style="width: 100%" v-if="isDataLoaded">
      <el-table :data="onShowServiceList" style="width: 100%">
        <el-table-column prop="oldVal" label="当前系统服务" />
        <el-table-column prop="newVal" label="对应 UnionTechOS 系统服务" />
        <el-table-column label="兼容性" width="130px" align="center">
          <template #default="scope">
            <div
              class="pkgTag"
              :class="{
                itemTagSame: scope.row.res == 'same',
                itemTagDifferent: scope.row.res == 'different',
              }"
            >
              {{ scope.row.res }}
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-button
      type="primary"
      class="loadMoreButton"
      @click="loadAllServiceList()"
      v-if="!isShowingAllService"
      >点击加载剩余数据</el-button
    >
    <el-button
      type="primary"
      class="loadMoreButton"
      @click="foldServiceList()"
      v-if="isShowingAllService"
      >点击折叠列表</el-button
    >
    <div style="height: 50px"></div>
  </el-main>
</template>

<script>
export default {
  name: "ConfigScan",
  data() {
    return {
      isDataLoaded: false,
      isShowingAllConf: false,
      isShowingAllService: false,
      confScanResult: {},
      onShowConfList: [],
      onShowServiceList: [],
    };
  },
  created() {
    this.confScanResult = this.$root.data.confscan_tabs;
    for (let i = 0; i < 10; i++) {
      this.onShowConfList[i] = this.confScanResult.dataTable[0].item[i];
      this.onShowServiceList[i] = this.confScanResult.dataTable[1].item[i];
    }
    this.isDataLoaded = true;
    console.log("loaded");
  },
  methods: {
    loadJSON: function (json) {
      return new Promise((resolve, reject) => {
        try {
          return resolve(JSON.parse(json));
        } catch (e) {
          return reject(e);
        }
      });
    },
    loadAllConfList: function () {
      new Promise((resolve) => {
        this.onShowConfList = this.confScanResult.dataTable[0].item;
        this.isShowingAllConf = true;
        return resolve();
      }).then(() => {
        window.scrollTo(0, 280);
      });
    },
    foldConfList: function () {
      this.onShowConfList = [];
      for (let i = 0; i < 10; i++) {
        this.onShowConfList[i] = this.confScanResult.dataTable[0].item[i];
      }
      this.isShowingAllConf = false;
    },
    loadAllServiceList: function () {
      new Promise((resolve) => {
        this.onShowServiceList = this.confScanResult.dataTable[1].item;
        this.isShowingAllService = true;
        return resolve();
      }).then(() => {});
    },
    foldServiceList: function () {
      this.onShowServiceList = [];
      for (let i = 0; i < 10; i++) {
        this.onShowServiceList[i] = this.confScanResult.dataTable[1].item[i];
      }
      this.isShowingAllService = false;
    },
  },
};
</script>

<style scoped>
.el-main {
  min-height: calc(100vh - 120px);
}
.infoItemLineMargin {
  margin-top: 10px;
}
.infoItemTitle {
  color: #606266;
}
.toolBarBox {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.left {
  vertical-align: center;
  float: left;
}
.right {
  vertical-align: center;
  float: right;
}
.line {
  width: 99%;
  height: 0;
  border-top: 1px solid var(--el-border-color-base);
}
.provideColumnTitle {
  margin: 3px 10px 0px 2px;
  padding: 0px 4px 0px 2px;
}
.provideItem {
  margin: 3px 10px 0px 2px;
  padding: 0px 4px 0px 2px;
}
.provideItem:hover {
  margin: 3px 10px 0px 4px;
  padding: 0px 4px 0px 4px;
  border-radius: 3px;
  background: #ffffff;
  box-shadow: 2px 2px 4px #c2c2c2, -2px -2px 4px #f0eeee;
}
.pkgTag {
  padding: 0px 5px 0px 5px;
  border-radius: 4px;
  border-width: 1px;
  width: 90px;
  text-align: center;
  margin-right: 10px;
  margin-left: 10px;
  color: #606266;
  border-style: solid;
  font-family: "Helvetica";
}
.itemTagSame {
  border-color: #ccff99;
  background: #ccff99;
}
.itemTagDifferent {
  border-color: #ffcc66;
  background: #ffcc66;
}
.loadMoreButton {
  width: 100%;
  height: 30px;
  margin: 10px 10px 10px 4px;
}
</style>
