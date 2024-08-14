import localStorageDB from "localstoragedb";

let database = null;
const _create = () => {
  var db = new localStorageDB("apiMock", "localStorage");
  if (db.isNew()) {
    db.createTable("hosts", [
      "id",
      "agent_ip",
      "agent_username",
      "agent_passwd",
      "hostname",
      "agent_os",
      "agent_arch",
      "agent_storage",
      "agent_kernel",
      "agent_repo_kernel",
      "agent_migration_os",
      "failure_reasons", // 和后端实际数据库字段不一致
      "task_CreateTime",
      "task_status",
      "agent_online_status",
      "migration_type",
      "task_Updatetime",
      "report_type",
      "report_name",
    ]);
  }

  let cnt = 128;
  for (var i = 1; i <= cnt; i++) {
    let id = i;
    let agent_ip = "192.168.1." + i;
    let hostname = "hostname" + i;
    let agent_online_status = i % (cnt / 2) < cnt / 4 ? 0 : 1;
    let agent_os = i % (cnt / 4) < cnt / 8 ? "centos7" : "centos8";
    let agent_arch = i % (cnt / 8) < cnt / 16 ? "x86_64" : "aarch64";
    let migration_type =
      i % (cnt / 16) < cnt / 32 ? "new_expansion" : "stock_replacement";
    let task_status = "00";
    let failure_reasons = "";
    if (i % (cnt / 32) < cnt / 64) {
      task_status = "00";
    } else if (i % (cnt / 64) < cnt / 64 / 2) {
      task_status = "01";
    } else if (i % (cnt / 64 / 2) < cnt / 64) {
      task_status = "08";
      failure_reasons = "失败原因" + i;
    }
    // types = {
    //   UOS_analysis_report_add: "迁移检测报告-新增扩容",
    //   UOS_analysis_report: "迁移检测报告-存量替换",
    //   UOS_migration_completed_report: "迁移分析报告",
    //   UOS_migration_log: "日志",
    // };
    let report_type = "迁移检测报告-存量替换";
    let report_name = "UOS_analysis_report_" + agent_ip + ".html";
    if (i % 6 == 1) {
      report_type = "迁移分析报告";
      let report_name = "UOS_migration_completed_report_" + agent_ip + ".html";
    } else if (i % 6 == 2) {
      report_type = "迁移检测报告-存量替换";
      report_name = "UOS_analysis_report_" + agent_ip + ".html";
    } else if (i % 6 == 3) {
      report_type = "迁移检测报告-新增扩容";
      report_name = "UOS_analysis_report_add_" + agent_ip + ".html";
    } else if (i % 6 == 4) {
      report_type = "日志";
      report_name = "UOS_migration_log_" + agent_ip + ".log";
    } else if (i % 6 == 5) {
      report_type = "主机列表";
      report_name = "UOS_host_list_" + agent_ip + ".xlsx";
    } else if (i % 6 == 0) {
      report_type = "迁移成功主机列表";
      report_name = "UOS_migration_success_host_list_" + agent_ip + ".xlsx";
    }
    let task_CreateTime = new Date().toLocaleString("zh-CN");
    if (db.queryAll("hosts").length < cnt) {
      db.insert("hosts", {
        id: id,
        agent_ip: agent_ip,
        hostname: hostname,
        agent_os: agent_os,
        agent_arch: agent_arch,
        failure_reasons: failure_reasons,
        task_CreateTime: task_CreateTime,
        task_status: task_status,
        agent_online_status: agent_online_status,
        migration_type: migration_type,
        agent_username: "",
        agent_passwd: "",
        agent_storage: "",
        agent_kernel: "4.19.0-21-generic",
        agent_repo_kernel: [
          "不迁移内核",
          "4.19.0-21-generic",
          "5.1.0-21-generic",
        ],
        agent_migration_os: "UOS V20",
        task_Updatetime: task_CreateTime,
        report_type: report_type,
        report_name: report_name,
      });
    }
  }
  // commit the database to localStorage
  // all create/drop/insert/update/delete operations should be committed
  db.commit();
  return db;
};

export const getDatabase = () => {
  if (database === null) {
    database = _create();
  }
  return database;
};
