<template>
  <StyledSubheaderBlock subHeader="下载中心" />
  <SubheaderInfoCard
    info="“下载中心”用于管理迁移过程中生成的日志和报告，以及其他导出的报告"
  />

  <el-form :model="filterForm" class="dropMenuContainer">
    <el-form-item class="child">
      <el-input
        clearable
        v-model="filterForm.reportName"
        placeholder="️报告名称：🔍️"
      ></el-input>
    </el-form-item>
    <el-form-item class="child">
      <el-select
        clearable
        v-model="filterForm.reportType"
        placeholder="报告类型："
      >
        <el-option
          v-for="item in reportTypes"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
    </el-form-item>
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
      <el-select clearable v-model="filterForm.os" placeholder="操作系统类型：">
        <el-option
          v-for="item in osOptions"
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
        align="center"
        :show-overflow-tooltip="true"
        prop="task_Updatetime"
        label="生成时间"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="report_name"
        label="报告名称"
      />
      <el-table-column
        align="center"
        :show-overflow-tooltip="true"
        prop="report_type"
        label="报告类型"
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
        label="操作"
      >
        <template #default="scope">
          <el-button type="text" @click="downloadReport(scope.row)"
            >下载</el-button
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
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";
import { ElMessage, ElMessageBox } from "element-plus";

export default {
  name: "DownloadCenter",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  computed: {
    osOptions() {
      let cache = new Set(this.allData.map((item) => item.agent_os));
      if (cache.has(undefined)) {
        cache.delete(undefined);
      }
      if (cache.has("")) {
        cache.delete("");
      }
      if (cache.has("--")) {
        cache.delete("--");
      }
      if (cache.has(null)) {
        cache.delete(null);
      }
      return Array.from(cache);
    },
    filterTableData() {
      // reportName
      var filterData = this.allData.filter(
        (item) =>
          !this.filterForm.reportName ||
          item.report_name
            .toLowerCase()
            .includes(this.filterForm.reportName.toLowerCase())
      );
      //  reportType
      filterData = filterData.filter(
        (item) =>
          !this.filterForm.reportType ||
          item.report_type == this.filterForm.reportType
      );
      // ip
      filterData = filterData.filter(
        (item) =>
          !this.filterForm.ip ||
          item.agent_ip.toLowerCase().includes(this.filterForm.ip.toLowerCase())
      );
      // hostname
      filterData = filterData.filter(
        (item) =>
          !this.filterForm.hostname ||
          item.hostname
            .toLowerCase()
            .includes(this.filterForm.hostname.toLowerCase())
      );
      // os
      filterData = filterData.filter(
        (item) => !this.filterForm.os || item.agent_os == this.filterForm.os
      );
      // arch
      filterData = filterData.filter(
        (item) =>
          !this.filterForm.arch || item.agent_arch == this.filterForm.arch
      );

      console.log("正在筛选表单", this.filterForm);
      return filterData;
    },
  },
  data() {
    return {
      filterForm: {
        reportName: "",
        reportType: "",
        ip: "",
        hostname: "",
        os: "",
        arch: "",
      },
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
      allData: [],
      reportTypes: {
        analysis_report: "迁移检测报告-存量替换",
        migration_completed_report: "迁移分析报告",
        analysis_report_add: "迁移检测报告-新增扩容",
        uos_migration_log: "日志",
        export_host_info: "主机列表",
        migration_success_list: "迁移成功主机列表",
      },
      archOptions: [
        { label: "x86_64", value: "x86_64" },
        { label: "aarch64", value: "aarch64" },
      ],
    };
  },
  created() {
    this.getDownloadCenterData();
  },
  methods: {
    getDownloadCenterData: function () {
      this.$http
        .post("/get_download_center_data", { mod: "get_download_center_data" })
        .then((res) => {
          this.allData = res.data.info;
          // 按时间降序排序
          this.allData.sort((a, b) => {
            return new Date(b.task_Updatetime) - new Date(a.task_Updatetime);
          });

          this.allData.forEach((item) => {
            // 处理空值
            if (!item.agent_os) {
              item.agent_os = "--";
            }
            if (!item.agent_arch) {
              item.agent_arch = "--";
            }
            if (!item.hostname) {
              item.hostname = "--";
            }
            if (!item.agent_ip) {
              item.agent_ip = "--";
            }

            // 处理中文报告类型
            for (let key in this.reportTypes) {
              if (item.report_type == this.reportTypes[key]) {
                item.reportType = key;
              }
            }
          });
          this.currentPageData = this.allData.slice(
            (this.currentPage - 1) * this.pageSize,
            this.currentPage * this.pageSize
          );
        });
    },
    downloadReport: function (item) {
      let ip = item.agent_ip;
      if (item.reportType == "export_host_info") {
        ip = "";
      }
      this.$http
        .post(
          "/export_reports",
          {
            mod: "export_reports",
            reports_type: item.reportType,
            agent_ip: ip,
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
            message: "文件将下载到本地，请注意保存。",
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
  },
};
</script>

<style scoped></style>
