<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="检查可用空间" />
      <SubheaderInfoCard
        info="进行迁移需保证 '/var/cache' 中至少有 10GB 的可用空间"
      />
      <el-card class="cardBox">
        <div class="cardBoxTitleContainer">
          <p style="font-weight: bold; margin: 4px 0 0 0">
            {{ machineList.length }} 项
          </p>
        </div>
        <el-table
          :v-if="isDataLoaded"
          :data="currentPageMachineList"
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
            prop="agent_storage"
            label="可用空间"
            align="center"
          >
            <template #default="scope">
              <el-row v-if="scope.row.agent_storage == ''" justify="center">
                <div>
                  <img src="@/assets/loading.png" class="loading" />
                </div>
                <span style="margin-left: 10px">检查中</span>
              </el-row>
              <div v-if="scope.row.agent_storage != ''">
                {{ scope.row.agent_storage }}
              </div>
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
        :disabled="!isCheckFinished"
        >下一步</el-button
      >
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";

import { ElMessageBox } from "element-plus";
import { ref } from "vue";

export default {
  name: "CheckAvalibleSpace",
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
    };
  },
  computed: {
    isCheckFinished() {
      let migrateMachines = [];
      this.machineList.forEach((element) => {
        console.log(
          "element.agent_storage",
          element.agent_storage,
          parseInt(element.agent_storage)
        );
        //  大于 10 G 的主机才迁移
        if (parseInt(element.agent_storage) >= 10) {
          migrateMachines.push(element);
        }
      });
      return migrateMachines.length > 0 ? true : false;
    },
  },
  created() {
    this.getData();
    this.freshData();
  },
  methods: {
    getData: function () {
      if (this.$route.params.machines === undefined) {
        console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
        this.$router.push("/");
        return;
      }
      this.machineList = JSON.parse(this.$route.params.machines);
      this.currentPageMachineList = this.machineList.slice(0, this.pageSize);
      this.isDataLoaded = true;
    },
    freshData: function () {
      // 这里还要加一步从网络获取数据，拿来和已经有的拼起来
      this.$http
        .post("/get_page_data", {
          mod: "/get_page_data",
          agent_ip: this.machineList.map((item) => item.agent_ip),
        })
        .then((res) => {
          this.machineList = res.data.info;
          this.handleSizeChange();
        });
      // 以及通过 server 下发命令的操作，然后后面定时访问，请求来结果拼起来
    },
    handleSizeChange: function () {
      // 处理改变页面大小
      this.currentPageMachineList = this.machineList.slice(0, this.pageSize);
      this.currentPage = 1;
    },
    handleCurrentChange: function () {
      // 处理换页
      this.currentPageMachineList = this.machineList.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
    },
    cancelMigrate: function () {
      this.$router.replace("machine-management");
    },
  },
  beforeRouteLeave(to, from, next) {
    // 导航离开该组件的对应路由时调用
    // 可以访问组件实例 `this`
    // 该导航可以通过 next(false) 来取消。
    if (to.name === "SetRepo") {
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
.loading {
  animation: rotate 1s linear infinite;
}
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

.cardBox {
  margin-top: 16px;
}

.cardBoxTitleContainer {
  display: flex;
  justify-content: space-between;
}
</style>
