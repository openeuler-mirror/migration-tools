<template>
  <StyledSubheaderBlock subHeader="导入主机说明" />
  <el-card class="cardBox">
    <h2 class="darkblueHeaderText">导入条件</h2>
    <ul class="smallPaddingUl">
      <li>支持的操作系统：CentOS 7/8、RHEL 7/8、Anolis OS、UOS V20</li>
      <li>主机防火墙确保能与统信服务端通信</li>
      <li>
        开启主机 SSHD 服务 |
        <a @click="showMsgBox()" class="textBtn">查看配置</a>
      </li>
      <li>导入的主机信息包含主机信息及 root 权限信息</li>
    </ul>
    <div style="height: 40px"></div>
    <h2 class="darkblueHeaderText">导入主机</h2>
    <ul class="smallPaddingUl">
      <li>
        将需要进行迁移的主机导入到平台中，平台对导入数据进行校验，校验通过的主机将显示在
        <a @click="pushMachineManagementPage()" class="textBtn">主机管理</a>页面
      </li>
      <li>
        请先下载模板，按照模板格式填写数据后再导入，每列数据为必填 |
        <a @click="downloadTemplate()" class="textBtn">下载模板</a>
      </li>
    </ul>
    <div class="confImportCard">
      <div style="margin-right: 30px; width: 150px">导入主机</div>
      <input
        class="input-file"
        type="file"
        ref="upload"
        @change="selectConfXlsx"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      />
      <el-button :icon="iconMore" @click="selectFile"></el-button>
      <el-input
        disabled
        placeholder="请选择文件"
        v-model="uploadFileName"
      ></el-input>
      <el-button
        @click="importMachine()"
        :disabled="uploadBtnDisabled"
        style="margin-left: 10px"
        >导入</el-button
      >
    </div>

    <el-row v-if="isLoading">
      <div>
        <img src="@/assets/loading.png" class="loading" />
      </div>
      <span>导入中...</span>
    </el-row>
    <el-row v-if="isLoadSuccess">
      <div>
        <img src="@/assets/load_success.svg" />
      </div>
      <span>
        导入成功，共导入
        {{ this.importMachineCount }}
        台主机， 请前往
        <a @click="pushMachineManagementPage()" class="textBtn">主机管理</a
        >查看导入结果
      </span>
    </el-row>
    <el-row v-if="isLoadFailed">
      <div>
        <img src="@/assets/load_failed.svg" />
      </div>
      <span>导入失败，请下载指定模板，填写数据后重新导入</span>
    </el-row>
  </el-card>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

// import { ref } from 'vue'
import { markRaw } from "vue";
import { ElMessageBox } from "element-plus";
import { MoreFilled } from "@element-plus/icons-vue";
// import-host-xlsx-template.json contains the base64 encoded template
import xlsxContent from "@/plugins/import-host-xlsx-template.json";
import readXlsxFile from "read-excel-file";
// import { ElUpload } from 'element-plus'

export default {
  name: "ImportMachine",
  components: {
    StyledSubheaderBlock,
  },
  data() {
    return {
      iconMore: markRaw(MoreFilled),
      uploadBtnDisabled: true,
      uploadFile: Object,
      uploadFileName: "",
      //  解析Excel 后的数据
      importExcelData: [],
      // 后台返回后的导出个数
      importMachineCount: 0,
      // 是否正在导入状态
      isLoading: false,
      isLoadSuccess: false,
      isLoadFailed: false,
    };
  },
  methods: {
    selectFile() {
      this.$refs.upload.click();
    },
    showMsgBox: function () {
      // 创建消息提示框
      ElMessageBox.alert("待填充的文案", "SSHD 配置", {
        customStyle: {
          width: "700px",
        },
        callback: (res) => {
          console.log(res);
        },
        closeOnClickModal: true,
        showClose: false,
      });
    },
};
</script>

<style scoped>
.cardBox {
  margin-top: 16px;
}

.darkblueHeaderText {
  color: #002672;
  font-size: 16px;
  margin: 0;
}

.smallPaddingUl {
  padding-left: 20px;
}

.smallPaddingUl > li {
  margin-top: 6px;
}

.textBtn {
  cursor: pointer;
  margin-right: 5px;
}

.confImportCard {
  width: fit-content;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-top: 20px;
  padding: 14px 18px 14px 18px;
  border-radius: 3px;
  border-color: #ffffff;
  box-shadow: 0px 0px 4px #bbbbbb;
}
.input-file {
  display: none;
}
.loading {
  animation: rotate 1s linear infinite;
}
</style>
