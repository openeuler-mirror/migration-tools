<template>
  <StyledSubheaderBlock subHeader="主机管理" />
  <SubheaderInfoCard info="“主机管理”用于管理未完成迁移工作的主机" />
  <el-form class="dropMenuContainer">
    <el-form-item class="child">
      <el-select placeholder="主机IP："></el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="主机名："></el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="在线状态："></el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="操作系统类型："></el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="架构："></el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="迁移状态："></el-select>
    </el-form-item>
    <el-form-item>
      <el-select placeholder="失败原因："></el-select>
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
              @click="dialogVisible = false"
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
            <div class="popoverItem" @click="migrateMachines">存量替换</div>
            <div class="popoverItem" @click="analyzeMachines">新增扩容</div>
          </div>
        </el-popover>
      </div>
      <div class="horizontalBtnSet" v-if="hasSelecton">
        <el-button style="margin-right: 15px" type="text">导出</el-button>
        <el-popover placement="bottom" trigger="click">
          <template #reference>
            <el-button type="text">迁移</el-button>
          </template>
          <!-- 这里应该只处理已勾选的机器 -->
          <div class="popoverMenu">
            <div class="popoverItem" @click="migrateMachines">存量替换</div>
            <div class="popoverItem" @click="analyzeMachines">新增扩容</div>
          </div>
        </el-popover>
      </div>
    </div>
    <el-table
      :v-if="isDataLoaded"
      :data="currentPageMachineList"
      style="width: 100%"
      @select="onUserSelect"
      @select-all="onUserSelectAll"
      ref="tableRef"
    >
      <!--产品会不会想要让不满足迁移条件的机器对应的 checkbox disable？如果要这样，那这个框框可能要自己实现了-->
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
        prop="agent_hostname"
        label="主机名"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="agent_status"
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
        prop="migration_type"
        label="迁移类型"
      >
        <template #default="scope">
          <el-select
            v-model="scope.row.migration_type"
            :disabled="scope.row.task_status == '迁移中'"
            @change="modifyMigrationType(scope.row)"
          >
            <el-option
              v-for="item in scope.row.migration_type_option"
              :key="item"
              :value="item"
            ></el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="task_status"
        label="迁移状态"
      />
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
            v-if="scope.row.migration_type == '存量替换'"
            @click="migrateMachine(scope.row)"
            type="text"
            :disabled="scope.row.allowMigrateType == 'none'"
            >迁移</el-button
          >
          <el-button
            v-if="scope.row.migration_type == '新增扩容'"
            @click="analyzeMachine(scope.row)"
            type="text"
            :disabled="scope.row.allowMigrateType == 'none'"
            >迁移</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[5, 10, 25, 50, 100]"
      :pager-count="11"
      :total="machineList.length"
      @size-change="handleSizeChange()"
      @current-change="handleCurrentChange()"
      layout="sizes, prev, pager, next"
    ></el-pagination>
  </el-card>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";
import { ElMessageBox } from "element-plus";
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
