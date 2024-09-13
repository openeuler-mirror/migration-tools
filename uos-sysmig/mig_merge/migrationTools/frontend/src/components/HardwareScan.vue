<template>
<el-main>
    <div>
        <h1>硬件兼容性评估</h1>
    </div>
    <div style="width:100%;" v-if="isDataLoaded">
        <el-table :data="displayResult" style="width: 100%">
            <el-table-column prop="vendorName" label="厂商名称" />
            <el-table-column prop="deviceName" label="设备名称" />
            <el-table-column prop="subsystemVendorName" label="子系统厂商名称" />
            <el-table-column prop="subsystemDeviceName" label="子系统设备名称" />
            <el-table-column prop="deviceClassName" label="设备类别名称" />
            <el-table-column label="兼容性" align="center" width=160>
                <template #default="scope">
                    <div class="compatabilityTag" 
                         :class="{'itemTagCompatable': scope.row.compatability=='Compatible', 
                         'itemTagNeedCheck': scope.row.compatability=='Need Check'}">
                         {{ scope.row.compatability }}
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <div style="height: 50px"></div>
</el-main>
</template>


<script>
export default {
    name: 'HardwareScan',
    data() {
        return {
            isDataLoaded: false,
            hardwareScanResultRaw: [],
            displayResult: Array()
        }
    },
    created() {
        this.loadJSON(window.utmt_report_data).then(res=>{
            this.hardwareScanResultRaw = res;
            
            console.log(this.hardwareScanResultRaw[0][0]);
            for(let i=0; i<this.hardwareScanResultRaw.length; i++) {
                let tmpArr = {}
                tmpArr.vendorID = this.hardwareScanResultRaw[i][0];
                tmpArr.deviceID = this.hardwareScanResultRaw[i][1];
                tmpArr.svID = this.hardwareScanResultRaw[i][2];
                tmpArr.ssID = this.hardwareScanResultRaw[i][3];
                tmpArr.deviceClassID = this.hardwareScanResultRaw[i][4];
                tmpArr.vendorName = this.hardwareScanResultRaw[i][5];
                tmpArr.deviceName = this.hardwareScanResultRaw[i][6];
                tmpArr.subsystemVendorName = this.hardwareScanResultRaw[i][7];
                tmpArr.subsystemDeviceName = this.hardwareScanResultRaw[i][8];
                tmpArr.deviceClassName = this.hardwareScanResultRaw[i][9];
                tmpArr.compatability = this.hardwareScanResultRaw[i][10];
                this.displayResult.push(tmpArr);
            }
            this.isDataLoaded = true;
        });
    },
    methods: {
        loadJSON: function(json) {
            return new Promise((resolve, reject)=>{
                try {
                    return resolve(JSON.parse(json));
                }
                catch (e) {
                    return reject(e);
                }
            });
        },
    }
}
</script>

<style scoped>
.el-main{
    min-height: calc(100vh - 120px)
}
.infoItemLineMargin {
    margin-top: 10px;
}
.infoItemTitle {
    color: #606266;
}
.compatabilityTag {
    padding: 0px 5px 0px 5px;
    border-radius: 4px;
    border-width: 1px;
    text-align: center;
    margin-right: 10px;
    margin-left: 10px;
    color: #606266;
    border-style: solid;
    font-family: "Helvetica";
}
.itemTagCompatable {
    border-color: #CCFF99;
    background: #CCFF99;
}
.itemTagNeedCheck {
    border-color: #FFCC66;
    background: #FFCC66;
}
</style>