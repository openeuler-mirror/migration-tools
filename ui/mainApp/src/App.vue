<template>
  <div class="layout">
    <el-container class="container">
      <el-aside
        :class="{
          'aside-collapsed': isCollapse == true,
          'aside-expand': isCollapse == false,
        }"
      >
        <div class="head">
          <fold
            class="menu-icon"
            v-show="!isAsideExpand"
            @click="toggleMenu()"
          />
          <expand
            class="menu-icon"
            v-show="isAsideExpand"
            @click="toggleMenu()"
          />
          <span v-if="!isCollapse">统信服务器系统迁移软件</span>
        </div>
        <div class="line" />
        <el-menu
          background-color="#424242"
          text-color="#ffffff"
          active-text-color="#ffffff"
          :default-active="currentRouter"
          :router="true"
          :collapse="isCollapse"
          :collapse-transition="false"
        >
          <el-menu-item index="/import-machine">
            <el-icon><document /></el-icon>
            <span>导入主机</span>
          </el-menu-item>
          <el-menu-item index="/machine-management">
            <el-icon><document /></el-icon>
            <span>主机管理</span>
          </el-menu-item>
          <el-menu-item index="/download-center">
            <el-icon><document /></el-icon>
            <span>下载中心</span>
          </el-menu-item>
          <el-menu-item index="/migration-history">
            <el-icon><document /></el-icon>
            <span>迁移记录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container class="content">
        <Header />
        <div class="main">
          <router-view />
        </div>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "./components/Header.vue";

import { Fold, Expand, Document } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

export default {
  name: "App",
  components: {
    Header,
    Fold,
    Expand,
    Document,
  },
  created() {
    const router = useRouter();
    router.afterEach((to) => {
      this.currentRouter = to.fullPath;
    });
    /*
    // 需要在跳转时弹出弹窗问一下是否确认跳转的，都加在这里
    const specialPages = new Set(["MigrateMachine", "MigrationNotice", 
                                "CheckAvalibleSpace", "SetRepo", 
                                "SelectMigrateKernel"]);
    router.beforeEach((to, from) => {
      if(specialPages.has(from.name)) {
        let answer = window.confirm('确定离开当前页面吗？离开将取消迁移');
        if (!answer) {
          this.currentRouter = from.fullPath;
          return false;
        }
      }
    })
    */
  },
  data() {
    return {
      isAsideExpand: true,
      buttonIcon: this.isAsideExpand ? Fold : Expand,
      currentRouter: "/",
    };
  },

  computed: {
    isCollapse() {
      if (this.isAsideExpand) {
        return false;
      } else {
        return true;
      }
    },
  },

  methods: {
    toggleMenu: function () {
      this.isAsideExpand = !this.isAsideExpand;
      this.buttonIcon = this.isAsideExpand ? Fold : Expand;
    },
  },
};
</script>

<style scoped>
.layout {
  min-height: 100vh; /* 1vh 等于页面高度的 1% */
  background-color: #ffffff;
}

.container {
  height: 100vh;
}

.aside-expand {
  width: 230px !important;
  background-color: #424242;
}

.aside-collapsed {
  width: fit-content;
  background-color: #424242;
}

.head {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
}

.head > div {
  display: flex;
  align-items: center;
}

.head el-icon {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.menu-icon {
  width: 24px;
  height: 24px;
  color: #ffffff;
  cursor: pointer;
}

.menu-text {
  margin-left: 8px;
}

.head span {
  font-size: 16px;
  margin-left: 8px;
  margin-bottom: 2px;
  color: #ffffff;
}

.line {
  border-top: 1px solid hsla(0, 0%, 100%, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.content {
  display: flex;
  flex-direction: column;
  max-height: 100vh;
  overflow: hidden;
}

.main {
  height: calc(100vh - 66px);
  overflow: auto;
  padding: 8px 25px 8px 25px;
  background-color: #f9f9f9;
}
</style>

<style>
body {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.el-menu {
  border-right: none !important;
}

.el-sub-menu {
  border-top: 1px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.el-sub-menu:first-child {
  border-top: none;
}

.el-sub-menu [class^="el-icon-"] {
  vertical-align: -1px !important;
}

a {
  color: #409eff;
  text-decoration: none;
}

.el-pagination {
  text-align: center;
  margin-top: 20px;
}

.el-popper__arrow {
  display: none;
}

.el-menu-item:is(.is-active),
.el-menu-item:is(.is-active):hover {
  background-color: #b9cfff;
}

.infoCard {
  display: flex;
  justify-content: start;
  align-items: center;
  background-color: #ffffff;
  border-radius: 3px;
  border-color: #dddddd;
  border-style: solid;
  border-width: 1px;
  margin-top: 12px;
  padding: 10px 12px 10px 18px;
}

.infoIcon {
  width: 16px;
  height: 16px;
  border-radius: 8px;
  background-color: #5798d9;
  color: #ffffff;
  text-align: center;
  font-size: small;
  margin-right: 12px;
  margin-top: 4px; /* 汉字文本在视觉上略偏下，将图标向下调整，可使效果看起来在同一高度上 */
}

.dropMenuContainer {
  margin-top: 16px;
  display: flex;
  justify-content: start;
  align-items: center;
}

.child {
  margin-right: 5px;
}
</style>
