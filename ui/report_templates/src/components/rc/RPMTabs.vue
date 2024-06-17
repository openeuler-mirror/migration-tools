<template>
  <div>
    <h1>{{ $root.data.rpm_tabs.name }}</h1>
    <el-row justify="end">
      <el-col :span="6">
        <el-input
          v-model="search"
          placeholder="按包名搜索 RPM 包（不区分大小写）"
        />
      </el-col>
    </el-row>
    <div style="width: 100%">
      <el-table
        :data="
          onShowList.filter(
            (data) =>
              !search || data.name.toLowerCase().includes(search.toLowerCase())
          )
        "
        style="width: 100%"
      >
        <!-- 包名 -->
        <el-table-column label="包名" prop="name" sortable></el-table-column>
        <!-- 是否兼容 -->
        <el-table-column
          label="是否兼容"
          prop="is_compatible"
          align="center"
          sortable
          :filters="[
            { text: '兼容', value: true },
            { text: '不兼容', value: false },
          ]"
          :filter-method="filterCompatible"
        >
          <template #default="scope">
            <el-tag
              :type="scope.row.is_compatible ? 'success' : 'danger'"
              disable-transitions
              >{{ scope.row.is_compatible ? "兼容" : "不兼容" }}</el-tag
            >
          </template>
        </el-table-column>
        <!-- 当前版本 -->
        <el-table-column
          label="当前版本"
          prop="current_version"
          align="center"
        ></el-table-column>
        <!-- uos 版本 -->
        <el-table-column
          label="uos 版本"
          prop="future_version"
          align="center"
        ></el-table-column>
        <!-- 不兼容类型 -->
        <el-table-column
          label="不兼容类型"
          prop="incompatible_type"
          align="center"
          sortable
          sort-by="string"
        ></el-table-column>
        <!-- 不兼容来源 -->
        <el-table-column
          label="不兼容来源"
          prop="incompatible_source"
          align="center"
        ></el-table-column>
        <!-- 说明 -->
        <el-table-column
          label="说明"
          prop="description"
          width="500"
          align="center"
        ></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
export default {
  name: "RPMTabs",
  data() {
    return {
      onShowList: [],
      rpm_data: [],
      search: "",
    };
  },
  created() {
    console.log("created @ RPMTabs.vue");
    this.rpm_data = this.$root.data.rpm_tabs.data;
    console.log(this.rpm_data);

    for (let i = 0; i < this.rpm_data.length; i++) {
      this.onShowList.push({
        name: this.rpm_data[i].name,
        is_compatible: this.rpm_data[i].is_compatible,
        current_version: this.rpm_data[i].current_version,
        future_version: this.rpm_data[i].future_version,
        incompatible_type: this.rpm_data[i].incompatible_type,
        incompatible_source: this.rpm_data[i].incompatible_source,
        description: this.rpm_data[i].description,
      });
    }
  },
  methods: {
    filterCompatible(value, row) {
      return row.is_compatible === value;
    },
  },
};
</script>

<style></style>
