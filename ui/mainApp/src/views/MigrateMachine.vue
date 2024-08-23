<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移主机" />
      <div class="infoCard">
        <div class="infoIcon">i</div>
        <div>
          即将对列表中的主机执行批量迁移{{ desc }}，点击
          <span style="color: #1b67b3">删除</span> 将删除对应主机的迁移任务
        </div>
      </div>
      <el-form :model="filterForm" class="dropMenuContainer">
        <el-form-item class="child">
          <el-input
            clearable
            v-model="filterForm.ip"
            placeholder="主机IP： 🔍️"
          ></el-input>
        </el-form-item>
        <el-form-item class="child">
          <el-input
            clearable
            v-model="filterForm.hostname"
            placeholder="️主机名称：🔍️"
          ></el-input>
        </el-form-item>
        <el-form-item class="child">
          <el-select
            clearable
            v-model="filterForm.onlineStatus"
            placeholder="️在线状态："
          >
            <el-option
              v-for="item in onlineStatusOptions"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="child">
          <el-select
            clearable
            v-model="filterForm.os"
            placeholder="操作系统类型："
          >
          </el-select>
        </el-form-item>
        <el-form-item class="child">
          <el-select clearable v-model="filterForm.arch" placeholder="架构：">
            <el-option
              v-for="item in archOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item class="child">
          <el-select
            clearable
            v-model="filterForm.migrationStatus"
            placeholder="迁移状态："
          >
            <el-option
              v-for="item in migrationStatusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select
            clearable
            v-model="filterForm.failureReason"
            placeholder="失败原因："
          >
            <el-option
              v-for="item in failureReasonOptions"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-card>
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
          <div class="horizontalBtnSet" v-if="hasSelecton">
            <el-button type="text" @click="deleteSelectedMachine()"
              >删除</el-button
            >
          </div>
        </div>
        <el-table
          :v-if="isDataLoaded"
          :data="
            filterTableData.slice(
              (currentPage - 1) * pageSize,
              currentPage * pageSize
            )
          "
          style="width: 100%"
          @selection-change="handleSelectionChange"
          :row-key="(row) => row.id"
          ref="tableRef"
        >
          <el-table-column
            type="selection"
            :reserve-selection="true"
            width="40"
          />
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
            label="主机名称"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="onlineStatus"
            label="在线状态"
            width="100"
          >
          </el-table-column>
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
            prop="migrationStatus"
            label="迁移状态"
          >
            <template #default="scope">
              <span v-if="scope.row.migrationStatus == 'not_yet'">未迁移</span>
              <span v-if="scope.row.migrationStatus == 'success'"
                >迁移成功</span
              >
              <span v-if="scope.row.migrationStatus == 'failed'">迁移失败</span>
              <span v-if="scope.row.migrationStatus == 'running'">迁移中</span>
              <span v-if="scope.row.migrationStatus == 'unknown'"
                >未知状态</span
              >
            </template>
          </el-table-column>
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            prop="failure_reasons"
            label="历史失败原因"
          />
          <el-table-column
            align="center"
            :show-overflow-tooltip="true"
            label="操作"
          >
            <template #default="scope">
              <el-button type="text" @click="deleteMachine(scope.row)"
                >删除</el-button
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
          :total="filterTableData.length"
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
        :disabled="!machineList.length"
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
import { ref } from "vue";

