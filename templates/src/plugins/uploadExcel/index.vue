<template>
  <span >
    导入主机
    <input
      type="file"
      @change="exportData"
      accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
    />
    <el-button @click="btnClick" class="two">....</el-button>
  </span>
</template>
 
<script>
import XLSX from "xlsx";
export default {
  data() {
    return {
      oneinput: "",
    };
  },
  methods: {
    btnClick() {
      document.querySelector().click();
    },
    exportData(event) {
      this.oneinput = event.target.files[0].name;

      if (!event.currentTarget.files.length) {
        return;
      }
      const that = this;

      var f = event.currentTarget.files[0];

      };
      reader.readAsBinaryString(f);
    },
};
</script>
 
<style>

.input {
  width: 230px;
}
.box {
  font-size: 14px;
}
</style>
