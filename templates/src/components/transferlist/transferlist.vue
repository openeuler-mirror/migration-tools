<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移前系统环境检查</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      对列表中的主机执行迁移环境检查，迁移检测报告可在报告生成后，前往 下载中心
      下载
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>

        <el-col :span="13" class="center-1-2">
          <el-button  type="primary" plain @click="inspect()" icon="el-icon-eleme" size="small" > 开始检查</el-button></el-col
        >
      </el-row>
      <el-table
        ref="multipleTable"
        :data="tranferdata.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >


        <el-table-column prop="task_CreateTime" label="迁移时间" align="center">
        </el-table-column>
        <el-table-column prop="agent_id" label="AgentID" align="center">
        </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center">
        </el-table-column>
        <el-table-column

          label="在线状态"
          align="center"
        >
        <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center">
        </el-table-column>
         <el-table-column label="检查进度" align="center" v-if="progress">
             <el-col>未执行</el-col>
        </el-table-column>


        <el-table-column
          label="检查进度"
          :formatter="formatState"
          align="center"
          v-if="isprogress"
        >
          <template slot-scope="scope">
            <el-col v-if="scope.row.task_status == 0">未执行</el-col>
            <el-col v-if="scope.row.task_status == 1">
              <el-row>执行中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 2"
              ><img src="./img/u856.svg" alt="" /> 执行成功</el-col
            >
            <el-col v-if="scope.row.task_status == 3"
              ><img src="./img/u1070.svg" alt="" /> 执行失败</el-col
            >
          </template>
        </el-table-column>

        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
              @click="checkone(scope.row.agent_ip)"
              icon="el-icon-eleme" size="small"
              >检查</el-button
            >
            <el-button
              type="primary"
              plain
              icon="el-icon-document" size="small"
              @click="testreport(scope.row.agent_ip, scope.row.hostname)"
              >迁移检测报告</el-button
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
          <el-button @click="err()">取消</el-button>

          <el-button
            @click="gotransfer()"
            :disabled="notempty(this.tranferdata)"
            >下一步</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  inject: ["reload"],
  data() {
    return {
      xian1: true,
      xian: true,
      kk: false,
      progress:true,
      isprogress:false,
      total: 0,
       currentIndex: "",
      currentPage: 1, //初始页
      pagesize: 4, //    每页的数据
      mod: "get_environment_data",
      mod1: "check_environment",
      mod2: "export_reports",
      mod3:"modify_task_status",
      reports_type: "migration_detection",

      tranferdata1: [
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
      tranferdata: [
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
      multipleSelection: [],
      jianarr: [],
      Arrid:[]
    };
  },
  created() {
    this.transferlist();

  },
  mounted() {
    this.tranferdata1 = this.$store.state.xin2Data;
    this.timer=setInterval(() => {
        setTimeout(() => {
       this.transferlist();
       console.log("在执行")

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
  this.transferlist();

    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
  this.transferlist();

    },


    // 列表
    transferlist() {
      this.$http
        .post("/get_environment_data", {
          mod: this.mod,

        })
        .then((res) => {
          this.tranferdata = res.data.info;
          this.total = res.data.num;
          for (var key in this.tranferdata) {
            this.tranferdata1.map((item) => {
              if (this.tranferdata[key].agent_ip == item.agent_ip) {
                this.tranferdata[key].task_CreateTime = item.task_CreateTime;
                this.tranferdata[key].agent_id = item.agent_id;
                this.tranferdata[key].hostname = item.hostname;
                this.tranferdata[key].agent_online_status =
                  item.agent_online_status;
                this.tranferdata[key].agent_os = item.agent_os;
                this.tranferdata[key].agent_arch = item.agent_arch;
                this.tranferdata[key].value1 = item.value1;
              } else {
              }
            });
          }
        });
    },

    formatState: function (row, column, cellValue) {
      // console.log(row);
      // console.log(column);
      // console.log(cellValue);
    },
    notempty(data){

         for(var key in data){
           if( data[key].task_status==1){
             return true
           }else{
             return false
           }
         }

    },
    //  全部检查
    inspect() {
      console.log(this.tranferdata)
        this.progress=false
        this.isprogress=true
       this.tranferdata.forEach((item)=>{
       this.Arrid.push(item.agent_ip);

       })
      let ip=this.Arrid
      this.$http.post("/check_environment", {
          mod: this.mod1,
          agent_ip:ip,
        })
        .then((res) => {
          console.log(res);
        });
    },
    // 单选检查
    checkone(ip) {
          this.progress=false
        this.isprogress=true
      let oneip = ip.split(",");
      console.log(oneip)

      this.$http
        .post("/check_environment", {
          mod: this.mod1,
          agent_ip:oneip,
        })
        .then((res) => {
          console.log(res);
          // this.reload();
        });
    },
    // 迁移报告
    testreport(ip, name) {
      const h = this.$createElement;
      this.$msgbox({
        title: "提示",
        message: h("p", null, [
          h("p", null, "确定导出“迁移检测报告”吗,  "),
          h("p", null, "文件将下载到本地，也可稍后前往下载中心下载。"),
        ]),
        showCancelButton: true,
        confirmButtonText: "确定",
        cancelButtonText: "取消",
      })
        .then(() => {
        this.$http.post("/export_reports",{
          mod:this.mod2,
          reports_type:this.reports_type,
          agent_ip:ip,
          hostname:name

        }).then((res)=>{
          // console.log(res)
        })
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
    gotransfer() {
      this.$confirm(
        "迁移工作即将开始，请确保稳定的网络连接。迁移开始后会禁用您的自动更新功能，迁移过程不可逆，请确保您的数据和设置已经【备份】",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
        }
      )
        .then(() => {
          this.$store.commit("gotransfer", this.tranferdata);
          this.$http.post("/modify_task_status",{
            mod:this.mod3
          }).then((res)=>{
            // console.log(res)
          })
          this.$router.push("/transfer");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "用户已取消",
          });
        });
    },
    err() {
      this.$confirm("确定退出吗, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$router.push("/hostment")

          this.$message({
            type: "success",
            message: "退出成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "用户已取消",
          });
        });
    },
  },
};
</script>

<style src="./index.css" scoped>

</style>
