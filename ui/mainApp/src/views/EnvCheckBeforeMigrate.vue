<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移前系统环境检查" />
      <div class="infoCard">
        <div class="infoIcon">i</div>
        <div>
          对列表中的主机执行迁移环境检查，迁移检测报告可在报告生成后，前往
          下载中心 下载
        </div>
      </div>
      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
          <div class="horizontalBtnSet">
            <el-button type="text">开始检查</el-button>
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
            label="主机名"
            align="center"
          />
          <el-table-column
            :show-overflow-tooltip="true"
            prop="agent_online_status"
            label="在线状态"
            align="center"
          />
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
          >
            <template #default="scope" align="center">
              <div v-if="scope.row.task_status == 1">
                <span>检查中...</span>
                <el-progress :percentage="scope.row.progress"></el-progress>
              </div>
              <div v-if="scope.row.task_status == 2">
                <el-row justify="center">
                  <div>
                    <img src="@/assets/load_success.svg" />
                  </div>
                  <span style="margin-left: 10px">检查成功</span>
                </el-row>
              </div>
              <div v-if="scope.row.task_status == 3">
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
            min-width="120"
          >
            <template #default="scope">
              <el-button
                type="text"
                :disabled="
                  scope.row.agent_status == '离线' ||
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
        @click="cancelMigrate()"
        type="text"
        style="width: 130px; color: #1b67b3"
        >取消</el-button
      >
      <el-button
        @click="nextStep()"
        style="width: 130px; color: white"
        color="#1b67b3"
        >下一步</el-button
      >
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

import { ElMessageBox } from "element-plus";
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
  created() {
    this.getData();
  },
  methods: {
    refreshData: function (agentIpGroup) {
      this.$http
        .post("/get_environment_data", {
          mod: "get_environment_data",
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
        element.task_status = 1;
      });

      let agentIpGroup = this.machineList.map((item) => {
        item.agent_ip;
      });
      this.$http
        .post("/check_environment", {
          mod: "check_environment",
          agent_ip: agentIpGroup,
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
        .then((res) => {})
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    cancelMigrate: function () {
      this.$router.replace("machine-management");
    },
    nextStep: function () {
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
    // 导航离开该组件的对应路由时调用
    // 可以访问组件实例 `this`
    // 该导航可以通过 next(false) 来取消。
    if (to.name === "MigrateRunning") {
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
        next(false);
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
