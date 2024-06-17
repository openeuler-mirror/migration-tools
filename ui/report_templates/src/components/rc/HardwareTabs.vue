<template>
  <div>
    <h1>{{ $root.data.hardware_tabs.name }}</h1>
    <div style="width: 100%">
      <el-table :data="displayResult" style="width: 100%">
        <el-table-column prop="vendorName" label="厂商名称" />
        <el-table-column prop="deviceName" label="设备名称" />
        <el-table-column prop="subsystemVendorName" label="子系统厂商名称" />
        <el-table-column prop="subsystemDeviceName" label="子系统设备名称" />
        <el-table-column prop="deviceClassName" label="设备类别名称" />
        <el-table-column label="兼容性" align="center" width="160">
          <template #default="scope">
            <div
              class="compatabilityTag"
              :class="{
                itemTagCompatable: scope.row.compatability == 'Compatible',
                itemTagNeedCheck: scope.row.compatability == 'Need Check',
              }"
            >
              {{ scope.row.compatability }}
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "HardwareTabs",
  data() {
    return {
      displayResult: [],
      hardwareScanResultRaw: [],
    };
  },
  created() {
    console.log("created @ HardwareTabs.vue");
    this.hardwareScanResultRaw = this.$root.data.hardware_tabs.data;
    for (let i = 0; i < this.hardwareScanResultRaw.length; i++) {
      let tmpArr = {};
      tmpArr.vendorID = this.hardwareScanResultRaw[i][0];
      tmpArr.deviceID = this.hardwareScanResultRaw[i][1];
      tmpArr.svID = this.hardwareScanResultRaw[i][2];
      tmpArr.ssID = this.hardwareScanResultRaw[i][3];
      tmpArr.deviceClassID = this.hardwareScanResultRaw[i][4];
      tmpArr.vendorName = this.hardwareScanResultRaw[i][5];
      tmpArr.deviceName = this.hardwareScanResultRaw[i][6];
      tmpArr.subsystemVendorName = this.hardwareScanResultRaw[i][7];
      tmpArr.subsystemDeviceName = this.hardwareScanResultRaw[i][8];
      tmpArr.deviceClassName = this.hardwareScanResultRaw[i][9];
      tmpArr.compatability = this.hardwareScanResultRaw[i][10];
      this.displayResult.push(tmpArr);
    }
  },
};
</script>

<style scoped>
.compatabilityTag {
  padding: 0px 5px 0px 5px;
  border-radius: 4px;
  border-width: 1px;
  text-align: center;
  margin-right: 10px;
  margin-left: 10px;
  color: #606266;
  border-style: solid;
  font-family: "Helvetica";
}
.itemTagCompatable {
  border-color: #ccff99;
  background: #ccff99;
}
.itemTagNeedCheck {
  border-color: #ffcc66;
  background: #ffcc66;
}
</style>
