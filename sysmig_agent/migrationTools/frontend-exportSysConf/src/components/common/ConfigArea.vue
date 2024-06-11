<template>
    
    <h3>{{ ConfigGroupName }}</h3>
    
    <div v-for="configItem in ConfigItems" :key="configItem" class="confBlockItem">
        <div @click="toggleDisplay(configItem)" class="flexBox">
            <div class="leftIconBox">
                <img src="../../assets/forward.svg" :class="{arrowIcon: !configItem.show, arrowIconRotate: configItem.show}">
            </div>
            <div class="left">
                <b>{{configItem.confName}}</b>
                <div>{{configItem.desc}}</div>
            </div>
            <div class="spacing"></div>
            <div class="right">
                <el-button-group>
                    <el-tooltip
                        :show-after=500
                        class="item"
                        effect="light"
                        content="将差异文件通过浏览器下载到当前系统中"
                        placement="top-end"
                    >
                        <el-button type="primary" @click.stop="download($event, configItem.diff)" size="small">下载到本地</el-button>
                    </el-tooltip>
                    <el-tooltip
                        :show-after=500
                        class="item"
                        effect="light"
                        content="将差异文件导出到运行 UTMTC 的系统中"
                        placement="top-start" 
                    >
                        <el-button type="primary" @click.stop="exportDiff($event, configItem.diff)" size="small">保存到远程</el-button>
                    </el-tooltip>
                </el-button-group>
            </div>
        </div>

        <div v-if="configItem.show" class="confBlockDiffBackground">
            <div v-html="configItem.diffHtml"></div>
        </div>
    </div>
</template>

<script>
import "./github.min.css"
import "./diff2html.css"
import { ElMessage } from 'element-plus'

import axios from 'axios'

export default {
    name: 'ConfigArea',
    props: {
        ConfigGroupName: String,
        ConfigItems: Array
    },
    data() {
        return {
            diffHtml: String
        }
    },
    setup() {
    },
    created() {

    },
    methods: {
        toggleDisplay: function(configItem) {
            configItem.show = !configItem.show;
        },
        download: function(event, filename) {
            console.info(event);
            let link = document.createElement('a');
            filename = filename.substring(filename.lastIndexOf('/')+1);
            link.href = window.backendApiEP + 'downloadConfDiff/' + filename;
            link.click();
        },
        exportDiff: function(event, filename) {
            console.info(event);
            console.log(filename);
            filename = filename.substring(filename.lastIndexOf('/')+1);
            console.log(filename);
            axios.get(window.backendApiEP + 'exportConfDiff/' + filename).then(res=>{
                console.log(res.data);
                if(res.data.success) {
                    ElMessage({
                        message: '导出成功，已导出至 ' + res.data.targetPath,
                        type: 'success',
                        duration: 10000,
                        showClose: true
                    })
                } else {
                    ElMessage({
                        message: "导出失败，原因：" + res.data.exception,
                        type: 'error',
                        duration: 6000,
                    })
                }
            }).catch(err=>{
                console.log(err);
                ElMessage({
                    message: '请求失败，请检查网络连接情况',
                    type: 'error',
                    duration: 6000,
                })
            });
        }
    }
}
</script>

<style scoped>
.arrowIcon {
    width:20px;
    height: 20px;
}
.arrowIconRotate {
    width:20px;
    height: 20px;
    transform: rotate(90deg);
}
.confBlockItem {
    margin: 0px 0px 15px 0px;
    border-radius: 4px;
    border-style: solid;
    border-width: 1px;
    border-color: #dddddd;
    background: #fefefe;
    transition: background 0.2s;
}
.confBlockItem:hover {
    margin: 0px 0px 15px 0px;
    background: #f8f8f8;
}
.confBlockTitle {
    padding: 15px 15px 15px 15px;
}
.confBlockDiffBackground {
    margin: 0px 15px 0px 15px;
    border-radius: 4px;
    background: #ffffff;
}
.flexBox {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px 15px 10px 15px;
}
.left {
    vertical-align: center;
    float: left;
}
.leftIconBox {
    vertical-align: center;
    flex-basis: 20px;
    margin: 0 10px 0 0;
    height: 20px;
}
.right {
    vertical-align: center;
    float: right;
}
.spacing {
    vertical-align: center;
    flex-grow: 1;
}
</style>

