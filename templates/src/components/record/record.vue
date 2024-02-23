<template>
  <div>
    <div class="head">
      <div class="head-1"></div>
      <span>迁移记录</span>
    </div>
    <el-card class="card">
      <img src="./img/u189.png" alt="" /> "迁移记录"
      用于记录迁移成功的主机信息，迁移成功的主机将自动移除Agent
    </el-card>
    <el-row>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机IP：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机名：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">迁移前os版本：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">迁移后os版本：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">架构：全部</el-card>
      </el-col>
    </el-row>
    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{this.total}}项</el-col>

        <el-col :span="12" class="center-1-2">
          <el-button type="primary" plain icon="el-icon-upload"  size="small " @click="exportData" >全部导出</el-button></el-col
        >
      </el-row>
      <el-table :data="tableData" style="width: 100%" >
        <el-table-column prop="create_time" label="迁移时间" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_migration_os" label="迁移后os版本" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center" :formatter="formatState"> </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center" :formatter="formatState"> </el-table-column>
       
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
         :current-page="list.page"
        :page-sizes="[2, 4,6,8 ]"
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
      mod:"migration_records",
       mod1:"export_reports",
      type:"migration_success_list",
      total:0,
       list: {
        page: 1, //当前页码不能为空
        size: 4, //每页显示条数不能为空
      },
      tableData: [
        {
          num:"",
          create_time:"",
          agent_ip:"",
          hostname:"",
          agent_os:"",
          agent_migration_os:"",
          agent_arch:"",
        },

      ],

    };
  },
  created(){
       this.migrationrecordslist();
  },
  methods: {
    handleSizeChange(val) {
          this.list.size = val;
          this.migrationrecordslist();

    },
    handleCurrentChange(val) {
      this.list.page = val;
        this.migrationrecordslist();

    },
// 数据显示
migrationrecordslist(){
      this.$http.post("/migration_records",{
        mod:this.mod,
         page:this.list.page,
            size:this.list.size
      }).then((res)=>{

        this.tableData=res.data.info
            this.total=res.data.num
      })
},
 formatState: function (row, column, cellValue) {
        if (cellValue == null || cellValue == "") {
           return "--";
      } else {
        // clearInterval(this.timer);
        return cellValue;
      }
     },

 exportData() {
      const h = this.$createElement;
      this.$msgbox({
        title: "提示",
        message: h("p", null, [
          h("p", null, "确定导出“迁移成功主机列表”吗, 是否继续? "),
          h("i", null, "文件将下载到本地，也可稍后前往下载中心下载。"),
        ]),
        showCancelButton: true,
        confirmButtonText: "导出",
        cancelButtonText: "取消",
      })
        .then(() => {
         this.$http.post("/export_reports",{
          mod:this.mod1,
          reports_type:this.type,
          agent_ip:this.tableData.agent_ip,
          hostname:this.tableData.hostname

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

}


};
</script>

<style src="./index.css" scoped>

</style>
