<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>软件仓库路径</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      请根据一下提示设置软件仓库地址
    </el-card>

    <el-card class="card">
      <el-row class="card-3">设置软件仓库路径</el-row>
      <div class="center">
        <div class="center-1" v-show="conter1">
          <el-row class="row">
            <div class="dian"></div>
            x86_64</el-row
          >

          <el-row class="inputDeep center-1-1" v-show="conter11">
            <p>CentOS 7系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="x86_64_7"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="x86center7 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>

          <el-row class="inputDeep center-1-1" v-show="conter12">
            <p>CentOS 8系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="x86_64_8"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="x86center8 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect1">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success1">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail1">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>
        </div>

        <div class="center-2" v-show="conter2">
          <el-row class="row"
            ><div class="dian"></div>
            aarch_64</el-row
          >

          <el-row class="inputDeep center-1-1" v-show="conter21">
            <p>CentOS 7系列平台</p>

            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="aarch_64_7"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="aarchcenter7 = true" />

            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect2">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success2">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail2">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>

          <el-row class="inputDeep center-1-1" v-show="conter22">
            <p>CentOS 8系列平台</p>
            <div>
              <el-input
                placeholder="请输入平台仓库路径"
                v-model="aarch_64_8"
              ></el-input>
            </div>

            <img src="./img/u1289.svg" alt="" @click="aarchcenter8 = true" />
            <div class="tu-zuo">
              <el-row class="tu-tu" v-show="connect3">
                <div class="img-1">
                  <img src="./img/u697.png" alt="" class="image" />
                </div>
                <span>正在连接软件仓库</span>
              </el-row>
              <el-row class="tu-tu" v-show="success3">
                <div class="tu-zuo-2"></div>
                软件仓库正确</el-row
              >
              <el-row class="tu-tu" v-show="fail3">
                <div class="tu-zuo-3"></div>
                连接失败，请检查您的网络</el-row
              >
            </div>
          </el-row>
        </div>
      </div>
      <el-row class="zi">
        <el-row class="zi-1">例如：</el-row>
        <el-row class="zi-1 zi-3">在线仓库</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/AppStream</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/BaseOS</el-row>
        <el-row class="zi-1 zi-3">http://0.0.0.0/ios/kernel-4.18</el-row>
        <el-row class="zi-1 zi-2 zi-3">请输入：http://0.0.0.0/ios</el-row>
      </el-row>

      <!-- 弹窗1 -->
      <el-dialog
        title="CentOS 7 系列平台-软件仓库路径"
        :visible.sync="x86center7"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="close7">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗2 -->
      <el-dialog
        title="CentOS 8 系列平台-软件仓库路径"
        :visible.sync="x86center8"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="x86center8value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="close8">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗3 -->
      <el-dialog
        title="CentOS 7 系列平台-软件仓库路径"
        :visible.sync="aarchcenter7"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="aarchcenter7value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="aarchclose7">关闭</el-button>
        </div>
      </el-dialog>

      <!-- 弹窗4 -->

      <el-dialog
        title="CentOS 8 系列平台-软件仓库路径"
        :visible.sync="aarchcenter8"
        :close-on-click-modal="false"
      >
        <el-row class="center-4">多个路径请使用 换行 进行分割</el-row>
        <yaml-editor v-model="aarchcenter8value" />

        <div slot="footer" class="dialog-footer">
          <el-button @click="aarchclose8">关闭</el-button>
        </div>
      </el-dialog>
    </el-card>

    <div class="footer">
      <div>
        <el-row>
          <el-button @click="err()">取消</el-button>

          <el-button
            :disabled="
              this.x86_64_7 != '' ||
              this.x86_64_8 != '' ||
              this.aarch_64_7 != '' ||
              this.aarch_64_8 != ''
                ? false
                : true
            "
            @click="go()"
            >下一步</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import YamlEditor from "../YamlEditor/index.vue";
