<!--
    只要已经填入了的路径检查通过，就可以下一步吗？
    因为用户可能不是需要全填吧，比如用户只有几台 C7 X86 的机器，那岂不是只需要填第一个就行了？

    还有，什么时候触发检查？
    用户每次输入完一个字母就检查一次？
    加个延时也许也可以？
    或者给他加个只在输入框内有值时才显示出来的确定按钮？？？
-->

<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="软件仓库路径" />
      <SubheaderInfoCard info="请根据以下提示设置软件仓库地址" />

      <el-card class="cardBox">
        <h2 class="darkblueHeaderText">设置软件仓库路径</h2>
        <div v-if="isx86Exist">
          <div class="dotStartSmallHeader">
            <div class="roundDot"></div>
            <h4 class="headerText">x86_64</h4>
          </div>
          <div class="repoInputComponent">
            <span class="smallGrayFonts">扩容系统的软件源：</span>
            <input
              v-model="c8x86repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="showDialog('扩容系统的软件源', 'x86_64', 'c8x86repo')"
              size="small"
              class="inputLargeBtn"
            >
              <img src="~@/assets/arrows-angle-expand.svg" />
            </el-button>
            <div class="leftMargin">
              <el-row v-show="isc8x86Connecting">
                <div>
                  <img src="@/assets/loading.png" class="loading" />
                  <span class="leftMargin">正在连接软件仓库......</span>
                </div>
              </el-row>
              <el-row v-show="isc8x86ConnectSuccess">
                <div>
                  <img src="@/assets/load_success.svg" />
                  <span class="leftMargin">软件仓库路径正确</span>
                </div>
              </el-row>
              <el-row v-show="isc8x86ConnectFailed">
                <div>
                  <img src="@/assets/load_failed.svg" />
                  <span class="leftMargin"
                    >连接失败，请检查您的软件仓库设置</span
                  >
                </div>
              </el-row>
            </div>
          </div>
        </div>
        <div v-if="isaarch64Exist">
          <div class="dotStartSmallHeader">
            <div class="roundDot"></div>
            <h4 class="headerText">aarch_64</h4>
          </div>
          <div class="repoInputComponent">
            <span class="smallGrayFonts">扩容系统的软件源：</span>
            <input
              v-model="c8aarch64repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="
                showDialog('扩容系统的软件源', 'aarch_64', 'c8aarch64repo')
              "
              size="small"
              class="inputLargeBtn"
            >
              <img src="~@/assets/arrows-angle-expand.svg" />
            </el-button>
            <div class="leftMargin">
              <el-row v-show="isc8aarch64Connecting">
                <div>
                  <img src="@/assets/loading.png" class="loading" />
                  <span class="leftMargin">正在连接软件仓库......</span>
                </div>
              </el-row>
              <el-row v-show="isc8aarch64ConnectSuccess">
                <div>
                  <img src="@/assets/load_success.svg" />
                  <span class="leftMargin">软件仓库路径正确</span>
                </div>
              </el-row>
              <el-row v-show="isc8aarch64ConnectFailed">
                <div>
                  <img src="@/assets/load_failed.svg" />
                  <span class="leftMargin"
                    >连接失败，请检查您的软件仓库设置</span
                  >
                </div>
              </el-row>
            </div>
          </div>
        </div>
        <div style="margin-top: 25px">
          <div class="smallLighterGrayFonts">例如：</div>
          <div class="smallLighterGrayFonts">在线仓库</div>
          <div class="smallLighterGrayFonts">http://0.0.0.0/iso/AppStream</div>
          <div class="smallLighterGrayFonts">http://0.0.0.0/iso/BaseOS</div>
          <div class="smallLighterGrayFonts">
            http://0.0.0.0/iso/kernel-4.18
          </div>
          <br />
          <div class="smallLighterGrayFonts">请输入： http://0.0.0.0/iso</div>
        </div>
      </el-card>
    </div>
    <div class="footerBar">
      <el-button
        @click="cancelMigrate()"
        type="text"
        style="width: 130px; color: #1b67b3"
        >取消</el-button
      >
      <el-button
        :disabled="
          !(!isx86Exist ^ !c8x86repo) &&
          !(!isaarch64Exist ^ !c8aarch64repo) &&
          !isConnecting &&
          !isConnectSuccess
            ? false
            : true
        "
        @click="checkRepo()"
        style="width: 130px; color: white"
        color="#1b67b3"
        >下一步</el-button
      >
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :show-close="false"
    >
      <div style="margin: -25px 0px">
        <div>多个路径请使用 换行 进行分隔</div>
        <!-- v-model 的值无法在运行时改变，只能出此下策-->
        <textarea
          v-if="dialogBind == 'c8x86repo'"
          v-model="c8x86repo"
          class="repoTextarea"
          :placeholder="textareaPlaceholder"
        ></textarea>
        <textarea
          v-if="dialogBind == 'c8aarch64repo'"
          v-model="c8aarch64repo"
          class="repoTextarea"
          :placeholder="textareaPlaceholder"
        ></textarea>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";
