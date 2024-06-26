// src/server.js
import { createServer, Model } from "miragejs";

export function makeServer({ environment = "development" } = {}) {
  let server = createServer({
    environment,

    models: {
      user: Model,
    },

    seeds(server) {
      server.create("user", { name: "Bob" });
      server.create("user", { name: "Alice" });
    },

    routes() {
      this.namespace = "";

      this.get("/users", (schema) => {
        return schema.users.all();
      });
      this.post("/import_host_info", (schema, request) => {
        return { data: "success", num: 2 };
        // return { data: "failed", };
      });
      this.post("/host_info_display", (schema, request) => {
        return {
          num: 18,
          page: 1,
          size: 5,
          info: [
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.10",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.20",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "新增扩容",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.30",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "迁移中",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.4",
              agent_hostname: "user",
              agent_status: "离线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.5",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.6",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.7",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.8",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "迁移中",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.9",
              agent_hostname: "user",
              agent_status: "离线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.10",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.11",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.12",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.13",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "迁移中",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.14",
              agent_hostname: "user",
              agent_status: "离线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.15",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "迁移错误",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.16",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: "- -",
              agent_ip: "1.1.1.17",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "未迁移",
              failure_reasons: "- -",
            },
            {
              task_CreateTime: 2,
              agent_ip: "1.1.1.18",
              agent_hostname: "user",
              agent_status: "在线",
              agent_os: "Centos 8",
              agent_arch: "x86",
              migration_type: "存量替换",
              task_status: "迁移中",
              failure_reasons: "迁移错误",
            },
          ],
        };
      });
      this.post("/get_page_data", (schema, request) => {
        return {
          info: [
            {
              agent_ip: "1.1.1.1",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 8",
              agent_arch: "x86_64",
              agent_storage: "",
              agent_id: 1,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "2.2.2.2",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 7",
              agent_arch: "x86_64",
              agent_storage: "4GB",
              agent_id: 2,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "3.3.3.3",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 8",
              agent_arch: "aarch64",
              agent_storage: "10GB",
              agent_id: 1,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "4.4.4.4",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 7",
              agent_arch: "aarch64",
              agent_storage: "12GB",
              agent_id: 2,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "5.5.5.5",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 8",
              agent_arch: "x86_64",
              agent_storage: "12GB",
              agent_id: 1,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "6.6.6.6",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 7",
              agent_arch: "x86_64",
              agent_storage: "12GB",
              agent_id: 2,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "7.7.7.7",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 8",
              agent_arch: "aarch64",
              agent_storage: "22GB",
              agent_id: 1,
              task_CreateTime: "xxx",
            },
            {
              agent_ip: "8.8.8.8",
              hostname: "user",
              agent_online_status: 0,
              agent_os: "Centos 7",
              agent_arch: "aarch64",
              agent_storage: "41GB",
              agent_id: 2,
              task_CreateTime: "xxx",
            },
          ],
        };
      });
      this.post("/modify_migration_type", (schema, request) => {
        return { data: "success" };
      });
      this.post("/check_repo", (schema, request) => {
        return { data: "success" };
      });
      this.post("/get_repo_data", (schema, request) => {
        return {
          centos7_x86: "success",
          centos8_x86: "success",
          centos7_aarch64: "success",
          centos8_aarch64: "success",
        };
      });
      this.post("/check_kernel", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/get_kernel_data", (schema, request) => {
        return {
          info: [
            {
              agent_ip: "1.1.1.1",
              agent_kernel: "4.19",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "2.2.2.2",
              agent_kernel: "4.18",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "3.3.3.3",
              agent_kernel: "4.19",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "4.4.4.4",
              agent_kernel: "4.18",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "5.5.5.5",
              agent_kernel: "4.18",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "6.6.6.6",
              agent_kernel: "4.19",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "7.7.7.7",
              agent_kernel: "4.18",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "8.8.8.8",
              agent_kernel: "4.19",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
            {
              agent_ip: "9.9.9.9",
              agent_kernel: "4.18",
              agent_repo_kernel: "4.18,4.19,5.10",
            },
          ],
        };
      });
      this.post("/check_environment", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/get_environment_data", (schema, request) => {
        return {
          info: [
            { agent_ip: "1.1.1.1", task_status: 0, progress: 60 },
            { agent_ip: "2.2.2.2", task_status: 1, progress: 60 },
            { agent_ip: "3.3.3.3", task_status: 2, progress: 60 },
            { agent_ip: "4.4.4.4", task_status: 3, progress: 60 },
            { agent_ip: "5.5.5.5", task_status: 0, progress: 60 },
            { agent_ip: "6.6.6.6", task_status: 1, progress: 60 },
            { agent_ip: "7.7.7.7", task_status: 2, progress: 60 },
            { agent_ip: "8.8.8.8", task_status: 3, progress: 60 },
            { agent_ip: "9.9.9.9", task_status: 1, progress: 60 },
          ],
        };
      });
      this.post("/system_migration", (schema, request) => {
        return {
          data: "success",
        };
      });
      this.post("/get_system_migration_data", (schema, request) => {
        return {
          info: [
            { agent_ip: "1.1.1.1", task_status: 0, progress: 60 },
            { agent_ip: "2.2.2.2", task_status: 1, progress: 60 },
            { agent_ip: "3.3.3.3", task_status: 2, progress: 60 },
            { agent_ip: "4.4.4.4", task_status: 3, progress: 60 },
            { agent_ip: "5.5.5.5", task_status: 0, progress: 60 },
            { agent_ip: "6.6.6.6", task_status: 1, progress: 60 },
            { agent_ip: "7.7.7.7", task_status: 2, progress: 60 },
            { agent_ip: "8.8.8.8", task_status: 3, progress: 60 },
            { agent_ip: "9.9.9.9", task_status: 2, progress: 60 },
          ],
        };
      });

      return server;
    },
  });
}
