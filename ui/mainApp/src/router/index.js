import { createRouter, createWebHashHistory } from "vue-router";
import ImportMachine from "../views/ImportMachine.vue";
import MachineManagement from "../views/MachineManagement.vue";
import DownloadCenter from "../views/DownloadCenter.vue";
import MigrationHistory from "../views/MigrationHistory.vue";
import MigrationAnalyze from "../views/MigrationAnalyze.vue";
import MigrationNotice from "../views/MigrationNotice.vue";
import MigrateMachine from "../views/MigrateMachine.vue";
import CheckAvalibleSpace from "../views/CheckAvalibleSpace.vue";
import SetRepo from "../views/SetRepo.vue";
import SelectMigrateKernel from "../views/SelectMigrateKernel.vue";
import EnvCheckBeforeMigrate from "../views/EnvCheckBeforeMigrate.vue";
import MigrateRunning from "../views/MigrateRunning.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: ImportMachine,
  },
  {
    path: "/import-machine",
    name: "ImportMachine",
    component: ImportMachine,
  },
  {
    path: "/machine-management",
    name: "MachineManagement",
    component: MachineManagement,
  },
  {
    path: "/download-center",
    name: "DownloadCenter",
    component: DownloadCenter,
  },
  {
    path: "/migration-history",
    name: "MigrationHistory",
    component: MigrationHistory,
  },
  {
    path: "/migration-analyze",
    name: "MigrationAnalyze",
    component: MigrationAnalyze,
  },
  {
    path: "/migration-notice",
    name: "MigrationNotice",
    component: MigrationNotice,
  },
  {
    path: "/migrate-machine",
    name: "MigrateMachine",
    component: MigrateMachine,
  },
  {
    path: "/check-avalible-space",
    name: "CheckAvalibleSpace",
    component: CheckAvalibleSpace,
  },
  {
    path: "/set-repo",
    name: "SetRepo",
    component: SetRepo,
  },
  {
    path: "/select-migrate-kernel",
    name: "SelectMigrateKernel",
    component: SelectMigrateKernel,
  },
  {
    path: "/env-check-before-migrate",
    name: "EnvCheckBeforeMigrate",
    component: EnvCheckBeforeMigrate,
  },
  {
    path: "/migrate-running",
    name: "MigrateRunning",
    component: MigrateRunning,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
