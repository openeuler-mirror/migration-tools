<template>
  <div class="header">
    <div>
      <span style="font-size: 20px">{{ name }}</span>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Header",
  setup() {
    // 在组件创建前执行, 无法使用 this , 用于接收 props 等
    const router = useRouter(); // 取当前的路由实例。const 代表常量，但该常量仅仅是“绑定不可变”
    const pathMap = {
      // 路由（页面）与标题的对应关系
      Home: "导入主机",
      ImportMachine: "导入主机",
      MachineManagement: "主机管理",
      MigrationAnalyze: "主机管理",
      MigrateMachine: "主机管理",
      MigrationNotice: "主机管理",
      CheckAvalibleSpace: "主机管理",
      SetRepo: "主机管理",
      SelectMigrateKernel: "主机管理",
      DownloadCenter: "下载中心",
      MigrationHistory: "迁移记录",
    };
    const state = reactive({
      // 定义 "响应式数据对象"。这是个对象，只不过可以响应式变化
      name: "Overview",
    });
    router.afterEach((to) => {
      // 这是个钩子。每次路由跳转后，变化到的路由都会作为参数 to 传进来
      console.log(to); // 可以看看 to 里面有什么
      state.name = pathMap[to.name];
    });

    return {
      // 这里返回的任何内容都可以用于组件的其余部分
      ...toRefs(state), // 前置 "..." 是 【展开运算符】
    };
  },
};
</script>

<style scoped>
.header {
  height: 52px;
  border-bottom: 1px solid #e9e9e9;
  background-color: #3a3f45;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
</style>
