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
        <div v-if="isc7x86Exist || isc8x86Exist">
          <div class="dotStartSmallHeader">
            <div class="roundDot"></div>
            <h4 class="headerText">x86_64</h4>
          </div>
          <div class="repoInputComponent" v-if="isc7x86Exist">
            <span class="smallGrayFonts">CentOS 7 系列平台：</span>
            <input
              v-model="c7x86repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="showDialog('CentOS 7', 'x86_64', 'c7x86repo')"
              size="small"
              class="inputLargeBtn"
            >
              <img src="~@/assets/arrows-angle-expand.svg" />
            </el-button>
            <div class="leftMargin">
              <el-row v-show="isc7x86Connecting">
                <div>
                  <img src="@/assets/loading.png" class="loading" />
                  <span class="leftMargin">正在连接软件仓库......</span>
                </div>
              </el-row>
              <el-row v-show="isc7x86ConnectSuccess">
                <div>
                  <img src="@/assets/load_success.svg" />
                  <span class="leftMargin">软件仓库路径正确</span>
                </div>
              </el-row>
              <el-row v-show="isc7x86ConnectFailed">
                <div>
                  <img src="@/assets/load_failed.svg" />
                  <span class="leftMargin"
                    >连接失败，请检查您的软件仓库设置</span
                  >
                </div>
              </el-row>
            </div>
          </div>
          <div class="repoInputComponent" v-if="isc8x86Exist">
            <span class="smallGrayFonts">CentOS 8 系列平台：</span>
            <input
              v-model="c8x86repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="showDialog('CentOS 8', 'x86_64', 'c8x86repo')"
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
        <div v-if="isc7aarch64Exist || isc8aarch64Exist">
          <div class="dotStartSmallHeader">
            <div class="roundDot"></div>
            <h4 class="headerText">aarch_64</h4>
          </div>
          <div class="repoInputComponent" v-if="isc7aarch64Exist">
            <span class="smallGrayFonts">CentOS 7 系列平台：</span>
            <input
              v-model="c7aarch64repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="showDialog('CentOS 7', 'aarch_64', 'c7aarch64repo')"
              size="small"
              class="inputLargeBtn"
            >
              <img src="~@/assets/arrows-angle-expand.svg" />
            </el-button>
            <div class="leftMargin">
              <el-row v-show="isc7aarch64Connecting">
                <div>
                  <img src="@/assets/loading.png" class="loading" />
                  <span class="leftMargin">正在连接软件仓库......</span>
                </div>
              </el-row>
              <el-row v-show="isc7aarch64ConnectSuccess">
                <div>
                  <img src="@/assets/load_success.svg" />
                  <span class="leftMargin">软件仓库路径正确</span>
                </div>
              </el-row>
              <el-row v-show="isc7aarch64ConnectFailed">
                <div>
                  <img src="@/assets/load_failed.svg" />
                  <span class="leftMargin"
                    >连接失败，请检查您的软件仓库设置</span
                  >
                </div>
              </el-row>
            </div>
          </div>
          <div class="repoInputComponent" v-if="isc8aarch64Exist">
            <span class="smallGrayFonts">CentOS 8 系列平台：</span>
            <input
              v-model="c8aarch64repo"
              class="repoLineInput"
              placeholder="请输入软件仓库路径"
            />
            <el-button
              @click="showDialog('CentOS 8', 'aarch_64', 'c8aarch64repo')"
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
          !(!isc7x86Exist ^ !c7x86repo) &&
          !(!isc7aarch64Exist ^ !c7aarch64repo) &&
          !(!isc8x86Exist ^ !c8x86repo) &&
          !(!isc8aarch64Exist ^ !c8aarch64repo) &&
          !isConnecting
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
          v-if="dialogBind == 'c7x86repo'"
          v-model="c7x86repo"
          class="repoTextarea"
          :placeholder="textareaPlaceholder"
        ></textarea>
        <textarea
          v-if="dialogBind == 'c8x86repo'"
          v-model="c8x86repo"
          class="repoTextarea"
          :placeholder="textareaPlaceholder"
        ></textarea>
        <textarea
          v-if="dialogBind == 'c7aarch64repo'"
          v-model="c7aarch64repo"
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
  name: "MigrationNotice",
  setup() {
    const isc7x86Exist = false;
    const isc8x86Exist = false;
    const isc7aarch64Exist = false;
    const isc8aarch64Exist = false;
    return {
      isc7x86Exist,
      isc8x86Exist,
      isc7aarch64Exist,
      isc8aarch64Exist,
    };
  },
  data() {
    return {
      // c7 x86
      isc7x86Connecting: false,
      isc7x86ConnectSuccess: false,
      isc7x86ConnectFailed: false,
      // c7 aarch64
      isc7aarch64Connecting: false,
      isc7aarch64ConnectSuccess: false,
      isc7aarch64ConnectFailed: false,
      // c8 x86
      isc8x86Connecting: false,
      isc8x86ConnectSuccess: false,
      isc8x86ConnectFailed: false,
      // c8 aarch64
      isc8aarch64Connecting: false,
      isc8aarch64ConnectSuccess: false,
      isc8aarch64ConnectFailed: false,
      //  repo checking
      isConnecting: false,
      machineList: [],
      dialogVisible: false,
      dialogTitle: "",
      dialogBind: "",
      c7x86repo: "",
      c8x86repo: "",
      c7aarch64repo: "",
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
      console.log(this.machineList);
      for (let i = 0; i < this.machineList.length; i++) {
        if (
          this.machineList[i].agent_arch == "x86_64" &&
          (this.machineList[i].agent_os == "Centos 7" ||
           this.machineList[i].agent_os == "anolis7" ||
           this.machineList[i].agent_os == "redhat7"
          )
        )
          this.isc7x86Exist = true;
        if (
          this.machineList[i].agent_arch == "aarch64" &&
          (this.machineList[i].agent_os == "Centos 7" ||
           this.machineList[i].agent_os == "anolis7" ||
           this.machineList[i].agent_os == "redhat7"
          )
        )
          this.isc7aarch64Exist = true;
        if (
          this.machineList[i].agent_arch == "x86_64" &&
          (this.machineList[i].agent_os == "Centos 8" ||
           this.machineList[i].agent_os == "anolis8" ||
           this.machineList[i].agent_os == "redhat8"
          )
        )
          this.isc8x86Exist = true;
        if (
          this.machineList[i].agent_arch == "aarch64" &&
          (this.machineList[i].agent_os == "Centos 8" ||
           this.machineList[i].agent_os == "anolis8" ||
           this.machineList[i].agent_os == "redhat8"
          )
        )
          this.isc8aarch64Exist = true;
      }
    },
    showDialog: function (system, arch, repoBindStr) {
      this.dialogTitle = system + " 系列平台-" + arch + "-软件仓库路径";
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
        name: "SelectMigrateKernel",
        params: { machines: JSON.stringify(this.machineList) },
      });
    },
    checkRepo: function () {
      this.$http
        .post("/check_repo", {
          mod: "check_repo",
          centos7_x86_64: this.c7x86repo,
          centos7_aarch64: this.c8x86repo,
          centos8_x86_64: this.c7aarch64repo,
          centos8_aarch64: this.c8aarch64repo,
        })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
      this.isConnecting = true;
      this.isc7x86Connecting = true;
      this.isc8x86Connecting = true;
      this.isc7aarch64Connecting = true;
      this.isc8aarch64Connecting = true;
      this.isc7x86ConnectFailed = this.isc7x86ConnectSuccess = false;
      this.isc7aarch64ConnectFailed = this.isc7aarch64ConnectSuccess = false;
      this.isc8aarch64ConnectFailed = this.isc8aarch64ConnectSuccess = false;
      this.isc8x86ConnectFailed = this.isc8x86ConnectSuccess = false;
      let num = 0;
      this.timer = setInterval(() => {
        this.$http
          .post("/get_repo_data", {
            mod: "get_repo_data",
          })
          .catch((err) => {
            console.log(err);
          })
          .then((res) => {
            console.log(res);
            //  c7 x86
            if (res.data.centos7_x86 == "success") {
              this.isc7x86Connecting = false;
              this.isc7x86ConnectSuccess = true;
            } else {
              this.isc7x86Connecting = false;
              this.isc7x86ConnectFailed = true;
            }
            // c8 x86
            if (res.data.centos8_x86 == "success") {
              this.isc8x86Connecting = false;
              this.isc8x86ConnectSuccess = true;
            } else {
              this.isc8x86Connecting = false;
              this.isc8x86ConnectFailed = true;
            }
            //  c7 aarch64
            if (res.data.centos7_aarch64 == "success") {
              this.isc7aarch64Connecting = false;
              this.isc7aarch64ConnectSuccess = true;
            } else {
              this.isc7aarch64Connecting = false;
              this.isc7aarch64ConnectFailed = true;
            }
            //  c8 aarch64
            if (res.data.centos8_aarch64 == "success") {
              this.isc8aarch64Connecting = false;
              this.isc8aarch64ConnectSuccess = true;
            } else {
              this.isc8aarch64Connecting = false;
              this.isc8aarch64ConnectFailed = true;
            }
            // if (this.isc7x86ConnectSuccess && this.isc8x86ConnectSuccess
            //     && this.isc7aarch64ConnectSuccess && this.isc8aarch64ConnectSuccess) {
            if (
              !(this.isc7x86Exist ^ this.isc7x86ConnectSuccess) &&
              !(this.isc7aarch64Exist ^ this.isc7aarch64ConnectSuccess) &&
              !(this.isc8x86Exist ^ this.isc8x86ConnectSuccess) &&
              !(this.isc8aarch64Exist ^ this.isc8aarch64ConnectSuccess)
            ) {
              clearInterval(this.timer);
              console.log("连接成功");
              setTimeout(() => {
                this.nextStep();
              }, 1000);
            }
            num++;
            if (num > 10) {
              clearInterval(this.timer);
            }
          });
      }, 1000);
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
  },
  beforeRouteLeave(to, from, next) {
    // 导航离开该组件的对应路由时调用
    // 可以访问组件实例 `this`
    // 该导航可以通过 next(false) 来取消。
    if (to.name === "SelectMigrateKernel") {
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
        next(false);
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
