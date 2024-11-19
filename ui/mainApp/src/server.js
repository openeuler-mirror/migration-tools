// src/server.js
import { createServer, Model } from "miragejs";

export function makeServer({ environment = "development" } = {}) {
  let server = createServer({
    environment,
    logging: true,

    models: {
      machine: Model,

      //       {
      //   agent_ip: "192.168.31.100",
      //   hostname: "test1",
      //   agent_online_status: 0,
      //   agent_os: "centos7",
      //   migration_type: "new_expansion",
      //   agent_arch: "x86_64",
      //   failure_reasons: "",
      //   task_CreateTime: "2021-11-22 17:45:40",
      //   task_status: "00",
      // },
    },

    routes() {
      this.namespace = "";
      this.timing = 0;

      this.post("/check_info", (schema, request) => {
        return { data: "success" };
      });
      this.post("/import_host_info", (schema, request) => {
        let data = JSON.parse(request.requestBody).data;
        let num = 0;
        data.forEach((item) => {
          if (item.agent_ip) {
            let machine = {
              agent_ip: "",
              hostname: "",
              agent_online_status: 0,
              agent_os: "centos7",
              migration_type: "",
              agent_arch: "aarch64",
              failure_reasons: "",
              task_CreateTime: "",
              task_status: "00",
            };
            machine.agent_ip = item.agent_ip;
            machine.hostname = item.hostname;
            machine.migration_type = item.migration_type;
            machine.task_CreateTime = new Date().toLocaleString();
            schema.db.machines.insert(machine);
            num += 1;
          }
        });
        let ret = "success";
        if (num == 0) {
          ret = "failed";
        }
        return { data: ret, num: num };
      });

      this.post("/host_info_display", (schema, request) => {
        let num = schema.machines.all().length;
        console.log("/host_info_display", schema);
        let info = schema.db.machines;
        if (num && info) {
          return { info: info, num: num };
        }
        return { info: [], num: 0 };
      });
      this.post("/modify_migration_type", (schema, request) => {
        let info = JSON.parse(request.requestBody).info;
        let originAgent = schema.db.machines.findBy({
          agent_ip: info.agent_ip,
        });
        let ret = schema.db.machines.update(
          {
            agent_ip: originAgent.agent_ip,
            migration_type: originAgent.migration_type,
          },
          info
        );
        return { data: "success" };
      });

      this.post("/export_reports", (schema, request) => {
        return { data: "success" };
      });
      this.post("/get_page_data", (schema, request) => {
        let agentIpGroup = JSON.parse(request.requestBody).agent_ip;
        let storageSize = 9;
        let retInfo = [];
        agentIpGroup.forEach((item) => {
          let finder = schema.db.machines.findBy({ agent_ip: item });
          if (finder) {
            let agent = {
              //   agent_ip: "5.5.5.5",
              //   hostname: "localhost.localdomain",
              //   agent_online_status: 0,
              //   agent_os: "centos8",
              //   agent_storage: "14GB",
              //   agent_arch: "x86_64",
              //   agent_id: 1,
              //   task_CreateTime: "2021-11-23 21:24:15",
              agent_ip: finder.agent_ip,
              hostname: finder.hostname,
              agent_online_status: finder.agent_online_status,
              agent_os: finder.agent_os,
              agent_arch: finder.agent_arch,
              task_CreateTime: new Date(
                finder.task_CreateTime
              ).toLocaleString(),
              agent_storage: storageSize.toString() + "G",
            };
            storageSize += 1;
            retInfo.push(agent);
          }
        });
        return { num: retInfo.length, info: retInfo };
      });
      let repos = {};
      let repoChkCount = 3;
      this.post("/check_repo", (schema, request) => {
        let rBody = JSON.parse(request.requestBody);
        repos = {
          centos7_aarch64: rBody.centos7_aarch64 ?? "",
          centos7_x86: rBody.centos7_x86_64 ?? "",
          centos8_aarch64: rBody.centos8_aarch64 ?? "",
          centos8_x86: rBody.centos8_x86_64 ?? "",
        };
        return { data: "success" };
      });
      this.post("/check_add_repo", (schema, request) => {
        let rBody = JSON.parse(request.requestBody);
        repos = {
          migration_before_aarch64: rBody.migration_before_aarch64 ?? "",
          migration_before_x86_64: rBody.migration_before_x86_64 ?? "",
          migration_after_aarch64: rBody.migration_after_aarch64 ?? "",
          migration_after_x86_64: rBody.migration_after_x86_64 ?? "",
        };
        return { data: "success" };
      });
      function handleRepoCheck(schema, request) {
        repoChkCount += 1;
        let ret = {};
        console.log("/get_repo_data", repos);
        Object.keys(repos).forEach((key) => {
          if (repos[key] == "") {
            ret[key] = "success";
          } else if (repos[key].toString().startsWith("http")) {
            ret[key] = "success";
          } else if (repoChkCount % 3 == 0) {
            ret[key] = "failed";
          } else {
            ret[key] = "";
          }
        });
        return ret;
      }
      this.post("/get_repo_data", (schema, request) => {
        let ret = handleRepoCheck(schema, request);
        return ret;
      });
      repos = {};
      repoChkCount = 0;
      this.post("/get_add_repo_data", (schema, request) => {
        let ret = handleRepoCheck(schema, request);
        return ret;
      });
      this.post("/check_kernel", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/modify_task_status", (schema, request) => {
        let rBody = JSON.parse(request.requestBody);
        let agentIpGroup = rBody.agent_ip;
        agentIpGroup.forEach((item) => {
          let finder = schema.db.machines.findBy({ agent_ip: item });
          if (finder) {
            schema.db.machines.update(
              { agent_ip: finder.agent_ip },
              {
                task_status: 0,
              }
            );
          }
        });

        return "success";
      });
      this.post("/get_kernel_data", (schema, request) => {
        let rBody = JSON.parse(request.requestBody);
        let agentIpGroup = rBody.agent_ip;
        let info = [];
        agentIpGroup.forEach((item) => {
          let finder = schema.db.machines.findBy({ agent_ip: item });
          if (finder) {
            let agent = {
              agent_ip: finder.agent_ip,
              agent_kernel: "4.18.0-25-generic",
              agent_repo_kernel: ["不迁移内核", "4.19", "5.10"],
            };
            info.push(agent);
            schema.db.machines.update({ agent_ip: finder.agent_ip }, agent);
          }
        });
        return { info: info };
      });
      this.post("/check_environment", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/check_add_environment", (schema, request) => {
        return {
          data: "success",
        };
      });
      let envChkCount = 1;
      let taskStatus = 0;
      let taskProgress = 0;
      function handleTaskProgress(schema, request) {
        envChkCount += 1;
        taskProgress += 10;
        if (taskProgress > 100) {
          taskProgress = 100;
        }
        let rBody = JSON.parse(request.requestBody);
        let agentIpGroup = rBody.agent_ip;
        let info = [];
        let num = 10;
        agentIpGroup.forEach((item) => {
          let finder = schema.db.machines.findBy({ agent_ip: item });
          if (finder) {
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
              agent_ip: finder.agent_ip,
              task_status: taskStatus,
              progress: taskProgress,
            };
            info.push(agent);
          }
        });
        return info;
      }
      this.post("/get_environment_data", (schema, request) => {
        let info = handleTaskProgress(schema, request);
        return { info: info };
      });
      this.post("/get_add_environment_data", (schema, request) => {
        let info = handleTaskProgress(schema, request);
        return { info: info };
      });
      this.post("/system_migration", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/get_system_migration_data", (schema, request) => {
        let info = handleTaskProgress(schema, request);
        return { info: info };
      });
      this.post("/get_download_center_data", (schema, request) => {
        return {
          num: 6,
          info: [
            {
              task_Updatetime: "2021-12-01 04:03:43",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:03:43",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
            {
              task_Updatetime: "2021-12-01 04:05:32",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:05:32",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
            {
              task_Updatetime: "2021-12-01 04:21:18",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:21:18",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
            {
              task_Updatetime: "2021-12-01 04:22:09",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:22:09",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
            {
              task_Updatetime: "2021-12-01 04:40:38",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:40:38",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
            {
              task_Updatetime: "2021-12-01 04:57:01",
              report_name:
                "\u8fc1\u79fb\u4e3b\u673a\u5217\u8868_2021-12-01 04:57:01",
              report_type: "\u4e3b\u673a\u5217\u8868",
              agent_ip: "10.12.21.200",
              hostname: null,
              agent_os: "",
              agent_arch: "",
            },
          ],
        };
      });
      this.post("/migration_records", (schema, request) => {
        return {
          num: 6,
          info: [
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.1",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.2",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.3",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.4",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.5",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
            {
              create_time: "2022/3/28 15:38:22",
              agent_ip: "1.1.1.6",
              hostname: "localhost",
              agent_os: "CentOS 8",
              agent_migration_os: "UOS V20",
              agent_arch: "x86_64",
            },
          ],
        };
      });

      return server;
    },
  });
  server.db.loadData({
    machines: [
      {
        agent_ip: "192.168.31.100",
        hostname: "test1",
        agent_online_status: 0,
        agent_os: "centos7",
        migration_type: "new_expansion",
        agent_arch: "x86_64",
        failure_reasons: "",
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.101",
        hostname: "test2",
        agent_online_status: 0,
        agent_os: "centos7",
        migration_type: "new_expansion",
        agent_arch: "aarch64",
        failure_reasons: "",
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.102",
        hostname: "test3",
        agent_online_status: 0,
        agent_os: "centos8",
        migration_type: "stock_replacement",
        agent_arch: "x86_64",
        failure_reasons: null,
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.103",
        hostname: "test4",
        agent_online_status: 0,
        agent_os: "centos8",
        migration_type: "stock_replacement",
        agent_arch: "aarch64",
        failure_reasons: null,
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.104",
        hostname: "test1",
        agent_online_status: 1,
        agent_os: "centos7",
        migration_type: "new_expansion",
        agent_arch: "x86_64",
        failure_reasons: "",
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.105",
        hostname: "test2",
        agent_online_status: 1,
        agent_os: "centos7",
        migration_type: "new_expansion",
        agent_arch: "aarch64",
        failure_reasons: "",
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.106",
        hostname: "test3",
        agent_online_status: 1,
        agent_os: "centos8",
        migration_type: "stock_replacement",
        agent_arch: "x86_64",
        failure_reasons: null,
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
      {
        agent_ip: "192.168.31.107",
        hostname: "test4",
        agent_online_status: 1,
        agent_os: "centos8",
        migration_type: "stock_replacement",
        agent_arch: "aarch64",
        failure_reasons: null,
        task_CreateTime: "2021-11-22 17:45:40",
        task_status: "00",
      },
    ],
  });
}
