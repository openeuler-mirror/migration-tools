<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      对列表中的主机执行迁移，生成的日志和报告前往 下载中心 下载
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>
      </el-row>
      <el-table
        ref="multipleTable"
        :data="
          transData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center">
        </el-table-column>

        <el-table-column prop="task_CreateTime" label="迁移时间" align="center">
        </el-table-column>
        <el-table-column prop="agent_id" label="AgentID" align="center">
        </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center">
        </el-table-column>
        <el-table-column label="在线状态" align="center">
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center">
        </el-table-column>

        <el-table-column label="迁移进度" align="center">
          <template slot-scope="scope" align="center">
            <el-col v-if="scope.row.task_status == 0">
              <el-row>迁移中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 1">
              <el-row>迁移中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 2">
              <img src="./img/u856.svg" alt="" />迁移成功</el-col
            >
            <el-col v-if="scope.row.task_status == 3">
              <img src="./img/u1070.svg" alt="" /> 迁移失败</el-col
            >
          </template>
        </el-table-column>

        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
              @click="journal(scope.row.agent_ip, scope.row.hostname)"
              icon="el-icon-tickets"
              size="small"
              >迁移日志</el-button
            >
            <el-button
              type="primary"
              plain
              icon="el-icon-document"
              size="small"
              @click="report(scope.row.agent_ip, scope.row.hostname)"
              >迁移分析报告</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[2, 4, 6, 8]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>

    <div class="footer">
      <div>
        <el-row>
          <el-button @click="gohostment()" :disabled="notempty(this.transData)"
            >返回</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>


