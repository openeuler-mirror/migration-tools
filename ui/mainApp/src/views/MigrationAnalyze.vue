<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移分析" />
      <div class="infoCard">
        <div class="infoIcon">i</div>
        <div>
          对新增扩容场景下，Agent 安装在 UOS V20 的主机进行迁移分析。点击查看
          <a @click="showHelpMessageBox()" class="textBtn">使用说明</a>
        </div>
      </div>
      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ currentPageData.num }} 项
          </p>
          <div class="horizontalBtnSet">
            <el-button type="text">开始检查</el-button>
          </div>
        </div>
        <el-table :data="currentPageData.info" style="width: 100%">
          <el-table-column
            :show-overflow-tooltip="true"
            prop="create_time"
            label="迁移时间"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_ip"
            label="主机IP"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="hostname"
            label="主机名称"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_online_status"
            label="在线状态"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_os"
            label="操作系统类型"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_arch"
            label="架构"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_migration_os"
            label="检查进度"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            label="操作"
            min-width="120"
          >
            <template #default="scope">
              <el-button
                type="text"
                :disabled="
                  scope.row.agent_online_status == '离线' ||
                  scope.row.task_status == '迁移中'
                "
                >检查</el-button
              >
              <el-button type="text" @click="exportMigrationReport()"
                >迁移检测报告</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          background
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[5, 10, 25, 50, 100]"
          :pager-count="11"
          :total="13"
          layout="sizes, prev, pager, next, jumper, slot"
        >
          <template #default>
            <el-button type="text"> 确定 </el-button>
          </template>
        </el-pagination>
      </el-card>
    </div>
    <div class="footerBar">
      <el-button style="width: 130px; color: white" color="#1b67b3"
        >关闭</el-button
      >
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

import { ElMessageBox } from "element-plus";

export default {
  name: "MigrationAnalyze",
  components: {
    StyledSubheaderBlock,
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
    };
  },
  created() {
    this.getData();
  },
  methods: {
    showHelpMessageBox: function () {
      ElMessageBox({
        message:
          "本功能支持统信服务器操作系统 V20 与 CentOS 7 进行迁移分析。包括软件包的 ABI 分析。。。。\n\n在使用时。。。。",
        title: "迁移分析使用说明",
        confirmButtonText: "关闭",
        showClose: false,
      });
    },
    getData: function (page, pageSize) {
      let a = `{
	            "num":18,
	            "info":[
	            {
                    "create_time":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_migration_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "create_time":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_migration_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }]}`;
      this.currentPageData = JSON.parse(a);
    },
    exportMigrationReport: function () {
      let filename =
        "UOS_migration_report_10.0.2.3_cy.server_202109301634.html";
      ElMessageBox({
        message: "文件将下载到本地，也可稍后前往下载中心下载。",
        title: "确定导出“" + filename + "”吗？",
        confirmButtonText: "导出",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
        customStyle: { width: "700px" },
      })
        .then((res) => {
          this.$router.push("/migration-analyze");
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
  },
};
</script>

<style scoped>
.pageContainer {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.footerBar {
  height: 50px;
  margin: 0px -25px -8px -25px;
  padding-right: 25px;
  background-color: #eeeeee;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.textBtn {
  cursor: pointer;
}

.cardBox {
  margin-top: 16px;
}

.cardBoxTitleContainer {
  display: flex;
  justify-content: space-between;
}

.horizontalBtnSet {
  display: flex;
  justify-content: space-between;
  width: fit-content;
}
</style>
