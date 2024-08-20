<template>
  <div>
    <h1>{{ $root.data.general_tabs.system_info.name }}</h1>
    <div id="headerInfo">
      <el-card
        shadow="hover"
        class="box-card"
        :body-style="{ padding: '0px 0px 15px 20px' }"
      >
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">当前系统版本</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.current_os_version }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">当前系统内核版本</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.current_os_kennel_version }}
          </el-col>
        </el-row>
      </el-card>
      <el-card
        shadow="hover"
        class="box-card"
        :body-style="{ padding: '0px 0px 15px 20px' }"
      >
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">系统架构</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.architecture }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">/var/cache 可用空间</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.var_cache_available_space }}
          </el-col>
        </el-row>
      </el-card>
      <el-card
        shadow="hover"
        class="box-card"
        :body-style="{ padding: '0px 0px 15px 20px' }"
      >
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">被替换的软件包数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.replaced_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">兼容软件包数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.compatible_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">不兼容软件包数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.incompatible_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">迁移软件包总数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.system_info.software_package_count }}
          </el-col>
        </el-row>
      </el-card>
    </div>
    <div>
          <h1 :style="tishiAccount_style"> 异常安装包：{{ $root.data.general_tabs.abnormal_pkg.num}} 个</h1>
          <div style="width: 100%">
            <el-table :data="fworkTable.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
          )" 
               style="margin-top: -25px">
              <el-table-column prop="soft_package" />
              <el-table-column prop="ware_package"  />
              </el-table>
          </div>
           <div style="margin-top: 30px">
      <el-pagination
        v-model:current-page="currentPage"
        :page-sizes="[10, 15, 30, 50, 100]"
        :page-size="pageSize"
        :pager-count="16"
        @current-change="currentPageChange"
        @size-change="handleSizeChange"
        layout="total, sizes, prev, pager, next"
        :total="fworkTable.length"
      >
      </el-pagination>
    </div>
  </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  name: "GeneralTabs",
   setup() {
    console.log("setup");
    const handleChange = (val) => {
      console.log(val);
    };
    const currentPageChange = (val) => {
      console.log(val);
      window.scrollTo(0, 460); // TODO: 换成动态计算的
    };

    return {
      rpmKeyword: ref(""),
      handleChange,
      currentPageChange,
    };
  },
  data(){
    return {
      fworkTable:[],
      currentPage:1,
       pageSize: 10,
        tishiAccount_style: {
        color: "",
      },

    }
  },
  created() {
   console.log("获取的值",this.$root.data.general_tabs.abnormal_pkg.num)
    this.fworkTable = this.$root.data.general_tabs.abnormal_pkg.data;
    if(this.$root.data.general_tabs.abnormal_pkg.num>0){
        this.tishiAccount_style.color = "red !important";

    }else{
      this.tishiAccount_style.color = "#303133 !important";
    }
   
    
  },
  methods:{
        handleSizeChange: function (size) {
      this.pageSize = size;
     
    },
  }
};
</script>

<style scoped>
.box-card {
  min-width: 600px;
  width: 40vw;
}
.infoItemLineMargin {
  margin-top: 10px;
}

.infoItemTitle {
  color: #606266;
}
</style>
