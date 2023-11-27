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

      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
        align="center"
      >
        <el-table-column type="selection" width="55" align="center">
        </el-table-column>

        <el-table-column label="迁移时间" align="center">
          <template slot-scope="scope">
            {{ timeTranslate(scope.row.task_CreateTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column label="在线状态" align="center" :formatter="formatState">
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column
          prop="agent_os"
          label="操作系统类型"
          align="center"
          show-overflow-tooltip=""
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center" :formatter="formatState">
        </el-table-column>
        <el-table-column prop="task_status" label="迁移状态" align="center" :formatter="formatState">
          <template slot-scope="scope">
            <el-col v-if="scope.row.task_status == '00'">未迁移</el-col>
            <el-col
              v-if="
                fn(scope.row.task_status)
              "
              >迁移中</el-col
            >

            <el-col v-if="scope.row.task_status == '09'">迁移成功</el-col>
            <el-col v-if="scope.row.task_status.slice(-1) == '8'">迁移失败</el-col>
          </template>
        </el-table-column>
        <el-table-column
          prop="failure_reasons"
          label="历史失败原因"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
              @click="gohostlist1(scope.row)"
              :disabled="item(scope.row)"
               icon=" el-icon-position"  size="small "
              >迁移</el-button
            >
          </template>
        </el-table-column>
      </el-table>

    </el-card>
  </div>
</template>

<style src="./index.css" scoped>

</style>
