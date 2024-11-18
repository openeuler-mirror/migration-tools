<template>
  <h1>系统修改配置导出</h1>
  <FileDiffCard
    v-for="config in confData"
    :key="config"
    :name="config.confGroupName"
    :items="config.confList"
  ></FileDiffCard>
</template>

<script>
import FileDiffCard from "./FileDiffCard.vue";
import * as diff from "diff2html";

export default {
  name: "SysConfFileTabs",
  props: ["tabsData"],
  components: { FileDiffCard },
  data() {
    return {
      confData: [],
    };
  },
  created() {
    console.log("SysConfFileTabs created, tabsData:", this.tabsData);
    this.confData = this.tabsData.data;
    for (let i = 0; i < this.confData.length; i++) {
      for (let j = 0; j < this.confData[i].confList.length; j++) {
        this.confData[i].confList[j].show = true;
        this.confData[i].confList[j].diffHtml = diff.html(
          diff.parse(this.confData[i].confList[j].diffContent),
          {
            drawFileList: false,
            matching: "lines",
            outputFormat: "side-by-side",
            diffStyle: "char",
          }
        );
      }
    }
  },
};
</script>

<style scoped></style>