//const yamlData = "- hosts: all\n  become: yes\n  become_method: sudo\n  gather_facts: no\n\n  tasks:\n  - name: \"install {{ package_name }}\"\n    package:\n      name: \"{{ package_name }}\"\n      state: \"{{ state | default('present') }}\"";
export default {
  // name: 'YamlEditorDemo',
  components: { YamlEditor },
  data() {
    return {
      mod: "get_repo_data",
      mod1: "check_repo",
      mod2: "get_repo_arch_info",
      //弹窗
      x86_64_7: "",
      value: "",
      x86center7: false,
      x86_64_8: "",
      x86center8value: "",
      x86center8: false,
      aarch_64_7: "",
      aarchcenter7value: "",
      aarchcenter7: false,
      aarch_64_8: "",
      aarchcenter8value: "",
      aarchcenter8: false,
      // xian: false,
      cons7: "x86_64",
      cons71: "centos7",
      cons72: "centos8",
      cons8: "aarch64",
      cons81: "centos7",
      cons82: "centos8",
      conter1: false,
      conter11: false,
      conter12: false,
      conter2: false,
      conter21: false,
      conter22: false,
      //连接 1
      connect: false,
      success: false,
      fail: false,
      // 连接2
      connect1: false,
      success1: false,
      fail1: false,
      // 连接3
      connect2: false,
      success2: false,
      fail2: false,
      // 连接4
      connect3: false,
      success3: false,
      fail3: false,
      softpathData: [
        {
          agent_arch: "",
          agent_id: "",
          agent_ip: "",
          agent_online_status: "",
          agent_os: "",
          agent_storage: "",
          hostname: "",
          task_CreateTime: "",
        },
      ],
    };
  },
  created() {
    this.getrepoarchinfo();
  },
  mounted() {
    this.softpathData = this.$store.state.tableData;
    this.$store.commit("softData", this.softpathData);
    console.log(this.softpathData)
  },
  destroyed() {
   clearInterval(this.timer)
    this.timer = null
    // console.log("摧毁")

  },
  methods: {
    // 检测数据类型
    getrepoarchinfo() {
      this.$http
        .post("/get_repo_arch_info", {
          mod: this.mod2,
        })
        .then((res) => {
          res.data.info.forEach((item, i) => {
            if (item.agent_arch == "x86_64") {
              this.conter1 = true;
            }
            if (item.agent_arch == "aarch64") {
              this.conter2 = true;
            }
            if (item.agent_os == "centos7" && item.agent_arch == "x86_64") {
              this.conter11 = true;
            }
            if (item.agent_os == "centos8" && item.agent_arch == "x86_64") {
              this.conter12 = true;
            }
            if (item.agent_os == "centos7" && item.agent_arch == "aarch64") {
              this.conter21 = true;
            }
            if (item.agent_os == "centos8" && item.agent_arch == "aarch64") {
              this.conter22 = true;
            }
          });
        });
    },
    close7() {
      this.x86center7 = false;
      this.x86_64_7 = this.value;
      this.value = "";
    },
    close8() {
      this.x86center8 = false;
      this.x86_64_8 = this.x86center8value;
      this.x86center8value = "";
    },
    aarchclose7() {
      this.aarchcenter7 = false;
      this.aarch_64_7 = this.aarchcenter7value;
      this.aarchcenter7value = "";
    },
    aarchclose8() {
      this.aarchcenter8 = false;
      this.aarch_64_8 = this.aarchcenter8value;
      this.aarchcenter8value = "";
    },
  go(){
      this.$http
        .post("/check_repo", {
          mod: this.mod1,
          centos7_x86_64: this.x86_64_7,
          centos8_x86_64: this.x86_64_8,
          centos7_aarch64: this.aarch_64_7,
          centos8_aarch64: this.aarch_64_8,
        })
        .then((res) => {
          // console.log(res);
        });
          this.connect = true;
      this.connect1 = true;
      this.connect2 = true;
      this.connect3 = true;
      this.success = false;
      this.success1 = false;
         this.success2 = false;
          this.success3 = false;
           this.fail = false;
            this.fail1 = false;
             this.fail2 = false;
              this.fail3 = false;
         this.timer = setInterval(() => {

          this.$http
            .post("/get_repo_data", {
              mod: this.mod,
            }).then((res)=>{
              console.log(res)

               if (res.data.centos7_x86 == "success") {
                this.connect = false;
                this.success = true;
              } else {
                this.connect = false;
                this.fail = true;
              }
              // 检查2
              if (res.data.centos8_x86 == "success") {
                this.connect1 = false;
                this.success1 = true;
              } else {
                this.connect1 = false;
                this.fail1 = true;
              }
              // 检查3
              if (res.data.centos7_aarch64 == "success") {
                this.connect2 = false;
                this.success2 = true;
              } else {
                this.connect2 = false;
                this.fail2 = true;
              }
              //  检查4
              if (res.data.centos8_aarch64 == "success") {
                this.connect3 = false;
                this.success3 = true;
              } else {
                this.connect3 = false;
                this.fail3 = true;
              }
              if( res.data.centos7_aarch64 == "success" &&
                res.data.centos7_x86 == "success" &&
                res.data.centos8_aarch64 == "success" &&
                res.data.centos8_x86 == "success"){
                this.$router.push("/coredata");
                } else{
                  // console.log("强制摧毁")
                   clearInterval(this.timer)
                  this.timer = null
                }

            })
         },5000)
  },
    err() {
      this.$confirm("确定退出吗, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
       this.$router.push("/hostment");

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
