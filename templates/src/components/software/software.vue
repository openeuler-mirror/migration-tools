<template>
  <div>
    <div class="head">
      <div class="head-1"></div>
      <span>导入主机说明</span>
    </div>
    <el-card class="center">
      <el-row class="zi-1">导入条件</el-row>
      <el-row class="zi-3 zi-4"
        >支持的操作系统: CentOS 7/8、RHEL 7/8、Anolis OS</el-row
      >
      <el-row class="zi-3">主机防火墙确保能与统信服务端通信</el-row>
      <!-- <el-row class="zi-3">开启主机SSHD服务|<span class="zi-2" @click="dialogFormVisible = true">查看配置</span></el-row> -->
      <el-row class="zi-3"
        >开启主机SSHD服务|<span class="zi-2"  @click="dialogFormVisible = true">查看配置</span></el-row
      >
      <el-row class="zi-3">导入的主机信息包含主机信息及root权限信息</el-row>

      <div class="center-1">
        <el-row class="zi-1">导入主机</el-row>
        <el-row class="zi-3"
          >将需要进行迁移的主机导入到平台中，平台对导入数据进行校验，校验通过的主机将显示在
          <span class="zi-2" @click="tohostment()">主机管理页面</span></el-row
        >
        <el-row class="zi-3"
          >请先下载模板，按照模板格式填写数据后再导入，每列数据均为必填 |<span
            class="zi-2"
            @click="downUp"
          >
            下载模板</span
          >
        </el-row>
        <el-card class="footer">
          <div class="box">
            <input-excel @getResult="getMyExcelData"></input-excel>
            <!-- <el-input v-model="oneinput" class="input"  placeholder="请选择文件夹"></el-input> -->
            <el-button class="button" type="primary" @click="dao()" :disabled="isDisable" >导入</el-button>

          </div>
        </el-card>

        <el-row class="footer-2" v-show="isshow">
          <div>
            <img src="@/components/software/img/u697.png" class="image" />
          </div>
          <span>导入中...</span></el-row
        >
        <div class="footer-3">
          <el-row v-show="success">
            <img src="./img/u856.svg" alt="" />
            导入成功，共导入<span>{{ this.list }}</span
            >台主机，请前往
            <span class="zi-2" @click="tohostment()">主机管理</span> 查看导入结果</el-row
          >
          <el-row v-show="faild">
            <img src="./img/u1070.svg" alt="" />
            导入失败，请下载指定模板，填写数据后重新导入</el-row
          >
        </div>
      </div>

      <!-- 查看配置弹框 -->
      <el-dialog title="环境配置" :visible.sync="dialogFormVisible">

                <div class="dialogcenter">

                    <el-row class=" row-one font"> <h3> serve 端修改ssh 服务配置，如图1、2、3所示</h3> </el-row>
                    
                    <el-row class="rowcenter row-color"># vim /etc/ssh/ssh_config</el-row>
                    <el-row  class="rowcenter"><img src="./img/3.png" alt="" class="tu"></el-row>
                    <el-row class="rowcenter row-buttom">图1修改ssh_config</el-row>
                    <el-row class="rowcenter row-color"># vim /etc/ssh/sshd_config</el-row>
                    <el-row class="rowcenter"><img src="./img/4.png" alt="" class="tu"></el-row>
                    <el-row class="rowcenter row-buttom">图2 修改sshd_config</el-row>
                    <el-row class="rowcenter"><img src="./img/5.png" alt=""></el-row>
                    <el-row class="rowcenter row-buttom">重启sshd服务。</el-row>
                    <el-row class="rowcenter row-color"># systemctl restart sshd</el-row>

                  </div>

        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">关闭</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import inputExcel from "@/plugins/uploadExcel";
export default {
  data() {
    return {
      mod: "import_host_info",
      dialogFormVisible: false,
      isDisable: false,
      isshow: false,
      success: false,
      faild: false,


      list: 0,
      input: "",
      newdata: [],
    };
  },
  components: {
    inputExcel,
  },
  methods: {
    go() {
      this.$router.push("/pei");
    },
    dao() {
      // console.log(this.input)
      this.isDisable = true
      // setTimeout(() => {
      //   this.isDisable = false
      // }, 10000)

      this.isshow = true;

      this.$http
        .post("/import_host_info", {
          mod: this.mod,
          data: this.newdata,
        })
        .then((res) => {

          if (res.data.data== "success") {
            this.isshow = false;
            this.success = true;
             this.isDisable = false
            this.list = res.data.num;
          } else {
            this.isDisable = false
             this.isshow = false;
            this.faild = true;
          }
        });
    },
    //下载模板
      downUp(){
        const jsonData = [{codeStr:"",tenantName:"",currentVal:""}];
        if (!jsonData.length) return;
        // 表格的列标题 如果出现科学技术法或者其他格式 使用 \t
        let title = 'agent_ip,agent_hostname,agent_password\n';
        jsonData.map(item => {
          let key = {};
          key['agent_ip'] = item.codeStr;
          key['agent_hostname'] = item.tenantName;
          key['agent_password'] = item.currentVal;
          for (let i in key){
            title += `${key[i]},`
          }
          title += '\n'
        });
        // encodeURIComponent 解决中文乱码
        let uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(title);
        // 创建a标签
        let link = document.createElement('a');
        link.href = uri;
        link.download='主机信息模板.xlsx';
        link.click()
      },

    getMyExcelData(data) {
      // data 为读取的excel数据，在这里进行处理该数据
      this.newdata = data;
    },
    tohostment(){
      this.$router.push("/hostment")
    }
  },
};
</script>

<style src="./index.css" scoped>

</style>
