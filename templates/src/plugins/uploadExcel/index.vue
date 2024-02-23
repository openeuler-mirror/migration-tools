<template>
  <span >
    导入主机
    <input
      type="file"
      @change="exportData"
      accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
    />
    <el-button @click="btnClick" class="two">....</el-button>
    <el-input
      v-model="oneinput"
      class="input"
      placeholder="请选择文件夹"
    ></el-input>
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
      document.querySelector(".input-file").click();
    },
    exportData(event) {
      this.oneinput = event.target.files[0].name;

      if (!event.currentTarget.files.length) {
        return;
      }
      const that = this;

      var f = event.currentTarget.files[0];

      var reader = new FileReader();

      FileReader.prototype.readAsBinaryString = function (f) {
        var binary = "";
        var wb;
        var outdata;
        var reader = new FileReader();
        reader.onload = function (e) {
          wb = XLSX.read(binary, {
            type: "binary",
          });
          // console.log(wb);
          outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);

          that.$emit("getResult", outdata);
        };
        reader.readAsArrayBuffer(f);
      };
      reader.readAsBinaryString(f);
    },
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
