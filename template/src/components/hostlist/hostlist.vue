<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移主机列表</span>
    </div>
    
    <el-card>
      <img src="./img/u189.png" alt="" />
      即将对列表中的在线主机执行批量迁移工作，点击
      <span class="head-2">删除</span> 将删除对应主机的迁移任务
    </el-card>

    <el-row>
      <el-col :span="2.5" class="col">
        <el-card>AgentID ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>主机IP ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>主机名：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>在线状态：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>操作系统类型：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>架构：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card>迁移状态：全部</el-card>
      </el-col>
      <el-col :span="2.5">
        <el-card>失败原因：全部</el-card>
      </el-col>
    </el-row>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{this.total}}项</el-col>

        <el-col :span="13" class="center-1-2">
          <el-button @click="delarr()" type="danger" plain  icon="el-icon-delete"  size="small"> 删除</el-button></el-col
        >
      </el-row>

       <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center"> </el-table-column>

        <el-table-column  label="迁移时间" align="center" :formatter="formatState">
           <template slot-scope="scope">
                {{timeTranslate(scope.row.task_CreateTime)}}                   
             </template>
        </el-table-column>
        <el-table-column prop="agent_id" label="AgentID" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column label="在线状态" align="center" :formatter="formatState">
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column label="迁移状态" align="center" :formatter="formatState">
          <template slot-scope="scope">
             <el-col v-if="scope.row.task_status=='00' ">未迁移</el-col>
              <el-col v-if="scope.row.task_status!='00' && scope.row.task_status!='08' && scope.row.task_status!='09' ">迁移中</el-col>
              <el-col v-if="scope.row.task_status=='09'">迁移成功</el-col>
              <el-col v-if="scope.row.task_status=='08'">迁移失败</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="failure_reasons" label="历史失败原因" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button type="danger" plain  icon="el-icon-delete"  size="small" @click="del(scope.row.agent_ip)" 
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="list.page"
        :page-sizes="[3, 4, 5, 6]"
        :page-size="list.size"
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
            :disabled="this.tableData.length > 0 ? false : true"
            @click="goti()"
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
      mod: "get_migrated_hosts",
      mod1: "delete_host_info",
      
      total: 0,
      list: {
        page: 1, //当前页码不能为空
        size: 4, //每页显示条数不能为空
      },

      tableData: [
        {
          num: "",
          task_CreateTime: "",
          agent_ip: "",
          agent_id: "",
          hostname: "",
          agent_online_status: "",
          agent_os: "",
          agent_arch: "",
          task_status: "",
          failure_reasons: "",
        },
      ],
      multipleSelection: [],

      deletionarr: [],
    };
  },
  created() {
    this.hostlist();
    //  console.log(this.tableData.length)
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
     
    },

    handleSizeChange(val) {
     
      this.list.size = val;
      this.hostlist();
    },
    handleCurrentChange(val) {
      this.list.page = val;
      this.hostlist();
     
    },
      //  时间转换
    timeTranslate(val) {
      return this.dayjs(val).format("YYYY-MM-DD HH:mm:ss");
    },
    hostlist() {
      this.$http
        .post("/get_migrated_hosts", {
          mod: this.mod,
          page: this.list.page,
          size: this.list.size,
        })
        .then((res) => {
           
          this.tableData = res.data.info;
          this.total = res.data.num;
        });
    },
    // 单选删除
    del(ip) {
      this.$confirm("确定删除所选主机的迁移任务吗, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
      }).then(() => {
          let oneip = ip.split(",");
          this.$http.post("/delete_host_info", {
                mod: this.mod1,
                agent_ip: oneip,
            }).then((res) => {
                this.reload();
            });
          this.$message({type: "success",message: "删除成功!",});
        }).catch(() => {
          this.$message({type: "info",message: "已取消删除",});
        });
    },
    // 选中删除
    delarr() {
         this.$confirm("确定删除所选主机的迁移任务吗, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
      }).then(() => {
         const leght = this.multipleSelection.length;
         for (let i = 0; i < leght; i++) {
            this.deletionarr.push(this.multipleSelection[i].agent_ip);
          }
         var ip = this.deletionarr;
        this.$http.post("/delete_host_info", {
              mod: this.mod1,
              agent_ip: ip,
        }).then((res) => {
            this.reload();
          });
         
          this.$message({type: "success",message: "删除成功!",});
        }).catch(() => {
          this.$message({type: "info",message: "已取消删除",});
        });
     
    },
    goti() {
      if (this.tableData != "") {
        this.$router.push("/migrationtips");
      } else {
        // console.log(111)
      }
    },
    err() {
      this.$confirm("确定退出迁移吗?", "提示", {
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
            message: "已取消",
          });
        });
    },
    formatState: function (row, column, cellValue) {
        if (cellValue == null || cellValue == "") {
           return "--";
      } else {
        // clearInterval(this.timer);
        return cellValue;
      }
     },
  },
};
</script>

<style src="./index.css" scoped>

</style>