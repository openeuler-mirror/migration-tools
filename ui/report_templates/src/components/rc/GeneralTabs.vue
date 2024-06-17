<template>
  <div>
    <h1>{{ $root.data.general_tabs.name }}</h1>
    <div id="headerInfo">
      <el-card
        shadow="hover"
        class="box-card"
        :body-style="{ padding: '0px 0px 15px 20px' }"
      >
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">当前系统版本</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.current_os_version }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">当前系统内核版本</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.current_os_kennel_version }}
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
            {{ $root.data.general_tabs.architecture }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">/var/cache 可用空间</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.var_cache_available_space }}
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
            {{ $root.data.general_tabs.replaced_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">兼容软件包数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.compatible_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">不兼容软件包数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.incompatible_software_package_count }}
          </el-col>
        </el-row>
        <el-row class="infoItemLineMargin">
          <el-col :span="6" class="infoItemTitle">迁移软件包总数量</el-col>
          <el-col :span="18" style="margin-top: 5px">
            {{ $root.data.general_tabs.software_package_count }}
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "GeneralTabs",
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
