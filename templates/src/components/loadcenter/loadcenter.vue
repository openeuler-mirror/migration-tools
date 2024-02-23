<template>
  <div>
    <div class="head">
      <div class="head-1"></div>
      <span>下载中心</span>
    </div>
    <el-card class="card">
      <img src="./img/u189.png" alt="" />
      "下载中心"用于管理迁移过程中生成的日志和报告，以及其他导出的报告
    </el-card>
    <el-row>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">报告名称：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">报告类型：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机IP：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机名 ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">操作系统类型：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">架构：全部</el-card>
      </el-col>
    </el-row>
    <el-card class="center">
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <!-- <el-table-column type="selection" width="55"> </el-table-column> -->

        <el-table-column prop="report_generation_time" label="生成时间" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column prop="report_name" label="报告名称"  show-overflow-tooltip="" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="report_type" label="报告类型" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center" show-overflow-tooltip="" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center" :formatter="formatState"> </el-table-column>

        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
               icon="el-icon-download"  size="small "
              @click="
                download(
                  scope.row.report_type,
                  scope.row.agent_ip,
                  scope.row.hostname
                )
              "
              >下载</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="list.page"
        :page-sizes="[2, 4, 6, 8]"
        :page-size="list.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mod: "get_download_center_data",
      mod1: "export_reports",
      // 迁移检测报告
      testingtype: "migration_detection",
      //  迁移日志
      journaltype: "migration_logs",
      // 迁移分析报告
      analysistype: "migration_analysis_report",
      // 主机列表
      hostlisttype: "export_host_info",
      // 迁移成功主机列表
      successlisttype: "migration_success_list",
      total: 0,
      list: {
        page: 1, //当前页码不能为空
        size: 4, //每页显示条数不能为空
      },
      tableData: [
        {
          report_generation_time: "",
          report_name: "",
          report_type: "",
          agent_ip: "",
          hostname: "",
          agent_os: "",
          agent_arch: "",
        },
      ],
      multipleSelection: [],
    };
  },
};
</script>

<style src="./index.css" scoped>

</style>
