<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移" />
      <div class="infoCard">
        <div class="infoIcon">i</div>
        <div>
          对列表中的主机执行迁移，生成的日志和报告也可前往 下载中心 下载
        </div>
      </div>
      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
        </div>
        <el-table
          :data="
            machineList.slice(
              (currentPage - 1) * pageSize,
              currentPage * pageSize
            )
          "
          style="width: 100%"
        >
          <el-table-column
            :show-overflow-tooltip="true"
            prop="task_CreateTime"
            label="迁移时间"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_ip"
            label="主机IP"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="hostname"
            label="主机名称"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_online_status"
            label="在线状态"
            align="center"
          >
            <template #default="scope">
              <span v-if="scope.row.agent_online_status == 0">在线</span>
              <span v-else>离线</span>
            </template>
          </el-table-column>
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_os"
            label="操作系统类型"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_arch"
            label="架构"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="progress"
            label="迁移进度"
            align="center"
            width="250"
          >
            <template #default="scope" align="center">
              <div v-if="scope.row.task_status == 1">
                <span>迁移中...</span>
                <el-progress :percentage="scope.row.progress"></el-progress>
              </div>
              <div v-if="scope.row.task_status == 2">
                <el-row justify="center">
                  <div>
                    <img src="@/assets/load_success.svg" />
                  </div>
                  <span style="margin-left: 10px">迁移成功</span>
                </el-row>
              </div>
              <div v-if="scope.row.task_status == 3">
                <el-row justify="center">
                  <div>
                    <img src="@/assets/load_failed.svg" />
                  </div>
                  <span style="margin-left: 10px">迁移失败</span>
                </el-row>
              </div>
              <div v-if="scope.row.task_status == 4">
                <el-row justify="center">
                  <div>
                    <el-icon size="medium" color="#e6a23c"
                      ><warning-filled
                    /></el-icon>
                  </div>
                  <span style="margin-left: 10px">存在风险</span>
                </el-row>
              </div>
            </template>
          </el-table-column>
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
                  !(
                    scope.row.agent_online_status == 0 &&
                    (scope.row.task_status == 2 || scope.row.task_status == 4)
                  )
                "
                @click="exportMigrationReport(scope.row, 'uos_migration_log')"
                >迁移日志</el-button
              >
              <el-button
                type="text"
                :disabled="
                  !(
                    scope.row.agent_online_status == 0 &&
                    (scope.row.task_status == 2 || scope.row.task_status == 4)
                  )
                "
                @click="
                  exportMigrationReport(scope.row, 'migration_completed_report')
                "
                >迁移分析报告</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          background
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[5, 10, 25, 50, 100]"
          :total="machineList.length"
          layout="sizes, prev, pager, next, jumper, slot"
        >
          <template #default>
            <el-button type="text"> 确定 </el-button>
          </template>
        </el-pagination>
      </el-card>
    </div>
    <div class="footerBar">
      <el-button
        @click="nextStep()"
        :disabled="!isAllFinished"
        style="width: 130px; color: white"
        color="#1b67b3"
        >返回</el-button
      >
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

import { ElMessageBox, ElMessage } from "element-plus";
import { WarningFilled } from "@element-plus/icons-vue";

export default {
  name: "EnvCheckBeforeMigrate",
  components: {
    StyledSubheaderBlock,
    WarningFilled,
  },
  data() {
    return {
      machineList: [],
      freshData: [],
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
      timer: null,
    };
  },
  computed: {
    isAllFinished() {
      return this.machineList.every(
        (item) =>
          item.task_status == 2 ||
          item.task_status == 3 ||
          item.task_status == 4
      );
    },
  },
  created() {
    this.getData();
  },
  methods: {
    refreshData: function (agentIpGroup) {
      this.$http
        .post("/get_system_migration_data", {
          mod: "get_system_migration_data",
          agent_ip: agentIpGroup,
        })
        .then((res) => {
          let isAllFinishFlag = true;
          this.freshData = res.data.info;
          this.machineList.forEach((item) => {
            let freshItem = this.freshData.find((freshItem) => {
              return freshItem.agent_ip == item.agent_ip;
            });
            if (freshItem) {
              item.task_status = freshItem.task_status;
              item.progress = freshItem.progress;
            }
            if (item.task_status == 1) {
              isAllFinishFlag = false;
            }
          });
          if (this.timer && isAllFinishFlag) {
            clearInterval(this.timer);
            this.timer = null;
          }
        });
    },
    getData: function () {
      if (this.$route.params.machines === undefined) {
        console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
        this.$router.push("/");
        return;
      }
      this.machineList = JSON.parse(this.$route.params.machines);
      console.log("machineList", this.machineList);
      this.machineList.forEach((element) => {
        element.progress = 0;
        element.task_status = 0;
      });

      let infoData = [];
      this.machineList.forEach((element) => {
        if (element.selectedTargetKernel == "不迁移内核") {
          element.selectedTargetKernel = "0";
        }
        infoData.push({
          agent_ip: element.agent_ip,
          kernel_version: element.selectedTargetKernel,
        });
      });
      let agentIpGroup = infoData.map((item) => {
        return item.agent_ip;
      });
      this.$http.post("/modify_task_status", {
        mod: "modify_task_status",
        agent_ip: agentIpGroup,
      });
      this.$http
        .post("/system_migration", {
          mod: "system_migration",
          info: infoData,
        })
        .then((res) => {
          console.log(res);
          //   收到回复会开始定时获取数据
          this.timer = setInterval(() => {
            this.refreshData(agentIpGroup);
          }, 5000);
        });
    },
    progressFormat: function (value) {
      return "";
    },
    exportMigrationReport: function (item, reportType) {
      this.$http
        .post(
          "/export_reports",
          {
            mod: "export_reports",
            reports_type: reportType,
            agent_ip: item.agent_ip,
            hostname: item.hostname,
          },
          { responseType: "blob" }
        )
        .then((res) => {
          let fileData = res.data;
          let fileName =
            res.headers["content-disposition"].split("filename=")[1];
          let fileType = res.headers["content-type"];
          ElMessageBox({
            title: "确定导出“" + fileName + "”吗？",
            message: "文件将下载到本地，也可稍后前往下载中心下载。",
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            showCancelButton: true,
            showConfirmButton: true,
            showClose: false,
            type: "info",
          })
            .then(() => {
              let blob = new Blob([fileData], { type: fileType });
              let link = document.createElement("a");
              link.href = window.URL.createObjectURL(blob);
              link.download = fileName;
              link.click();
            })
            .catch(() => {
              ElMessage({
                type: "info",
                message: "已取消导出",
              });
            });
        })
        .catch((err) => {
          this.$message.error("下载失败,请稍后重试");
        });
    },
    nextStep: function () {
      this.$router.push("/");
    },
  },

  mounted() {
    window.onbeforeunload = function (e) {
      e = e || window.event;
      // 兼容IE8和Firefox 4之前的版本
      if (e) {
        e.returnValue = "关闭提示";
      }
      // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
      return "关闭提示";
    };
  },

  unmounted() {
    clearInterval(this.timer);
    window.onbeforeunload = null;
  },
  beforeRouteLeave(to, from, next) {
    if (to.name === "Home") {
      next();
      return false;
    }
    ElMessageBox({
      title: "确定退出迁移吗？",
      confirmButtonText: "退出",
      cancelButtonText: "取消",
      showCancelButton: true,
      showClose: false,
    })
      .then((res) => {
        next();
      })
      .catch((err) => {
        console.log(err);
      });
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

.progressBar {
  width: 30px;
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
