<template>
  <div class="pageContainer">
    <div>
      <StyledSubheaderBlock subHeader="迁移重要提示" />
      <SubheaderInfoCard :info="title" />

      <el-card class="cardBox">
        <h2 class="darkblueHeaderText">重要提示</h2>
        <ol class="smallPaddingUl">
          <li v-for="info in infoList" :key="info">
            <span v-html="info"></span>
          </li>
        </ol>
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
        @click="nextStep()"
        style="width: 130px; color: white"
        color="#1b67b3"
        >下一步</el-button
      >
    </div>
  </div>
</template>

<script>
import StyledSubheaderBlock from "@/components/StyledSubheaderBlock.vue";
import SubheaderInfoCard from "@/components/SubheaderInfoCard.vue";

import { ElMessageBox } from "element-plus";

export default {
  name: "MigrationNotice",
  components: {
    StyledSubheaderBlock,
    SubheaderInfoCard,
  },
  data() {
    return {
      title: "",
      infoList: [],
    };
  },
  created() {
    if (this.$route.params.machines === undefined) {
      console.log("从路由或者url来的，应该拒绝该跳转请求并跳回到主页");
      this.$router.push("/");
      return;
    }
    this.migrationType = JSON.parse(this.$route.params.migrationType);
    if (this.migrationType == "stock_replacement") {
      this.title = "即将开始迁移工作，请仔细阅读以下提示";
      this.infoList = [
        "迁移一旦开始，过程不可逆。请确保您已将系统的数据与设置进行<b>【完整备份】</b>。",
        "迁移前请获得管理员许可，再进行迁移工作。",
        "请提前获取【统信服务器操作系统 V20 】的软件仓库地址。",
        "迁移过程中请保证稳定的网络连接。",
        "迁移过程中请不要在迁移主机上进行任何操作。",
        "请确保在 <b>/var/cache</b> 中至少有 10GB 的可用空间。",
      ];
    }
    if (this.migrationType == "new_expansion") {
      this.title = "即将开始迁移分析工作，请仔细阅读以下提示";
      this.infoList = [
        "本功能支持新增扩容场景下， CentOS 迁移到【统信服务器操作系统 V20】的迁移分析。",
        "分析内容包括系统硬件、系统配置、RPM包差异分析等。",
        "迁移分析前请获得管理员许可，再进行迁移工作。",
        "请提前获取【统信服务器操作系统 V20 】的软件仓库地址。",
        "迁移分析过程中请保证稳定的网络连接。",
      ];
    }
  },
  methods: {
    cancelMigrate: function () {
      this.$router.push("machine-management");
    },
    nextStep: function () {
      let routeName = "";
      if (this.migrationType == "stock_replacement") {
        routeName = "CheckAvalibleSpace";
      }
      if (this.migrationType == "new_expansion") {
        routeName = "SetAnalyzeRepo";
      }
      this.$router.replace({
        name: routeName,
        params: {
          machines: this.$route.params.machines,
          migrationType: this.$route.params.migrationType,
        },
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
  },
  beforeRouteLeave(to, from, next) {
    if (to.name === "CheckAvalibleSpace" || to.name === "SetAnalyzeRepo") {
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

.cardBoxTitleContainer {
  display: flex;
  justify-content: space-between;
}

.horizontalBtnSet {
  display: flex;
  justify-content: space-between;
  width: fit-content;
}
</style>
