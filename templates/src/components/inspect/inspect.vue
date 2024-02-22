<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>检查可用空间</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      进行迁移需保证 ‘/var/cache’ 中至少有10GB的可用空间
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>
      </el-row>
      <el-table
        ref="multipleTable"
        :data="
          tableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center">
        </el-table-column>

        <el-table-column
          prop="task_CreateTime"
          label="迁移时间"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column
          prop="agent_id"
          label="AgentID"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column
          prop="agent_ip"
          label="主机IP"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column
          prop="hostname"
          label="主机名"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column label="在线状态" align="center" :formatter="empty">
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column
          prop="agent_os"
          label="操作系统类型"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column
          prop="agent_arch"
          label="架构"
          align="center"
          :formatter="empty"
        >
        </el-table-column>
        <el-table-column
          label="可用空间"
          align="center"
          :formatter="formatState"
          prop="agent_storage"
        >
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

      <!-- 提示弹窗 -->

      <el-dialog
        title="提示"
        :visible.sync="dialogFormVisible"
        width="22%"
        top="40vh"
      >
        <div>
          <div class="tan tan-1">
            <span>{{ this.success }}</span>
            台主机可用空间充足，点击“确定”继续迁移
          </div>
          <div class="tan">
            <span>{{ this.faild }}</span>
            台主机可用空间不足或无法检测可用空间，迁移失败。请检查 /var/cache
            目录，确认后再重新执行迁移
          </div>
        </div>
        <div slot="footer" class="dialog-footer">
          <el-button @click="info()">取 消</el-button>
          <el-button type="primary" @click="go()" :disabled="this.success == 0"
            >确 定</el-button
          >
        </div>
      </el-dialog>
    </el-card>

    <div class="footer">
      <div>
        <el-row>
          <el-button @click="err()">取消</el-button>

          <el-button
            :disabled="this.tableData.agent_storage > 10 ? true : false"
            @click="getnum()"
            >下一步</el-button
          >
          <!-- && this.tableData.agent_storage !=null -->
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogFormVisible: false,
      success: "1",
      faild: "2",

      timer: null,
      mod: "get_page_data",
      mod1: "get_storage_num",
      mod2: "check_info",
      total: 0,

      currentIndex: "",
      currentPage: 1, //初始页
      pagesize: 4, //    每页的数据

      tableData: [
        {
          agent_ip: "",
          hostname: "",
          hostname: "",
          agent_online_status: "",
          agent_arch: "",
          agent_os: "",
          agent_storage: "",
          agent_id: "",
          task_CreateTime: "",
          value1: "",
        },
      ],
      list: "3",
      multipleSelection: [],
    };
  },
  created() {
    this.check_info();
  },
  mounted() {
    this.timer = setInterval(() => {
      setTimeout(() => {
        this.getpagedata();

      }, 0);
    }, 5000);
  },
  beforeUpdate() {
    this.tableData.forEach((item) => {
      if (item.agent_storage != "" && item.agent_storage != "nullGB") {
        clearInterval(this.timer);

      }
    });
  },
  destroyed() {
    clearInterval(this.timer);
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    handleSizeChange: function (size) {
      this.pagesize = size;
      this.getpagedata();
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      this.getpagedata();
    },
    check_info() {
      this.$http
        .post("/check_info", {
          mod: this.mod2,
        })
        .then((res) => {
          // console.log("check_info");
        });
    },
    // 获取列表数据
    getpagedata() {
      this.$http
        .post("/get_page_data", {
          mod: this.mod,
        })
        .then((res) => {
          this.tableData = res.data.info;
          this.total = res.data.num;
        });
    },
    // 检查可用空间  定时器
    formatState: function (row, column, cellValue) {
      if (cellValue == "NoneGB" || cellValue == "") {
        return "检查中";
      } else {
        return cellValue;
      }
    },
  },
};
</script>

<style src="./index.css" scoped>
</style>
