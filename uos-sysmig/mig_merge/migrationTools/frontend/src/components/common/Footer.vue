<template>
    <el-footer class="negativeMarginFooter">
        <img src="data:img/png; base64,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" class="logo" />
        <!--<div class="title">打造操作系统创新生态</div>-->
        <div class="copyright">Copyright © 2021 统信软件技术有限公司版权所有</div>
    </el-footer>
</template>

<script>
export default {
    name: 'Footer',
    data() {
        return {
            publicPath: process.env.BASE_URL
        }
    },
    props: {
    },
}
</script>

<style scoped>
.negativeMarginFooter {
    margin: 0px -58px -40px -60px;
    padding: 5px 30px 0 80px;
    height: 60px;
    background-color: #003296;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
}

.logo {
    vertical-align: center;
    margin-top: 14px;
    width: 106px;
    height: 22px;
    float: left;
}

.title {
    vertical-align: center;
    float: left;
    color: rgba(255, 255, 255, 0.719);
    margin: -2px 0px 2px 60px;
}

.copyright {
    vertical-align: center;
    float: right;
    color: rgba(255, 255, 255, 0.719);
    margin: -2px 60px 2px 0px;
    font-size: 14px;
}
</style>