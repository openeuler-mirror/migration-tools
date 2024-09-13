<template>
    <el-container direction="vertical">
        <Header />
        <ConfigScan />
        <Footer />
    </el-container>
</template>

<script>
import Header from './common/Header.vue'
import Footer from './common/Footer.vue'
import ConfigScan from './ConfigScan.vue'

export default {
    name: 'ConfigScanApp',
    components: {
        Header,
        Footer,
        ConfigScan
    },
    beforeCreate() {
        console.log("beforeCreate @ ConfigScanApp.vue")
    }
}
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #303133;
        margin-top: 0px;
        margin-left: 20px;
        margin-right: 20px;
        padding: 30px;
    }

    .el-header,
    .el-footer {
        background-color: #409EFF;
        color: var(--el-text-color-primary);
        line-height: 60px;
        padding: 0px;
    }

    body > .el-container {
        margin: 40px;
        padding: 0px;
    }
</style>
