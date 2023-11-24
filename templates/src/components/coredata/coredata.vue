<template>
  <div class="box">
    <div class="head">
      <div class="head-1"></div>
      <span>选择迁移系统内核版本</span>
    </div>
    <el-card>
      <img src="./img/u189.png" alt="" />
      请在"迁移后OS内核"列下拉框中,选择迁移到新系统的内核版本
    </el-card>

    <el-card class="center">
      <el-row>
        <el-col :span="10" class="center-1">{{ this.total }}项</el-col>

        <el-col :span="13" class="center-1-2">
          <!-- <el-select v-model="value" placeholder="选择内核版本" class="selsect1" @change="fu1(value)">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select> -->

          <el-dropdown
            size="small"
            placement="bottom"
            trigger="click"
            @command="batchOperate"
            style="margin-left: 10px"
          >
            <el-button class="search-btn" size="mini">
              选择内核版本
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="batch_remarks"
                >不迁移内核</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </el-col>
      </el-row>
      <el-table
        ref="multipleTable"
        :data="
          xin2Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)
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
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          prop="agent_id"
          label="AgentID"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          prop="agent_ip"
          label="主机IP"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          prop="hostname"
          label="主机名"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          label="在线状态"
          align="center"
          :formatter="formatState"
        >
          <template slot-scope="scope">
            <el-col v-if="scope.row.agent_online_status == 0">在线</el-col>
            <el-col v-if="scope.row.agent_online_status == 1">离线</el-col>
          </template>
        </el-table-column>
        <el-table-column
          prop="agent_os"
          label="操作系统类型"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          prop="agent_arch"
          label="架构"
          align="center"
          :formatter="formatState"
        >
        </el-table-column>
        <el-table-column
          prop="agent_kernel"
          label="迁移前os内核"
          align="center"
        >
        </el-table-column>

        <el-table-column label="迁移后OS内核" align="center">
          <template slot-scope="scope">
            <el-select
              v-model="scope.row.value1"
              size="mini	"
              class="select2"
              v-if="kernel"
              placeholder="不迁移内核"
            >
              <el-option
                v-for="item in scope.row.agent_repo_kernel"
                :key="item"
                :label="item"
                :value="item"
              >
              </el-option>
            </el-select>
            <el-col v-if="iskernel">
              <el-select
                v-model="scope.row.value1"
                size="mini	"
                class="select2"
                placeholder="不迁移内核"
              >
              </el-select>
            </el-col>
          </template>
          <!-- @change="function2(value)" -->
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

          <el-button @click="go()">下一步</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  inject: ["reload"],
  data() {
    return {
      not: false,
      isnot: true,
      kernel: true,
      iskernel: false,
      mod: "check_kernel",
      mod1: "get_kernel_data",
      mod2: "modify_task_status",
      mod3: "close_tool",
      total: 0,
      currentIndex: "",
      currentPage: 1, //初始页
      pagesize: 4, //    每页的数据
      xin1Data: [
        {
          task_CreateTime: "",
          agent_id: "",
          agent_ip: "",
          hostname: "",
          agent_online_status: "",
          agent_os: " ",
          agent_arch: "",
          agent_kernel: "",
          agent_repo_kernel: "",
        },
      ],
      //  value1:"",
      undefined: "undefined",

      xin2Data: [
        {
          task_CreateTime: "",
          agent_id: "",
          agent_ip: "",
          hostname: "",
          agent_online_status: "",
          agent_os: " ",
          agent_arch: "",
          agent_kernel: "",
          agent_repo_kernel: "",
          value1: "不迁移内核",
        },
      ],
      options: [
        {
          value: "不迁移内核",
          label: "不迁移内核",
        },
      ],
      value: "",
      multipleSelection: [],
      deletionarr: [],
    };
  },
  created() {

    this.check_kernel();

    this.kernel_data();
  },
  mounted() {
    this.xin1Data = this.$store.state.softpathData;
          this.timer = setInterval(() => {
          setTimeout(() => {
            this.kernel_data();

          }, 0);
        }, 5000);

  },

  destroyed() {
    clearInterval(this.timer);
  },

  methods: {
    kernel_data() {
      this.$http
        .post("/get_kernel_data", {
          mod: this.mod1,
        })
        .then((res) => {
          console.log(res)
          this.total = res.data.num;
          this.xin2Data = res.data.info;

          for (var key in this.xin2Data) {
            this.xin1Data.map((item) => {
              if (this.xin2Data[key].agent_ip == item.agent_ip) {
                this.xin2Data[key].task_CreateTime = item.task_CreateTime;
                this.xin2Data[key].agent_id = item.agent_id;
                this.xin2Data[key].hostname = item.hostname;
                this.xin2Data[key].agent_online_status =
                  item.agent_online_status;
                this.xin2Data[key].agent_os = item.agent_os;
                this.xin2Data[key].agent_arch = item.agent_arch;
              }
            });
          }
          console.log(this.xin2Data)
           for (var key in this.xin2Data) {
      if (
        this.xin2Data[key].agent_kernel != "" &&
        this.xin2Data[key].agent_repo_kernel != ""
      ) {
           clearInterval(this.timer);
       }
    }
        });
    },
    batchOperate(command) {
      switch (command) {
        case "batch_remarks":
          this.dialogRemarks();
          break;
      }
    },

    dialogRemarks() {
      this.iskernel = true;
      this.kernel = false;
    },
    fu1(value) {
      if ((value = "‘不迁移内核’")) {
        this.xin2Data.agent_repo_kernel == "";
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    handleSizeChange: function (size) {
      this.pagesize = size;
      this.kernel_data();
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      this.kernel_data();
    },
    // 下发检测agent内核版本和软件仓库版本
    check_kernel() {
      this.$http
        .post("/check_kernel", {
          mod: this.mod,
        })
        .then((res) => {
          // console.log(res)
        });
    },
    formatState: function (row, column, cellValue) {
      if (cellValue == null || cellValue == "") {
        return "--";
      } else {
        // clearInterval(this.timer);
        return cellValue;
      }
    },

    go() {
      this.$router.push("/transferlist");
      this.$store.commit("coreData", this.xin2Data);
      this.$http
        .post("/modify_task_status", {
          mod: this.mod2,
        })
        .then((res) => {
          // console.log(res)
        });
    },
    err() {
      this.$confirm("确定退出吗, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$router.push("/hostment");

          this.$message({ type: "success", message: "退出成功!" });
        })
        .catch(() => {
          this.$message({ type: "info", message: "用户已取消" });
        });
    },
  },
};
</script>

<style src="./index.css" scoped>
</style>
