<template>
  <StyledSubheaderBlock subHeader="迁移记录" />
  <SubheaderInfoCard
    info="“迁移记录”用于记录迁移成功的主机信息，迁移成功的主机将自动移除 Agent"
  />
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
        v-model="filterForm.preMigrationOS"
        placeholder="迁移前OS版本："
      >
        <el-option
          v-for="item in preMigrationOSOptions"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select
        clearable
        v-model="filterForm.postMigrationOS"
        placeholder="迁移后OS版本："
      >
        <el-option
          v-for="item in postMigrationOSOptions"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
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
  </el-form>

  <el-card>
    <div class="cardBoxTitleContainer">
      <p style="font-weight: bold; margin: 4px 0 0 0">
        {{ allData.length }} 项
      </p>
      <div class="horizontalBtnSet">
        <el-button @click="showExportAllMachineListDialog()" type="text"
          >全部导出</el-button
        >
        <el-dialog
          v-model="dialogVisible"
          :title="dialogTitle"
          width="450px"
          :show-close="false"
        >
          <div style="margin: -25px 0px">
            <div>
              文件将下载到本地，也可稍后前往<a
                @click="toDownloadCenter()"
                class="textBtn"
                >下载中心</a
              >下载。
            </div>
          </div>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button
              @click="exportAllMachineList(fileName, fileData, fileType)"
              style="color: white"
              color="#1b67b3"
              >导出</el-button
            >
          </template>
        </el-dialog>
      </div>
    </div>
    <el-table
      :data="
        filterTableData.slice(
          (currentPage - 1) * pageSize,
          currentPage * pageSize
        )
      "
      style="width: 100%"
    >
      <el-table-column
        :show-overflow-tooltip="true"
        prop="create_time"
        label="迁移时间"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="agent_ip"
        label="主机IP"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="hostname"
        label="主机名称"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="agent_os"
        label="迁移前OS版本"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="agent_migration_os"
        label="迁移后OS版本"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="agent_arch"
        label="架构"
      />
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
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";

export default {
  name: "MigrationHistory",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  computed: {
    preMigrationOSOptions() {
      let cache = new Set(this.allData.map((item) => item.agent_os));
      let deleteItems = ["", null, undefined, "--"];
      for (let item of deleteItems) {
        if (cache.has(item)) {
          cache.delete(item);
        }
      }
      return Array.from(cache);
    },

    postMigrationOSOptions() {
      let cache = new Set(this.allData.map((item) => item.agent_migration_os));
      let deleteItems = ["", null, undefined, "--"];
      for (let item of deleteItems) {
        if (cache.has(item)) {
          cache.delete(item);
        }
      }
      return Array.from(cache);
    },

    filterTableData() {
      let filterData = this.allData;
      // ip
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.ip ||
          item.agent_ip.toLowerCase().includes(this.filterForm.ip.toLowerCase())
        );
      });
      // hostname
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.hostname ||
          item.hostname
            .toLowerCase()
            .includes(this.filterForm.hostname.toLowerCase())
        );
      });
      // preMigrationOS
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.preMigrationOS ||
          item.agent_os == this.filterForm.preMigrationOS
        );
      });
      // postMigrationOS
      filterData = filterData.filter((item) => {
        return (
          !this.filterForm.postMigrationOS ||
          item.agent_migration_os == this.filterForm.postMigrationOS
        );
      });
      // arch
      filterData = filterData.filter((item) => {
        return !this.filterForm.arch || item.agent_arch == this.filterForm.arch;
      });

      console.log("正在筛选表单: ", this.filterForm);
      console.log("筛选后的数据: ", filterData);

      return filterData;
    },
  },
  data() {
    return {
      filterForm: {
        ip: "",
        hostname: "",
        preMigrationOS: "",
        postMigrationOS: "",
        arch: "",
      },
      archOptions: [
        { label: "x86_64", value: "x86_64" },
        { label: "aarch64", value: "aarch64" },
      ],
      currentPage: 1,
      pageSize: 5,
      allData: [],
      currentPageData: [],
      dialogVisible: false,
      dialogTitle: "",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData: function () {
      this.$http
        .post("/migration_records", { mod: "migration_records" })
        .then((res) => {
          this.allData = res.data.info;
          // 按时间降序排序
          this.allData.sort((a, b) => {
            return new Date(b.create_time) - new Date(a.create_time);
          });
          this.allData.forEach((item) => {
            //  处理空值， 空值用 '--' 替换
            if (!item.hostname) {
              item.hostname = "--";
            }
            if (!item.agent_os) {
              item.agent_os = "--";
            }
            if (!item.agent_migration_os) {
              item.agent_migration_os = "--";
            }
            if (!item.agent_arch) {
              item.agent_arch = "--";
            }
          });
        });
    },
    handleSizeChange: function () {
      // 处理改变页面大小
      this.currentPageData = this.allData.slice(0, this.pageSize);
      this.currentPage = 1;
    },
    handleCurrentChange: function () {
      // 处理换页
      this.currentPageData = this.allData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
    },
    showExportAllMachineListDialog: function () {
      this.$http
        .post(
          "/export_reports",
          {
            mod: "export_reports",
            reports_type: "migration_success_list",
            agent_ip: "",
            hostname: "",
          },
          { responseType: "blob" }
        )
        .then((res) => {
          this.dialogVisible = true;
          this.fileName =
            res.headers["content-disposition"].split("filename=")[1];
          this.dialogTitle = "确定导出“" + this.fileName + "”吗？";
          this.fileType = res.headers["content-type"];
          this.fileData = res.data;
        })
        .catch((err) => {
          this.$message.error("导出失败，请稍后重试！");
        });
    },
    exportAllMachineList: function (fileName, fileData, fileType) {
      this.dialogVisible = false;
      let blob = new Blob([fileData], { type: fileType });
      let link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = fileName;
      link.click();
    },
    toDownloadCenter: function () {
      this.$router.push("/download-center");
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
  justify-content: space-between;
  width: fit-content;
}
</style>
