<template>
  <StyledSubheaderBlock subHeader="主机管理" />
  <SubheaderInfoCard info="“主机管理”用于管理未完成迁移工作的主机" />
  <el-form :model="filterForm" class="dropMenuContainer">
    <el-form-item class="child">
      <el-input
        clearable
        v-model="filterForm.agent_ip"
        placeholder="主机IP： 🔍️"
      ></el-input>
    </el-form-item>
    <el-form-item class="child">
      <el-input
        clearable
        v-model="filterForm.hostname"
        placeholder="️主机名：🔍️"
      ></el-input>
    </el-form-item>
    <el-form-item class="child">
      <el-select
        clearable
        v-model="filterForm.onlineStatus"
        placeholder="️在线状态："
      >
        <el-option
          v-for="item in onlineOptions"
          :key="item.label"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select
        clearable
        v-model="filterForm.agent_os"
        placeholder="操作系统类型："
      >
        <el-option
          v-for="item in osOptions"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select clearable v-model="filterForm.agent_arch" placeholder="架构：">
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
        v-model="filterForm.migration_type"
        placeholder="迁移类型："
      >
        <el-option
          v-for="item in migrationTypeOptions"
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
        v-model="filterForm.failure_reasons"
        placeholder="失败原因："
      >
        <el-option
          v-for="item in failureReasonsOptions"
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
      <div class="horizontalBtnSet" v-if="!hasSelecton">
        <el-button
          style="margin-right: 15px"
          type="text"
          @click="exportAllMachineList"
          >全部导出</el-button
        >
        <el-dialog
          v-model="dialogVisible"
          :title="dialogTitle"
          width="400px"
          :show-close="false"
        >
          <div style="margin: -25px 0px">
            <div>
              文件将下载到本地，也可稍后前往
              <a @click="toDownloadCenter()" class="textBtn">下载中心</a>下载。
            </div>
          </div>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button
              @click="handleExportFile(fileName, fileData)"
              style="color: white"
              color="#1b67b3"
              >导出</el-button
            >
          </template>
        </el-dialog>
        <el-popover placement="bottom" trigger="click">
          <template #reference>
            <el-button type="text">全部迁移</el-button>
          </template>
          <div class="popoverMenu">
            <div
              class="popoverItem"
              @click="migrateMachines('stock_replacement')"
            >
              存量替换
            </div>
            <div class="popoverItem" @click="migrateMachines('new_expansion')">
              新增扩容
            </div>
          </div>
        </el-popover>
      </div>
      <div class="horizontalBtnSet" v-if="hasSelecton">
        <el-button
          @click="exportSelectionMachine"
          style="margin-right: 15px"
          type="text"
          >导出</el-button
        >
        <el-popover placement="bottom" trigger="click">
          <template #reference>
            <el-button type="text">迁移</el-button>
          </template>
          <!-- 这里应该只处理已勾选的机器 -->
          <div class="popoverMenu">
            <div
              class="popoverItem"
              @click="migrateMachines('stock_replacement')"
            >
              存量替换
            </div>
            <div class="popoverItem" @click="migrateMachines('new_expansion')">
              新增扩容
            </div>
          </div>
        </el-popover>
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
      <!--产品会不会想要让不满足迁移条件的机器对应的 checkbox disable？如果要这样，那这个框框可能要自己实现了-->
      <el-table-column type="selection" :reserve-selection="true" width="40" />
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
        width="180"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="hostname"
        label="主机名称"
        width="180"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="onlineStatus"
        label="在线状态"
        width="100"
      >
        <template #default="scope">
          <span v-if="scope.row.onlineStatus == 'online'">在线</span>
          <span v-else>离线</span>
        </template>
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
        width="100"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="migration_type"
        label="迁移类型"
      >
        <template #default="scope">
          <el-select
            v-model="scope.row.migration_type"
            :disabled="
              scope.row.migrationStatus == 'running' ||
              scope.row.onlineStatus == 'offline'
            "
            @change="modifyMigrationType(scope.row)"
          >
            <el-option
              v-for="item in migrationTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="migrationStatus"
        label="迁移状态"
      >
        <template #default="scope">
          <span v-if="scope.row.migrationStatus == 'not_yet'">未迁移</span>
          <span v-if="scope.row.migrationStatus == 'success'">迁移成功</span>
          <span v-if="scope.row.migrationStatus == 'failed'">迁移失败</span>
          <span v-if="scope.row.migrationStatus == 'running'">迁移中</span>
          <span v-if="scope.row.migrationStatus == 'unknown'">未知状态</span>
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
          <el-button
            @click="migrateMachine(scope.row)"
            type="text"
            :disabled="scope.row.allowMigrateType == 'none'"
            >迁移</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-row>
      <el-col :span="1">
        <el-button
          type="text"
          @click="handleClearSelection"
          style="margin-right: 15px"
        >
          清空选择
        </el-button>
      </el-col>
      <el-col :span="2">
        <span>共选择 {{ multipleSelection.length }} 项</span>
      </el-col>
    </el-row>
    <el-pagination
      background
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[5, 10, 25, 50, 100]"
      :pager-count="11"
      :total="filterTableData.length"
      @size-change="handleSizeChange()"
      @current-change="handleCurrentChange()"
      layout="sizes, prev, pager, next, jumper, slot"
    >
      <template #default>
        <el-button type="text"> 确定 </el-button>
      </template>
    </el-pagination>
  </el-card>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";
import { ElMessageBox } from "element-plus";
import { ElMessage } from "element-plus";
import { ref } from "vue";
import axios from "axios";

