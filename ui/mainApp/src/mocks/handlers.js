import { rest } from "msw";
import { getDatabase } from "./database";

let storageChkCnt = 0;
let repoChkCnt = 0;
let repos = {};

let envChkCount = 1;
let taskStatus = 0;
let taskProgress = 0;

export const handlers = [
  rest.post("/import_host_info", (req, res, ctx) => {
    const data = req.body.data;
    let num = 0;
    for (let i = 0; i < data.length; i++) {
      const host = data[i];
      const db = getDatabase();
      const id = db.insert("hosts", host);
      if (id) {
        num++;
        db.commit();
      }
    }
    let result = "success";
    if (num == 0) {
      result = "failed";
    }
    return res(
      ctx.json({
        data: result,
        num: num,
      })
    );
  }),

  rest.post("check_info", (req, res, ctx) => {
    return res(
      ctx.json({
        data: "success",
      })
    );
  }),

  rest.post("/host_info_display", (req, res, ctx) => {
    const hosts = getDatabase().queryAll("hosts");
    const filterHosts = hosts.map((item) => {
      return {
        agent_ip: item.agent_ip,
        hostname: item.hostname,
        agent_online_status: item.agent_online_status,
        agent_os: item.agent_os,
        migration_type: item.migration_type,
        agent_arch: item.agent_arch,
        failure_reasons: item.failure_reasons,
        task_CreateTime: item.task_CreateTime,
        task_status: item.task_status,
      };
    });
    return res(
      ctx.json({
        num: filterHosts.length,
        info: filterHosts,
      })
    );
  }),

  rest.post("/modify_migration_type", (req, res, ctx) => {
    let info = req.body.info;
    let db = getDatabase();
    db.update("hosts", { agent_ip: info.agent_ip }, function (row) {
      row.migration_type = info.migration_type;
      return row;
    });
    db.commit();

    return res(
      ctx.json({
        data: "success",
      })
    );
  }),

  rest.post("/get_page_data", (req, res, ctx) => {
    const reqHosts = req.body.agent_ip;
    const hosts = getDatabase().queryAll("hosts");
    let filterHosts = hosts.filter((item) => {
      return reqHosts.includes(item.agent_ip);
    });
    filterHosts = filterHosts.map((item) => {
      return {
        agent_ip: item.agent_ip,
        hostname: item.hostname,
        agent_online_status: item.agent_online_status,
        agent_arch: item.agent_arch,
        agent_os: item.agent_os,
        agent_id: item.id,
        task_CreateTime: item.task_CreateTime,
      };
    });
    let agent_storage = "";
    storageChkCnt++;
    for (let i = 0; i < filterHosts.length; i++) {
      if (storageChkCnt > 1) {
        agent_storage = i % 2 == 0 ? "7G" : 7 + i + "G";
      }
      filterHosts[i].agent_storage = agent_storage;
    }

    return res(
      ctx.json({
        num: filterHosts.length,
        info: filterHosts,
      })
    );
  }),

  rest.post("/check_repo", (req, res, ctx) => {
    repos = {
      centos7_aarch64: req.body.centos7_aarch64,
      centos7_x86: req.body.centos7_x86_64,
      centos8_aarch64: req.body.centos8_aarch64,
      centos8_x86: req.body.centos8_x86_64,
    };

    return res(
      ctx.json({
        data: "success",
      })
    );
  }),

  rest.post("/check_add_repo", (req, res, ctx) => {
    repos = {
      migration_before_aarch64: req.body.migration_before_aarch64,
      migration_before_x86_64: req.body.migration_before_x86_64,
      migration_after_aarch64: req.body.migration_after_aarch64,
      migration_after_x86_64: req.body.migration_after_x86_64,
    };
    return res(
      ctx.json({
        data: "success",
      })
    );
  }),

  rest.post(/get_repo_data|get_add_repo_data/, (req, res, ctx) => {
    const ret = {};
    repoChkCnt++;
    Object.keys(repos).forEach((key) => {
      if (repos[key].toString().startsWith("http")) {
        ret[key] = "success";
      } else if (repoChkCnt % 2 == 0) {
        ret[key] = "failed";
      } else {
        ret[key] = "";
      }
    });
    return res(ctx.json(ret));
  }),

  rest.post("/check_kernel", (req, res, ctx) => {
    return res(ctx.json({ data: "success" }));
  }),

  rest.post("/get_kernel_data", (req, res, ctx) => {
    let agentIpGroup = req.body.agent_ip;
    const hosts = getDatabase().queryAll("hosts");
    const filterHosts = hosts.filter((item) => {
      return agentIpGroup.includes(item.agent_ip);
    });
    const filterKernel = filterHosts.map((item) => {
      return {
        agent_ip: item.agent_ip,
        agent_kernel: item.agent_kernel,
        agent_repo_kernel: item.agent_repo_kernel,
      };
    });
    return res(ctx.json({ info: filterKernel }));
  }),

  rest.post("/modify_task_status", (req, res, ctx) => {
    return res(ctx.body("success"));
  }),

  rest.post(
    /check_environment|check_add_environment|system_migration/,
    (req, res, ctx) => {
      return res(ctx.json({ data: "success" }));
    }
  ),

  rest.post(
    /get_environment_data|get_add_environment_data|get_system_migration_data/,
    (req, res, ctx) => {
      envChkCount++;
      taskProgress += 10;
      if (taskProgress > 100) taskProgress = 100;
      const agentIpGroup = req.body.agent_ip;
      const info = [];
      const num = 10;
      const hosts = getDatabase().queryAll("hosts");
      const filterHosts = hosts.filter((item) => {
        return agentIpGroup.includes(item.agent_ip);
      });

      agentIpGroup.forEach((item) => {
        if (envChkCount % num < num && envChkCount % num > 0) {
          taskStatus = 1;
        }
        if (envChkCount % num == 0 || taskProgress == 100) {
          taskStatus = 2;
          taskProgress = 0;
        }
        if (envChkCount % (num + 1) == 0) {
          taskStatus = 3;
          taskProgress = 0;
        }
        if (envChkCount % (num + 2) == 0) {
          taskStatus = 4;
          taskProgress = 0;
        }
        let agent = {
          agent_ip: item,
          task_status: taskStatus,
          progress: taskProgress,
        };
        info.push(agent);
      });

      return res(ctx.json({ info: info }));
    }
  ),

  rest.post("/export_reports", (req, res, ctx) => {
    let date = new Date()
      .toLocaleString("zh-CN")
      .replace(/\//g, "")
      .replace(/:/g, "");
    let filename = "UOS_host_info_" + date + ".xls";
    let filetype =
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    if (req.body.reports_type == "export_host_info") {
      filename = "UOS_host_info_" + date + ".xls";
      filetype =
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    }
    if (req.body.reports_type == "uos_migration_log") {
      filename = "UOS_migration_log_" + date + ".log";
      filetype = "text/plain";
    }
    if (req.body.reports_type == "migration_success_list") {
      filename = "UOS_migration_success_list_" + date + ".xls";
      filetype =
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    }
    if (req.body.reports_type == "analysis_report") {
      filename = "UOS_analysis_report_" + date + ".html";
      filetype = "text/html";
    }
    if (req.body.reports_type == "migration_completed_report") {
      filename = "UOS_migration_completed_report_" + date + ".html";
      filetype = "text/html";
    }
    if (req.body.reports_type == "analysis_report_add") {
      filename = "UOS_analysis_report_add_" + date + ".html";
      filetype = "text/html";
    }

    let file = new File([], filename, {
      type: filetype,
    });

    return res(
      ctx.set("Content-Disposition", `attachment; filename=${file.name}`),
      ctx.set("Content-Type", file.type),
      ctx.body(file)
    );
  }),

  rest.post("/get_download_center_data", (req, res, ctx) => {
    let hosts = getDatabase().queryAll("hosts");
    let filterHosts = hosts.map((item) => {
      return {
        task_Updatetime: item.task_Updatetime,
        report_name: item.report_name,
        report_type: item.report_type,
        agent_ip: item.agent_ip,
        hostname: item.hostname,
        agent_os: item.agent_os,
        agent_arch: item.agent_arch,
      };
    });
    return res(
      ctx.json({
        num: filterHosts.length,
        info: filterHosts,
      })
    );
  }),

  rest.post("/migration_records", (req, res, ctx) => {
    let hosts = getDatabase().queryAll("hosts");
    let filterHosts = hosts.map((item) => {
      return {
        create_time: item.task_Updatetime,
        agent_ip: item.agent_ip,
        hostname: item.hostname,
        agent_os: item.agent_os,
        agent_migration_os: item.agent_migration_os,
        agent_arch: item.agent_arch,
      };
    });
    return res(
      ctx.json({
        num: filterHosts.length,
        info: filterHosts,
      })
    );
  }),
];
