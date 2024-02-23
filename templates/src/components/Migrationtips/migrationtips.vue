<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移重要提示</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />  即将开始迁移工作，请仔细阅读一下提示
    </el-card>
    <el-card class="center">
      <el-row  class="center-1">重要提示 </el-row>
      <el-row class="center-2">1.迁移一旦开始，过程不可逆。请确保您已将系统的数据与设置进行【完整备份】。</el-row>
      <el-row class="center-2">2.迁移前请获得管理员许可,再进行迁移工作。</el-row>
      <el-row class="center-2">3.请提前获取[统信服务器操作系统V20]的软件仓库地址。</el-row>
      <el-row class="center-2">4.迁移过程中请保证稳定的网络连接。</el-row>
      <el-row class="center-2">5.迁移过程中请不要在迁移主机上进行任何操作。</el-row>
      <el-row class="center-2"> 6.请确保在'/var/cache'中至少有10GB的可用空间。 </el-row>
    </el-card>
    <div class="footer">
      <div>
        <el-row>
          <el-button @click="err()">取消</el-button>

          <el-button @click=go()>下一步</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mod:"close_tool"
    }
  },
  methods: {
    err(){
      this.$confirm('确定退出吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$http.post("/close_tool",{
               mod:this.mod
          }).then((res)=>{
            this.$router.push("/hostment")
          })
          this.$message({type: 'success',message: '退出成功!'});
        }).catch(() => {
          this.$message({type: 'info',message: '用户已取消'});
        });
    },
    go(){
      this.$router.push("/inspect")
    }
  },
};
</script>

<style src="./index.css" scoped>

</style>
