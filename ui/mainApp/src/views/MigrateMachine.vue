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
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";

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
