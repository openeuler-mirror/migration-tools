<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>迁移前系统环境检查</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      对列表中的主机执行迁移环境检查，迁移检测报告可在报告生成后，前往 下载中心
      下载
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>

        <el-col :span="13" class="center-1-2">
          <el-button  type="primary" plain @click="inspect()" icon="el-icon-eleme" size="small" > 开始检查</el-button></el-col
        >
      </el-row>
      <el-table
        ref="multipleTable"
        :data="tranferdata.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >


        <el-table-column prop="task_CreateTime" label="迁移时间" align="center">
        </el-table-column>
        <el-table-column prop="agent_id" label="AgentID" align="center">
        </el-table-column>
        <el-table-column prop="agent_ip" label="主机IP" align="center">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名" align="center">
        </el-table-column>
        <el-table-column

          label="在线状态"
          align="center"
        >
        <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column prop="agent_os" label="操作系统类型" align="center">
        </el-table-column>
        <el-table-column prop="agent_arch" label="架构" align="center">
        </el-table-column>
         <el-table-column label="检查进度" align="center" v-if="progress">
             <el-col>未执行</el-col>
        </el-table-column>


        <el-table-column
          label="检查进度"
          :formatter="formatState"
          align="center"
          v-if="isprogress"
        >
          <template slot-scope="scope">
            <el-col v-if="scope.row.task_status == 0">未执行</el-col>
            <el-col v-if="scope.row.task_status == 1">
              <el-row>执行中</el-row>
              <el-progress :percentage="scope.row.task_progress"></el-progress>
            </el-col>
            <el-col v-if="scope.row.task_status == 2"
              ><img src="./img/u856.svg" alt="" /> 执行成功</el-col
            >
            <el-col v-if="scope.row.task_status == 3"
              ><img src="./img/u1070.svg" alt="" /> 执行失败</el-col
            >
          </template>
        </el-table-column>

        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              plain
              @click="checkone(scope.row.agent_ip)"
              icon="el-icon-eleme" size="small"
              >检查</el-button
            >
            <el-button
              type="primary"
              plain
              icon="el-icon-document" size="small"
              @click="testreport(scope.row.agent_ip, scope.row.hostname)"
              >迁移检测报告</el-button
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
          <el-button @click="err()">取消</el-button>

          <el-button
            @click="gotransfer()"
            :disabled="notempty(this.tranferdata)"
            >下一步</el-button
          >
        </el-row>
      </div>
    </div>
  </div>
</template>

