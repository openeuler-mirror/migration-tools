<template>
  <div>
    <h1>{{ $root.data.packages_tabs.name }}</h1>
    <div style="width: 100%">
      <el-table :data="onShowList" style="width: 100%">
        <el-table-column
          :label="$root.data.packages_tabs.current_os_item.name"
          prop="current_os"
          width="400"
        ></el-table-column>
        <el-table-column
          :label="$root.data.packages_tabs.future_os_item.name"
          prop="future_os"
          width="400"
        ></el-table-column>
        <el-table-column
          :label="$root.data.packages_tabs.total_list_item.name"
          prop="total_list"
          width="400"
        ></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "PackagesTabs",
  data() {
    return {
      onShowList: [],
      current_os_item: [],
      future_os_item: [],
      total_list_item: [],
    };
  },
  created() {
    console.log("created @ PackagesTabs.vue");
    this.current_os_item = this.$root.data.packages_tabs.current_os_item.data;
    this.future_os_item = this.$root.data.packages_tabs.future_os_item.data;
    this.total_list_item = this.$root.data.packages_tabs.total_list_item.data;

    let length1 = this.current_os_item.length;
    let length2 = this.future_os_item.length;
    let lentth3 = this.total_list_item.length;

    // 数据长度不一致， 显示最大的长度
    let maxLenth = Math.max(length1, length2, lentth3);
    for (let i = 0; i < maxLenth; i++) {
      this.onShowList.push({
        current_os: this.current_os_item[i],
        future_os: this.future_os_item[i],
        total_list: this.total_list_item[i],
      });
    }
  },
};
</script>
