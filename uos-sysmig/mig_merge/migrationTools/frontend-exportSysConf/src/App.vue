<template>
<el-container direction="vertical">
  <Header />
  <MainPage />
</el-container>
</template>

<script>
import Header from './components/common/Header.vue'
import MainPage from './components/MainPage.vue'

export default {
  name: 'App',
  components: {
    Header, 
    MainPage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding: 0px;
  margin: 0px;
}

.el-header,
.el-footer {
    background-color: #409EFF;
    color: var(--el-text-color-primary);
    line-height: 60px;
    padding: 0px;
    margin: 0px;
}

body > .el-container {
    margin: 40px;
    padding: 0px;
}

</style>
