<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      对列表中的主机执行迁移，生成的日志和报告前往 下载中心 下载
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>
      </el-row>
      <el-table
        ref="multipleTable"
        :data="
          transData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center">
        </el-table-column>

        <el-table-column prop="task_CreateTime" label="迁移时间" align="center">
        </el-table-column>
        <el-table-column prop="agent_id" label="AgentID" align="center">
        </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center">
        </el-table-column>
        <el-table-column label="在线状态" align="center">
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center">
        </el-table-column>

        <el-table-column label="迁移进度" align="center">
          <template slot-scope="scope" align="center">
            <el-col v-if="scope.row.task_status == 0">
              <el-row>迁移中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 1">
              <el-row>迁移中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 2">
              <img src="./img/u856.svg" alt="" />迁移成功</el-col
            >
            <el-col v-if="scope.row.task_status == 3">
              <img src="./img/u1070.svg" alt="" /> 迁移失败</el-col
            >
          </template>
        </el-table-column>

        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
              @click="journal(scope.row.agent_ip, scope.row.hostname)"
              icon="el-icon-tickets"
              size="small"
              >迁移日志</el-button
            >
            <el-button
              type="primary"
              plain
              icon="el-icon-document"
              size="small"
              @click="report(scope.row.agent_ip, scope.row.hostname)"
              >迁移分析报告</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[2, 4, 6, 8]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>

    <div class="footer">
      <div>
        <el-row>
          <el-button @click="gohostment()" :disabled="notempty(this.transData)"
            >返回</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mod: "get_system_migration_data",
      mod1: "export_reports",
      mod2: "system_migration",
      reports_type: "migration_logs",
      reports_type1: "migration_analysis_report",
      total: 0,
      currentIndex: "",
      currentPage: 1, //初始页
      pagesize: 4, //    每页的数据
      transData: [
        {
          task_CreateTime: "",
          agent_id: "",
          agent_ip: "",
          hostname: "",
          agent_online_status: "",
          agent_os: " ",
          agent_arch: "",
          task_progress: "",
          task_status: "",
          value1: "",
        },
      ],
      transData1: [
        {
          task_CreateTime: "",
          agent_id: "",
          agent_ip: "",
          hostname: "",
          agent_online_status: "",
          agent_os: " ",
          agent_arch: "",
          task_progress: "",
          task_status: "",
          value1: "",
        },
      ],
      Frame: 0,
      multipleSelection: [],
    };
  },

  created() {
    this.getsystemmigrationdata();
  },

  mounted() {
    // console.log(this.$store.state.tranferdata)
    this.transData1 = this.$store.state.tranferdata;
    // console.log(this.transData1);

    this.transData1.forEach((item) => {
      if (item.value1 == "不迁移内核") {
        item.value1 = this.Frame;
        console.log(this.transData1.agent_ip);
        for (var key in this.transData1) {
          var info = [
            {
              agent_ip: this.transData1[key].agent_ip,
              kernel_version: this.transData1[key].value1,
            },
          ];
          console.log(info);
          this.$http
            .post("/system_migration", {
              mod: this.mod2,
              info: info,
            })
            .then((res) => {
              console.log(res);
            });
        }
      } else {
        for (var key in this.transData1) {
          var info = [
            {
              agent_ip: this.transData1[key].agent_ip,
              kernel_version: this.transData1[key].value1,
            },
          ];
          console.log(info);
          this.$http
            .post("/system_migration", {
              mod: this.mod2,
              info: info,
            })
            .then((res) => {
              console.log(res);
            });
        }
      }
    });
    this.timer = setInterval(() => {
      setTimeout(() => {
        this.getsystemmigrationdata();
      }, 0);
    }, 5000);
  },

  destroyed() {
    clearInterval(this.timer);
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    handleSizeChange: function (size) {
      this.pagesize = size;
      this.getsystemmigrationdata();
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      this.getsystemmigrationdata();
    },
    notempty(data) {
      for (var key in data) {
        //  console.log(data[key].task_status)
        if (data[key].task_status == 0 || data[key].task_status == 1) {
          return true;
        } else {
          return false;
        }
      }
    },

    // 列表
    getsystemmigrationdata() {
      this.$http
        .post("/get_system_migration_data", {
          mod: this.mod,
        })
        .then((res) => {
          this.transData = res.data.info;
          this.total = res.data.num;

          for (var key in this.transData) {
            this.transData1.map((item) => {
              if (this.transData[key].agent_ip == item.agent_ip) {
                this.transData[key].task_CreateTime = item.task_CreateTime;
                this.transData[key].agent_id = item.agent_id;
                this.transData[key].hostname = item.hostname;
                this.transData[key].agent_online_status =
                  item.agent_online_status;
                this.transData[key].agent_os = item.agent_os;
                this.transData[key].agent_arch = item.agent_arch;
                this.transData[key].value1 = item.value1;
              } else {
                // console.log("名称不相等")
              }
            });
          }
        });
    },

    // 迁移日志
    journal(ip, name) {
      const h = this.$createElement;
      this.$msgbox({
        title: "提示",
        message: h("p", null, [
          h("p", null, "确定导出“迁移日志”吗,  "),
          h("p", null, "文件将下载到本地，也可稍后前往下载中心下载。"),
        ]),
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消",
      })
        .then(() => {
          this.$http
            .post("/export_reports", {
              mod: this.mod1,
              reports_type: this.reports_type,
              agent_ip: ip,
              hostname: name,
            })
            .then((res) => {
              // console.log(res)
            });
          this.$message({
            type: "success",
            message: "导出成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消导出",
          });
        });
    },
    // 迁移分析报告
    report(ip, name) {
      const h = this.$createElement;
      this.$msgbox({
        title: "提示",
        message: h("p", null, [
          h("p", null, "确定导出“迁移分析报告”吗,  "),
          h("p", null, "文件将下载到本地，也可稍后前往下载中心下载。"),
        ]),
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消",
      })
        .then(() => {
          this.$http
            .post("/export_reports", {
              mod: this.mod1,
              reports_type: this.reports_type1,
              agent_ip: ip,
              hostname: name,
            })
            .then((res) => {
              // console.log(res)
            });
          this.$message({
            type: "success",
            message: "导出成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消导出",
          });
        });
    },
    gohostment() {
      this.$router.push("/hostment");
    },
  },
};
</script>

<style src="./index.css" scoped>
</style>
