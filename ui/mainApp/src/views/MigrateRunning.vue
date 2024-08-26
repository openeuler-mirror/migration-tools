<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移" />
      <div class="infoCard">
        <div class="infoIcon"></div>
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
                    scope.row.task_status == 2
                  )
                "
                >迁移分析报告</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

import { ElMessageBox, ElMessage } from "element-plus";

export default {
  name: "EnvCheckBeforeMigrate",
  components: {
    StyledSubheaderBlock,
    
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
  },
  created() {
    this.getData();
  },
  methods: {
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
    window.onbeforeunload = null;
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

</style>
