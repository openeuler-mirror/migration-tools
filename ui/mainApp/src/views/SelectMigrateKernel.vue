<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="选择迁移系统内核版本" />
      <SubheaderInfoCard
        info="请在“迁移后OS内核”列下拉框中，选择迁移到新系统的内核版本"
      />

      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
          <!-- <div class="horizontalBtnSet" v-if="currentPageHasSelection"> -->
          <div class="horizontalBtnSet">
            <el-popover
              v-model:visible="visible"
              placement="bottom"
              trigger="click"
            >
              <template #reference>
                <el-button type="text" @click="visible = true"
                  >选择内核版本</el-button
                >
              </template>
              <!-- 这里应该只处理已勾选的机器 -->
              <div class="popoverMenu">
                <div class="popoverItem" @click="batchOperate">不迁移内核</div>
              </div>
            </el-popover>
          </div>
        </div>
        <el-table
          :data="currentPageMachineList"
          style="width: 100%"
          @select="onUserSelect"
          @select-all="onUserSelectAll"
        >
          <el-table-column type="selection" width="40" />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="task_CreateTime"
            label="迁移时间"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="agent_ip"
            label="主机IP"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="hostname"
            label="主机名"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="agent_online_status"
            label="在线状态"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="agent_os"
            label="操作系统类型"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="agent_arch"
            label="架构"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="agent_kernel"
            label="迁移前OS内核"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            label="迁移后OS内核"
          >
            <template #default="scope">
              <el-select
                v-model="scope.row.selectedTargetKernel"
                placeholder="选择内核"
              >
                <el-option
                  v-for="item in scope.row.agent_repo_kernel"
                  :key="item"
                  :value="item"
                ></el-option>
              </el-select>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[5, 10, 50, 100]"
          :total="machineList.length"
          layout="sizes, prev, pager, next"
        ></el-pagination>
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
        :disabled="!isCheckFinish"
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
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";

import { ElMessageBox } from "element-plus";

export default {
  name: "SelectMigrateKernel",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  created() {
    this.getData();
  },
  data() {
    return {
      visible: false,
      machineList: [],
      currentPageMachineList: [],
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
      currentPageHasSelection: false,
      isSelectNullKernelVersion: false,
      isCheckFinish: false,
    };
  },
  watch: {
    machineList: {
      handler(newValue, oldValue) {
        let res = true;
        this.machineList.forEach((item) => {
          res = res && item.selectedTargetKernel;
          console.log("item.selectedTargetKernel", item.selectedTargetKernel);
          console.log("res", res);
        });
        this.isCheckFinish = res;
      },
      deep: true,
    },
  },
  methods: {
    getData: function (page, pageSize) {
      if (this.$route.params.machines === undefined) {
        console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
        this.$router.push("/");
        return;
      }

      this.machineList = JSON.parse(this.$route.params.machines);
      this.currentPageMachineList = this.machineList.slice(0, this.pageSize);
      console.log("@DEBUG: 获取到的主机列表", this.machineList);
      this.$http
        .post("/check_kernel", {
          mod: "/check_kernel",
          agent_ip: this.machineList.map((item) => item.agent_ip),
        })
        .then((res) => {
        });

      this.freshData(this.machineList.map((item) => item.agent_ip));
      this.currentPageData = this.machineList;
    },
    freshData: function (agent_ips) {
      this.$http
        .post("/get_kernel_data", {
          mod: "/get_kernel_data",
          agent_ip: agent_ips,
        })
        .then((res) => {
          console.log(res.data.info);
          let info = res.data.info;
          for (let i = 0; i < info.length; i++) {
            for (let j = 0; j < this.machineList.length; j++) {
              if (info[i].agent_ip === this.machineList[j].agent_ip) {
                this.machineList[j].agent_repo_kernel =
                  info[i].agent_repo_kernel.split(",");
                this.machineList[j].agent_repo_kernel.unshift("不迁移内核");
                this.machineList[j].agent_kernel = info[i].agent_kernel;
                this.machineList[j].selectedTargetKernel = "";
                break;
              }
            }
          }
        });
    },
    handleSizeChange: function (val) {
      console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.currentPageMachineList = this.machineList.slice(0, val);
    },
    handleCurrentChange: function (val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
      this.currentPageMachineList = this.machineList.slice(
        (val - 1) * this.pageSize,
        val * this.pageSize
      );
    },
    batchOperate: function () {
      this.visible = false;
      this.machineList.forEach((element) => {
        element.selectedTargetKernel = "不迁移内核";
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

  unmouted() {
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

.footerBar {
  height: 50px;
  margin: 0px -25px -8px -25px;
  padding-right: 25px;
  background-color: #eeeeee;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.darkblueHeaderText {
  color: #002672;
  font-size: 16px;
  margin: 0;
}

.cardBox {
  margin-top: 16px;
}

.cardBoxTitleContainer {
  height: 32px;
  display: flex;
  justify-content: space-between;
  margin-top: -10px;
  margin-bottom: 5px;
}

.horizontalBtnSet {
  display: flex;
  justify-content: space-between;
  width: fit-content;
}
.popoverMenu {
  margin: -12px;
  padding: 5px 0 5px 0;
  display: flex;
  flex-direction: column;
}

.popoverItem {
  color: #409eff;
  background-color: #ffffff00;
  text-align: start;
  width: 134px;
  padding: 10px 10px 10px 30px;
  transition: background-color 0.1s;
}

.popoverItem:hover {
  background-color: #f8f8f8;
  transition: background-color 0.1s;
  cursor: pointer;
}
</style>
