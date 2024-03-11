<template>
  <div>
    <el-container class="el-container home-container is-vertical">
      <el-header>
        <div class="header-left">

        </div>
        <div></div>
      </el-header>

      <el-container>
        <!-- 左边 -->
        <el-aside :width="isCollapse ? '64px' : '200px'">
          <div class="toggle-button" @click="toggleCollapse">|||</div>

          <el-menu
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            :collapse-transition="false"
            background-color="#333744"
            text-color="#fff"
            active-text-color="#409EFF"
            unique-opened
          >
            <el-submenu index="1">
              <template slot="title">
                <router-link to="/software" tag="li">
                <img src="../assets/left/u9.svg" alt="" class="software-1 left">
                 <img src="../assets/left/u10.svg" alt="" class="software-3">
               <!-- <span  class="software-2 software-3">Ip</span> -->

                <span>导入软件</span>
                </router-link>
              </template>

            </el-submenu>

            <el-submenu index="2">
              <template slot="title">
                <router-link to="/hostment" tag="li">
               <img src="../assets/left/u9.svg" alt="" class="hostment-1 left" >
               <img src="../assets/left/u10.svg" alt="" class="hostment-2">
                <span>主机管理</span>
                </router-link>
              </template>

            </el-submenu>

            <el-submenu index="3">
              <template slot="title">

                <router-link to="/loadcenter" tag="li">
                 <img src="../assets/left/u6.svg" alt="" class="left">
                <span>下载中心</span>
                </router-link>
              </template>

            </el-submenu>

            <el-submenu index="4">
              <template slot="title">
                <router-link to="/record" tag="li">

                 <img src="../assets/left/u7.svg" alt="" class="left">
                <span>迁移记录</span>
                </router-link>
              </template>

            </el-submenu>

          </el-menu>
          <!-- </el-col>
          </el-row> -->
        </el-aside>

        <!-- 右边 -->
        <el-main>

          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isCollapse: false,
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },
  },
};
</script>

<style>
.left{
    margin-right:30px ;
}
.home-container {
  height: 100vh;
}
.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #373d41;
  padding: 0 20px;
  box-sizing: border-box;
  line-height: 60px;
}
.header-left {
  display: flex;
  align-items: center;
}
.header-left > img {
  margin-right: 15px;
  width: 61px;
  height: 56px;
  border-radius: 50%;
}
.header-left > span {
  font-size: 22px;
  color: #fff;
  display: inline-block;
}
.el-aside {
  background-color: #333744;
}
.el-submenu [class^="el-icon-"] {
  font-size: 14px;
}
.toggle-button {
  background-color: #4a5064;
  font-size: 10px;
  line-height: 24px;
  color: #fff;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
.software-1{
  position: relative;
}
/* .software-2{
  position: fixed;
  color:palevioletred;
  left: 26px;
  top:85px
} */
.software-3{
  position: absolute;
   left: 24px;
  top:23px;
  /* background: fuchsia; */
}
.hostment-1{
  position: relative;
}
.hostment-2{
  position: absolute;
  left: 24px;
  top:23px
}

</style>
