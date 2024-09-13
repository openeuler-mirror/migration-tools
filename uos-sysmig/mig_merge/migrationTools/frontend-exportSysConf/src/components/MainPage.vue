<template>
    <el-main>
        <div v-if="pageState==0">
            <h1>数据加载中</h1>
        </div>
        <div class="mainFlexContainer" v-if="pageState==1">
            <div class="titleFlexBox">
                <div class="left">
                    <h1>系统修改配置导出</h1>
                </div>
                <div class="spacing"></div>
                <div class="right">
                    <el-button-group>
                        <el-tooltip
                            :show-after=500
                            class="item"
                            effect="light"
                            content="将所有差异文件打包，通过浏览器下载到当前系统中"
                            placement="top-end"
                        >
                            <el-button type="primary" @click="downloadAll()" size="small">打包下载到本地</el-button>
                        </el-tooltip>
                        <el-tooltip
                            :show-after=500
                            class="item"
                            effect="light"
                            content="将所有差异文件打包，导出到运行 UTMTC 的系统中"
                            placement="top-start" 
                        >
                            <el-button type="primary" @click="exportAll()" size="small">打包保存到远程</el-button>
                        </el-tooltip>
                    </el-button-group>
                </div>
            </div>
            
            <div class="infoBlock">
                <p>系统名称： {{systemInfo.system}}</p>
                <p>系统架构： {{systemInfo.arch}}</p>
            </div>
            <ConfigArea v-for="config in configList" :key="config" :ConfigGroupName="config.confGroupName" :ConfigItems="config.confList" />
        </div>
        <div v-if="pageState==-1">
            <h1>数据加载失败，请检查网络连接</h1>
        </div>
    </el-main>
</template>

<script>
import * as diff from "diff2html"
import ConfigArea from './common/ConfigArea.vue'
import { ElMessage } from 'element-plus'

import axios from 'axios'

export default {
    name: 'MainPage',
    components: {
        ConfigArea
    }, 
    setup() {
        
    },
    data() {
        return {
            pageState: 0,       // 0:loading, 1:loaded, -1: loadfailed
            systemInfo: {},
            configList: []
        }
    },
    created() {
        axios.get(window.backendApiEP + 'getSysInfo').then(res=>{
            this.systemInfo = res.data;
            this.pageState = 1;
        }).catch(err=>{
            console.log(err);
            this.pageState = -1;
        });
        axios.get(window.backendApiEP + 'getDiffGroups').then(res=>{
            this.configList = res.data;
            for(let i=0; i<this.configList.length; i++) {
                for(let j=0; j<this.configList[i].confList.length; j++) {
                    this.configList[i].confList[j].show = false;
                    this.configList[i].confList[j].diffHtml = diff.html(diff.parse(this.configList[i].confList[j].diffContent), 
                        {
                            drawFileList: false,
                            matching: 'lines',
                            outputFormat: 'side-by-side',
                            diffStyle: 'char'
                        }
                    );
                }
            }
            console.log(this.configList);
            this.pageState = 1;
        }).catch(err=>{
            console.log(err);
            this.pageState = -1;
        })
    },
    methods: {
        downloadAll: function() {
            let link = document.createElement('a');
            link.href = window.backendApiEP + 'downloadAllConfDiff';
            link.click();
        },
        exportAll: function() {
            axios.get(window.backendApiEP + 'exportAllConfDiff').then(res=>{
                if(res.data.success) {
                    ElMessage({
                        message: '导出成功，已导出至  ' + res.data.targetPath,
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
.el-main {
    margin: 10px 60px 10px 60px;
}
.mainFlexContainer {
    display: flex;
    flex-direction: column;
}
.infoBlock {
    margin: 0 0 50px 50px;
}
.titleFlexBox {
    display: flex;
    flex-direction: row;
    align-items: center;
    align-content: center;
    padding: 10px 0px 10px 0px;
}
.flexBox {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px 15px 10px 15px;
}
.left {
    float: left;
}
.right {
    float: right;
}
.spacing {
    flex-grow: 1;
}

</style>

