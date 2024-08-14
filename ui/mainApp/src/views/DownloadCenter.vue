<template>
  <StyledSubheaderBlock subHeader="下载中心" />
  <SubheaderInfoCard
    info="“下载中心”用于管理迁移过程中生成的日志和报告，以及其他导出的报告"
  />

  <el-form class="dropMenuContainer">
    <el-form-item class="child">
      <el-select placeholder="报告名称："> </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="报告类型："> </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="主机IP："> </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="主机名："> </el-select>
    </el-form-item>
    <el-form-item class="child">
      <el-select placeholder="操作系统类型："> </el-select>
    </el-form-item>
    <el-form-item>
      <el-select placeholder="架构："> </el-select>
    </el-form-item>
  </el-form>

  <el-card>
    <div class="cardBoxTitleContainer">
      <p style="font-weight: bold; margin: 4px 0 0 0">
        {{ allData.length }} 项
      </p>
    </div>
    <el-table :data="currentPageData" style="width: 100%">
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
        label="主机名"
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
      :total="allData.length"
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

export default {
  name: "DownloadCenter",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      currentPageData: [],
      allData: [],
    };
  },
  created() {
    this.getDownloadCenterData();
  },
  methods: {
    getDownloadCenterData: function () {
      let a = `{     
                "num":18,
                "info":[
	            {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }, {
                    "task_Updatetime":"xxxxx",
                    "report_name":"xxxxx",
                    "report_type":"xxxxx",
                    "agent_ip":"xxxxx",
                    "hostname":"xxxxx",
                    "agent_os":"xxxxx",
                    "agent_arch":"xxxxx"
                }]}`;
      this.allData = JSON.parse(a).info;
      this.currentPageData = this.allData.slice(0, this.pageSize);
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
    downloadReport: function (reportIndex) {
      // 文档中没找到对应 API
      console.log("TODO: should download " + reportIndex);
    },
  },
};
</script>

<style scoped></style>