export default {
  name: "MigrateMachine",
  components: {
    StyledSubheaderBlock,
  },
  setup() {
    const tableRef = ref(null); // 引用表格
    const isDataLoaded = false; // 页面是否完成加载
    return {
      tableRef,
      isDataLoaded,
    };
  },

  computed: {
    failureReasonOptions() {
      let cache = new Set(this.machineList.map((item) => item.failure_reasons));
      let deleteItems = ["--", null, undefined, ""];
      for (let item of cache) {
        if (deleteItems.includes(item)) {
          cache.delete(item);
        }
      }
      return cache;
    },

    filterTableData() {
      let filterData = this.machineList;

      //  ip
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.ip || item.agent_ip.includes(this.filterForm.ip)
        );
      });
      //  hostname
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.hostname ||
          item.hostname
            .toLowerCase()
            .includes(this.filterForm.hostname.toLowerCase())
        );
      });
      //  online status
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.onlineStatus ||
          item.onlineStatus == this.filterForm.onlineStatus
        );
      });
      //  os
      filterData = filterData.filter((item) => {
        return !this.filterForm.os || item.agent_os == this.filterForm.os;
      });
      //  arch
      filterData = filterData.filter((item) => {
        return !this.filterForm.arch || item.agent_arch == this.filterForm.arch;
      });
      // migration status
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.migrationStatus ||
          item.migrationStatus == this.filterForm.migrationStatus
        );
      });
      // failure reason
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.failureReason ||
          item.failure_reasons == this.filterForm.failureReason
        );
      });

      console.log("正在筛选数据", this.filterForm);
      return filterData;
    },
  },

  data() {
    return {
      filterForm: {
        ip: "",
        hostname: "",
        onlineStatus: "",
        os: "",
        arch: "",
        migrationStatus: "",
        failureReason: "",
      },
      onlineStatusOptions: [
        { label: "在线", value: "online" },
        { label: "离线", value: "offline" },
        { label: "agent 安装中", value: "installing" },
      ],
      archOptions: [
        { label: "x86_64", value: "x86_64" },
        { label: "aarch64", value: "aarch64" },
      ],
      migrationStatusOptions: [
        { label: "未迁移", value: "not_yet" },
        { label: "迁移中", value: "running" },
        { label: "分析中", value: "checking" },
        { label: "环境检查失败", value: "env_failed" },
        { label: "迁移失败", value: "failed" },
      ],
      currentPage: 1,
      pageSize: 5,
      machineList: [],
      currentPageMachineList: [],
      hasSelecton: false,
      migrationType: "",
      desc: "",
    };
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
      console.log("params", this.$route.params);
      this.migrationType = JSON.parse(this.$route.params.migrationType);
      if (this.migrationType == "stock_replacement") {
        this.desc = "工作";
      }
      if (this.migrationType == "new_expansion") {
        this.desc = "分析";
      }
      this.machineList = JSON.parse(this.$route.params.machines);
      for (let i = 0; i < this.machineList.length; i++) {
        this.machineList[i].isSelected = false;
      }
      this.currentPageMachineList = this.machineList.slice(0, this.pageSize);
      this.isDataLoaded = true;
    },
    handleSelectionChange(val) {
      this.hasSelecton = val.length > 0;
      this.multipleSelection = val;
      console.log("选中的机器", this.multipleSelection);
    },
    deleteMachine: function (row) {
      ElMessageBox({
        title: "确定删除所选主机的迁移任务吗？",
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          for (let i = 0; i < this.machineList.length; i++) {
            if (this.machineList[i].agent_ip == row.agent_ip) {
              this.machineList.splice(i, 1); // 删掉用户选择删除的
            }
          }
          // 处理当前行是否为选中后点击 操作 删除
          if (row) {
            this.$refs.tableRef.toggleRowSelection(row, false);
          }
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    deleteSelectedMachine: function () {
      ElMessageBox({
        title: "确定删除所选主机的迁移任务吗？",
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          let tmpList = this.machineList;
          for (let i = 0; i < tmpList.length; i++) {
            for (let j = 0; j < this.multipleSelection.length; j++) {
              if (tmpList[i].id == this.multipleSelection[j].id) {
                this.machineList.splice(i, 1); // 删掉用户选择删除的
              }
            }
          }
          this.multipleSelection = [];
          this.hasSelecton = false;
          this.$refs.tableRef.clearSelection();
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    cancelMigrate: function () {
      this.$router.push("machine-management");
    },
    nextStep: function () {
      this.$router.replace({
        name: "MigrationNotice",
        params: {
          machines: JSON.stringify(this.machineList),
          migrationType: JSON.stringify(this.migrationType),
        },
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
  beforeRouteLeave(to, from, next) {
    if (to.name === "MigrationNotice") {
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

.smallPaddingUl {
  padding-left: 20px;
}

.smallPaddingUl > li {
  margin-top: 6px;
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
</style>
>