export default {
  name: "MachineManagement",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  setup() {
    const tableRef = ref(null); // 引用表格
    const isDataLoaded = false; // 页面是否完成加载
    return {
      tableRef,
      isDataLoaded,
    };
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      machineList: [],
      currentPageMachineList: [],
      hasSelecton: false,
      dialogVisible: false,
      dialogTitle: "",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData: function () {
      axios
        .post("/host_info_display", { mod: "host_info_display" })
        .then((res) => {
          this.machineList = res.data.info;
          for (let i = 0; i < this.machineList.length; i++) {
            // 将从服务器请求来的信息加上自定义字段，目前只加了选中标记
            this.machineList[i].isSelected = false;
            this.machineList[i].migration_type_option = [
              "存量替换",
              "新增扩容",
            ];
            if (
              this.machineList[i].agent_status != "离线" &&
              this.machineList[i].task_status != "迁移中"
            ) {
              this.machineList[i].allowMigrateType = "migrate"; // 迁移目标为 a 版是 migrate，目标为 e 是 analyze，无法迁移是 none
            } else {
              this.machineList[i].allowMigrateType = "none";
            }
          }
          this.currentPageMachineList = this.machineList.slice(
            0,
            this.pageSize
          );
          this.isDataLoaded = true;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleSizeChange: function () {
      // 处理改变页面大小
      this.currentPageMachineList = this.machineList.slice(0, this.pageSize);
      this.currentPage = 1;
      this.setSelect();
    },
    handleCurrentChange: function () {
      // 处理换页
      this.currentPageMachineList = this.machineList.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
      this.setSelect();
    },
    onUserSelect: function (selection, row) {
      row.isSelected = !row.isSelected;
      if (selection.length) {
        this.hasSelecton = true;
      } else {
        this.hasSelecton = false;
      }
    },
    onUserSelectAll: function (selection) {
      for (let i = 0; i < selection.length; i++) {
        selection[i].isSelected = !selection[i].isSelected;
      }
      if (selection.length) {
        this.hasSelecton = true;
      } else {
        this.hasSelecton = false;
      }
    },
    setSelect: function () {
      for (let i = 0; i < this.currentPageMachineList.length; i++) {
        if (this.currentPageMachineList[i].isSelected) {
          this.$nextTick(() => {
            this.tableRef.toggleRowSelection(this.currentPageMachineList[i]);
          });
        }
      }
    },
    exportAllMachineList: function () {
      let filename = "主机列表_202112011118.xlsx"; // 这里应该是从 server 获取到的文件名
      this.dialogTitle = "确定导出" + filename + "吗？";
      this.dialogVisible = true;
    },
    toDownloadCenter: function () {
      this.$router.replace("/download-center");
    },
    analyzeMachines: function () {
      ElMessageBox({
        message:
          "即将对“在线”，且不在“迁移中”的主机进行新增扩容场景下的迁移分析。",
        title: "确定开始迁移分析吗？",
        confirmButtonText: "分析",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          this.$router.replace({ name: "MigrationAnalyze" });
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    analyzeMachine: function (agent_datarow) {
      ElMessageBox({
        message:
          "即将对主机 " +
          agent_datarow.agent_ip +
          " 进行新增扩容场景下的迁移分析。",
        title: "确定开始迁移分析吗？",
        confirmButtonText: "分析",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          this.$router.replace({
            name: "MigrationAnalyze",
            params: { machines: JSON.stringify([agent_datarow]) },
          });
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    migrateMachine: function (agent_datarow) {
      ElMessageBox({
        message: "即将对主机 " + agent_datarow.agent_ip + " 进行迁移。",
        title: "确定开始迁移吗？",
        confirmButtonText: "迁移",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          this.$router.replace({
            name: "MigrateMachine",
            params: { machines: JSON.stringify([agent_datarow]) },
          });
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    migrateMachines: function () {
      // 负责迁移已选中的或全部的主机。根据 this.hasSelecton 值决定
      ElMessageBox({
        // 这里其实还应该加个判断，就是没有可迁移机器的情况。。
        message: "即将对“在线”，且不在“迁移中”的主机进行迁移。",
        title: "确定开始迁移吗？",
        confirmButtonText: "迁移",
        cancelButtonText: "取消",
        showCancelButton: true,
        showClose: false,
      })
        .then((res) => {
          let migrateMachines = [];
          if (this.hasSelecton) {
            this.machineList.forEach((machine) => {
              if (
                machine.isSelected &&
                machine.migration_type == "存量替换" &&
                machine.agent_status == "在线" &&
                machine.task_status != "迁移中"
              ) {
                migrateMachines.push(machine);
              }
            });
          } else {
            this.machineList.forEach((machine) => {
              if (
                machine.migration_type == "存量替换" &&
                machine.agent_status == "在线" &&
                machine.task_status != "迁移中"
              ) {
                migrateMachines.push(machine);
              }
            });
          }
          this.$router.replace({
            name: "MigrateMachine",
            params: { machines: JSON.stringify(migrateMachines) },
          });
        })
        .catch((err) => {
          // 取消，什么事都不会发生
        });
    },
    modifyMigrationType: function (row) {
      let agent_ip = row.agent_ip;
      let migration_type = row.migration_type;
      if (migration_type == "新增扩容") {
        migration_type = "new_expansion";
      } else if (migration_type == "存量替换") {
        migration_type = "stock_replacement";
      }
      console.log(agent_ip, migration_type);
      this.$http.post("/modify_migration_type", {
        mod: "modify_migration_type",
        info: {
          agent_ip: agent_ip,
          migration_type: migration_type,
        },
      });
    },
  },
};
</script>

<style scoped>
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
  justify-content: flex-end;
  width: 135px;
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

.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
