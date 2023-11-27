<template>
  <div>
    <div class="head">
      <div class="head-1"></div>
      <span>主机管理</span>
    </div>

    <el-card>
      <img src="./img/u189.png" alt="" />&ensp;
      "主机管理"用于管理未完成迁移工作的任务
    </el-card>

    <el-row>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机ip ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">主机名 ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">现在状态：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">操作系统类型 ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">构架 ：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">迁移状态：全部</el-card>
      </el-col>
      <el-col :span="2.5" class="col">
        <el-card class="col-1">失败原因：全部</el-card>
      </el-col>
    </el-row>

    <el-card class="center">

      <el-row class="center-1">
        <el-col :span="20" class="num">{{ this.total }}项</el-col>
        <el-col :span="2">
          <el-button type="primary" plain @click="exportData()" icon="el-icon-upload"  size="small "
            >全部导出</el-button
          >

        </el-col>
        <el-col :span="2">
          <el-button type="primary" plain @click="gohostlist()"  icon=" el-icon-position"  size="small "
            >全部迁移</el-button
          >
        </el-col>
      </el-row>

    </el-card>
  </div>
</template>

<style src="./index.css" scoped>

</style>