import { ElMessageBox } from "element-plus";

export default {
  setup() {
    const isx86Exist = false;
    const isaarch64Exist = false;
    return {
      isx86Exist,
      isaarch64Exist,
    };
  },
  computed: {
    isConnecting() {
      if (this.isc8x86Connecting || this.isc8aarch64Connecting) {
        return true;
      } else {
        return false;
      }
    },
    isConnectSuccess() {
      if (this.isc8x86ConnectSuccess && this.isc8aarch64ConnectSuccess) {
        return true;
      } else {
        return false;
      }
    },
  },
  data() {
    return {
      timer: null,
      // c8 x86
      isc8x86Connecting: false,
      isc8x86ConnectSuccess: false,
      isc8x86ConnectFailed: false,
      // c8 aarch64
      isc8aarch64Connecting: false,
      isc8aarch64ConnectSuccess: false,
      isc8aarch64ConnectFailed: false,
      //  repo checking
      machineList: [],
      dialogVisible: false,
      dialogTitle: "",
      dialogBind: "",
      c8x86repo: "",
      c8aarch64repo: "",
      textareaPlaceholder:
        "请输入软件仓库路径\n\n例如：\n在线仓库\nhttp://0.0.0.0/iso/AppStream\nhttp://0.0.0.0/iso/BaseOS\nhttp://0.0.0.0/iso/kernel-4.18\n\n请输入： http://0.0.0.0/iso",
    };
  },
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  created() {
    this.getData();
  },
  methods: {
    getData: function () {
      if (this.$route.params.machines === undefined) {
        console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
        this.$router.push("/");
        return;
      }
      this.machineList = JSON.parse(this.$route.params.machines);
      console.log("set repo page machineList ", this.machineList);
      //  check x86_64 exist
      this.machineList.forEach((machine) => {
        if (machine.agent_arch === "x86_64") {
          this.isx86Exist = true;
        }
      });
      this.machineList.find((machine) => {
        if (machine.agent_arch === "aarch64") {
          this.isaarch64Exist = true;
        }
      });
    },
    showDialog: function (system, arch, repoBindStr) {
      this.dialogTitle = system + " - " + arch + " - 软件仓库路径";
      this.dialogVisible = true;
      this.dialogBind = repoBindStr;
      console.log(this.dialogBind);
    },
    cancelMigrate: function () {
      this.$router.push("machine-management");
    },
    nextStep: function () {
      // this.$router.replace("/select-migrate-kernel");
      console.log("@DEBUG: 迁移下一步", this.machineList);
      this.$router.replace({
        name: "EnvCheckBeforeMigrate",
        params: this.$route.params,
      });
    },
    checkRepo: function () {
      clearInterval(this.timer);
      this.timer = null;
      let agentIpGroup = this.machineList.map((machine) => {
        return machine.agent_ip;
      });
      this.$http
        .post("/check_add_repo", {
          mod: "check_add_repo",
          agent_ip: agentIpGroup,
          migration_after_x86_64: this.c8x86repo,
          migration_after_aarch64: this.c8aarch64repo,
        })
        .then((res) => {
          this.isc8x86Connecting = true;
          this.isc8aarch64Connecting = true;
          this.isc8aarch64ConnectFailed =
            this.isc8aarch64ConnectSuccess = false;
          this.isc8x86ConnectFailed = this.isc8x86ConnectSuccess = false;
          let num = 0;
          this.timer = setInterval(() => {
            this.$http
              .post("/get_add_repo_data", {
                mod: "get_add_repo_data",
                agent_ip: agentIpGroup,
              })
              .catch((err) => {
                console.log(err);
              })
              .then((res) => {
                console.log(res);
                // after x86
                if (res.data.migration_after_x86_64 == "success") {
                  this.isc8x86Connecting = false;
                  this.isc8x86ConnectSuccess = true;
                } else if (res.data.migration_after_x86_64 == "failed") {
                  this.isc8x86Connecting = false;
                  this.isc8x86ConnectFailed = true;
                } else {
                  this.isc8x86Connecting = true;
                }
                //  after aarch64
                if (res.data.migration_after_aarch64 == "success") {
                  this.isc8aarch64Connecting = false;
                  this.isc8aarch64ConnectSuccess = true;
                } else if (res.data.migration_after_aarch64 == "failed") {
                  this.isc8aarch64Connecting = false;
                  this.isc8aarch64ConnectFailed = true;
                } else {
                  this.isc8aarch64Connecting = true;
                }
                // 如果都成功了，就清除定时器，跳转到下一步
                if (
                  this.isc8x86ConnectSuccess &&
                  this.isc8aarch64ConnectSuccess
                ) {
                  this.isc8x86Connecting = false;
                  this.isc8aarch64Connecting = false;
                  clearInterval(this.timer);
                  console.log("全部源连接成功");
                  setTimeout(() => {
                    this.nextStep();
                  }, 2000);
                  return;
                }
                // 所有结果不为空，但是不全为成功，只清除定时器，不跳转
                if (
                  (this.isc8aarch64ConnectSuccess ||
                    this.isc8aarch64ConnectFailed) &&
                  (this.isc8x86ConnectSuccess || this.isc8x86ConnectFailed)
                ) {
                  this.isc8x86Connecting = false;
                  this.isc8aarch64Connecting = false;
                  clearInterval(this.timer);
                  console.log("部分或全部源连接失败");
                  return;
                }
                num++;
                if (num > 30) {
                  this.isc8aarch64Connecting = false;
                  this.isc8x86Connecting = false;
                  clearInterval(this.timer);
                  return;
                }
              });
          }, 5000);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    window.onbeforeunload = function (e) {
      e = e || window.event;
      // 兼容IE8和Firefox 4之前的版本
      if (e) {
        e.returnValue = "关闭提示";
      }
      // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
      return "关闭提示";
    };
  },

  unmouted() {
    window.onbeforeunload = null;
    clearInterval(this.timer);
    this.timer = null;
  },
  beforeRouteLeave(to, from, next) {
    if (to.name === "EnvCheckBeforeMigrate") {
      next();
      return false;
    }
    ElMessageBox({
      title: "确定退出迁移吗？",
      confirmButtonText: "退出",
      cancelButtonText: "取消",
      showCancelButton: true,
      showClose: false,
    })
      .then((res) => {
        next();
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style scoped>
textarea.repoTextarea {
  width: 530px;
  height: 200px;
  border-color: #e2e2e2;
  background-color: #f2f2f2;
  border-style: solid;
  border-radius: 3px;
  padding: 15px;
  margin-top: 10px;
  resize: none;
}

textarea.repoTextarea:focus {
  outline: none;
}

.repoInputComponent {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 6px;
}

input.repoLineInput {
  height: 24px;
  width: 360px;
  font-size: 14px;
  margin-top: 2px;
  margin-left: 8px;
  border-style: none none solid none;
  border-color: #e2e2e2;
  transition: border-color 0.2s;
}

input.repoLineInput:focus {
  outline: none;
  border-style: none none solid none;
  border-color: #1b67b3;
  transition: border-color 0.2s;
}

.inputLargeBtn {
  margin-left: -24px;
  height: 24px !important;
  width: 24px !important;
}

.pageContainer {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.footerBar {
  height: 50px;
  margin: 0px -25px -8px -25px;
  padding-right: 25px;
  background-color: #eeeeee;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.darkblueHeaderText {
  color: #002672;
  font-size: 16px;
  margin: 0;
}

.smallPaddingUl {
  padding-left: 20px;
}

.smallPaddingUl > li {
  margin-top: 6px;
}

.cardBox {
  margin-top: 16px;
}

.dotStartSmallHeader {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-top: 14px;
}

.dotStartSmallHeader > .roundDot {
  background-color: #1b67b3;
  width: 6px;
  height: 6px;
  border-radius: 3px;
}

.dotStartSmallHeader > .headerText {
  margin: 6px 0 6px 10px;
}

.smallGrayFonts {
  font-size: 15px;
  color: #888888;
}

.smallLighterGrayFonts {
  margin-top: 3px;
  font-size: 14px;
  color: #999999;
}
.loading {
  animation: rotate 1s linear infinite;
}
.leftMargin {
  margin-left: 20px;
}
</style>
