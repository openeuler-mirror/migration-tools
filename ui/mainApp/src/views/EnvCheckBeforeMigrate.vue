<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock :subHeader="title" />
      <div class="infoCard">
        <div class="infoIcon">i</div>
        <div>
          对列表中的主机执行{{ title }}，迁移检测报告可在报告生成后，前往
          下载中心 下载
        </div>
      </div>
      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
          <div class="horizontalBtnSet">
            <el-button :disabled="isAllChecking" type="text" @click="getAllData"
              >开始检查</el-button
            >
          </div>
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
            label="检查进度"
            align="center"
            width="250"
          >
            <template #default="scope" align="center">
              <div v-if="scope.row.task_status == 0 && !scope.row.isChecking">
                <span>未执行</span>
              </div>
              <div
                v-if="scope.row.task_status == 1 || scope.row.isChecking"
                class="progress"
              >
                <span>检查中...</span>
                <el-progress :percentage="scope.row.progress"></el-progress>
              </div>
              <div v-if="scope.row.task_status == 2 && !scope.row.isChecking">
                <el-row justify="center">
                  <div>
                    <img src="@/assets/load_success.svg" />
                  </div>
                  <span style="margin-left: 10px">检查成功</span>
                </el-row>
              </div>
              <div v-if="scope.row.task_status == 3 && !scope.row.isChecking">
                <el-row justify="center">
                  <div>
                    <img src="@/assets/load_failed.svg" />
                  </div>
                  <span style="margin-left: 10px">检查失败</span>
                </el-row>
              </div>
              <div v-if="scope.row.task_status == 4 && !scope.row.isChecking">
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
          >
            <template #default="scope">
              <el-button
                type="text"
                :disabled="scope.row.isChecking"
                @click="getData(scope.row)"
                >检查</el-button
              >
              <el-button
                type="text"
                :disabled="
                  !(
                    scope.row.agent_online_status == 0 &&
                    (scope.row.task_status == 2 || scope.row.task_status == 4)
                  )
                "
                @click="exportMigrationReport(scope.row)"
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
          :total="machineList.length"
          layout="sizes, prev, pager, next, jumper, slot"
        >
          <template #default>
            <el-button type="text"> 确定 </el-button>
          </template>
        </el-pagination>
      </el-card>
    </div>
    <div v-if="isStockReplacementType" class="footerBar">
      <el-button
        @click="cancelMigrate()"
        type="text"
        style="width: 130px; color: #1b67b3"
        >取消</el-button
      >
      <el-button
        @click="nextStep()"
        :disabled="isSomeChecking"
        style="width: 130px; color: white"
        color="#1b67b3"
        >下一步</el-button
      >
    </div>
    <div v-if="isNewExpansionType" class="footerBar">
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
  computed: {
    isNewExpansionType() {
      return this.migrationType == "new_expansion";
    },
    isStockReplacementType() {
      return this.migrationType == "stock_replacement";
    },
    isAllFinished() {
      return this.machineList.every(
        (item) =>
          item.task_status == 2 ||
          item.task_status == 3 ||
          item.task_status == 4
      );
    },
    isAllChecking() {
      return this.machineList.every((item) => item.isChecking == true);
    },
    isSomeChecking() {
      return this.machineList.some((item) => item.isChecking == true);
    },
  },
  data() {
    return {
      migrationType: "",
      machineList: [],
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
      timer: null,
      title: "",
    };
  },
  created() {
    this.initData();
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
    getAllData: function () {
      let cacheIpList = [];
      //  排除掉正在检查的
      this.machineList.forEach((item) => {
        if (!item.isChecking) {
          cacheIpList.push(item.agent_ip);
          item.isChecking = true;
        }
      });
      let post_mod = "check_environment";
      if (this.migrationType == "new_expansion") {
        post_mod = "check_add_environment";
      }
      this.$http
        .post("/" + post_mod, {
          mod: post_mod,
          agent_ip: cacheIpList,
        })
        .then((response) => {
          this.timer = setInterval(() => {
            let post_mod = "get_environment_data";
            if (this.migrationType == "new_expansion") {
              post_mod = "get_add_environment_data";
            }
            if (cacheIpList.length == 0) {
              return;
            }
            this.$http
              .post("/" + post_mod, {
                mod: post_mod,
                agent_ip: cacheIpList,
              })
              .then((res) => {
                let freshData = res.data.info;
                this.machineList.forEach((machine) => {
                  let item = freshData.find((findItem) => {
                    return findItem.agent_ip == machine.agent_ip;
                  });
                  if (item) {
                    machine.task_status = item.task_status;
                    machine.progress = item.progress;
                    machine.isChecking = true;
                    if (
                      machine.task_status == 2 ||
                      machine.task_status == 3 ||
                      machine.task_status == 4
                    ) {
                      machine.isChecking = false;
                      //  remove machine.ip from cacheIpList
                      cacheIpList = cacheIpList.filter((ip) => {
                        return ip != machine.agent_ip;
                      });
                    }
                  }
                });
              });
          }, 5000);
        });
    },

    getData: function (rowData) {
      this.machineList.forEach((item) => {
        if (item.agent_ip == rowData.agent_ip) {
          item.isChecking = true;

          let agentIpGroup = [rowData.agent_ip];

          let post_mod = "check_environment";
          if (this.migrationType == "new_expansion") {
            post_mod = "check_add_environment";
          }
          this.$http
            .post("/" + post_mod, {
              mod: post_mod,
              agent_ip: agentIpGroup,
            })
            .then((response) => {
              item.timer = setInterval(() => {
                let post_mod = "get_environment_data";
                if (this.migrationType == "new_expansion") {
                  post_mod = "get_add_environment_data";
                }
                this.$http
                  .post("/" + post_mod, {
                    mod: post_mod,
                    agent_ip: agentIpGroup,
                  })
                  .then((res) => {
                    let freshData = res.data.info;
                    this.machineList.forEach((machine) => {
                      let item = freshData.find((findItem) => {
                        return findItem.agent_ip == machine.agent_ip;
                      });
                      if (item) {
                        machine.task_status = item.task_status;
                        machine.progress = item.progress;

                        //  如果检查成功或失败，则清除定时器
                        if (
                          machine.task_status == 2 ||
                          machine.task_status == 3 ||
                          machine.task_status == 4
                        ) {
                          machine.isChecking = false;
                          clearInterval(machine.timer);
                          machine.timer = null;
                        }
                      }
                    });
                  });
              }, 5000);
            });
        }
      });
    },

    initData: function () {
      if (this.$route.params.machines === undefined) {
        console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
        this.$router.push("/");
        return;
      }
      this.migrationType = JSON.parse(this.$route.params.migrationType);
      if (this.migrationType == "new_expansion") {
        this.title = "迁移分析";
      }
      if (this.migrationType == "stock_replacement") {
        this.title = "迁移前系统环境检查";
      }

      this.machineList = JSON.parse(this.$route.params.machines);
      console.log("machineList", this.machineList);
      this.machineList.forEach((element) => {
        element.progress = 0;
        element.task_status = 0;
        element.timer = null;
        element.isChecking = false;
      });

      let agentIpGroup = this.machineList.map((item) => {
        return item.agent_ip;
      });

      this.$http.post("/modify_task_status", {
        mod: "modify_task_status",
        agent_ip: agentIpGroup,
      });
    },

    progressFormat: function (value) {
      return "";
    },
    exportMigrationReport: function (item) {
      let reportType = "analysis_report";
      if (this.migrationType == "new_expansion") {
        reportType = "analysis_report_add";
      }
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
    cancelMigrate: function () {
      this.$router.replace("machine-management");
    },
    nextStep: function () {
      if (this.migrationType == "new_expansion") {
        this.$router.push("/");
        return;
      }
      ElMessageBox({
        // 这里其实还应该加个判断，就是没有可迁移机器的情况。。
        message:
          "迁移工作即将开始，请确保稳定的网络连接。迁移开始后会禁用主机的自动更新功能，迁移过程不可逆，请确保您的数据和设置已经【备份】。",
        title: "确定开始迁移吗？",
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          this.$router.replace({
            name: "MigrateRunning",
            params: { machines: JSON.stringify(this.machineList) },
          });
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
      //   this.$router.replace({
      //     name: "EnvCheckBeforeMigrate",
      //     params: { machines: JSON.stringify(this.machineList) },
      //   });
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
    if (to.name === "MigrateRunning" || to.name === "Home") {
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
.progress {
  width: 100%;
}
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
