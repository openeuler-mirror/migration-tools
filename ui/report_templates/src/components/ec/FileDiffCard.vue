<template>
  <h3>{{ name }}</h3>
  <div v-for="item in items" :key="item" class="confBlockItem">
    <div @click="toggleShow(item)" class="flexBox">
      <div class="leftIconBox">
        <img
          src="@/assets/forward.svg"
          :class="{
            arrowIcon: !item.show,
            arrowIconRotate: item.show,
          }"
        />
      </div>
      <div class="left">
        <b> {{ item.confName }}</b>
        <div>{{ item.desc }}</div>
      </div>
      <div class="spacing"></div>
      <div v-if="item.show">
        <div v-html="item.diffHtml"></div>
      </div>
    </div>
  </div>
</template>

<script>
import "highlight.js/styles/github.css";
import "diff2html/bundles/css/diff2html.min.css";
export default {
  name: "FileDiffCard",
  props: {
    // TODO: 去除用于开发时设置的默认值，
    name: {
      type: String,
      default: "aaa",
    },
    items: Array,
  },
  methos: {
    toggleShow: function (item) {
      item.show = !item.show;
    },
  },
};
</script>

<style scoped>
.arrowIcon {
  width: 20px;
  height: 20px;
}
.arrowIconRotate {
  width: 20px;
  height: 20px;
  transform: rotate(90deg);
}
.confBlockItem {
  margin: 0px 0px 15px 0px;
  border-radius: 4px;
  border-style: solid;
  border-width: 1px;
  border-color: #dddddd;
  background: #fefefe;
  transition: background 0.2s;
}
.confBlockItem:hover {
  margin: 0px 0px 15px 0px;
  background: #f8f8f8;
}
.confBlockTitle {
  padding: 15px 15px 15px 15px;
}
.confBlockDiffBackground {
  margin: 0px 15px 0px 15px;
  border-radius: 4px;
  background: #ffffff;
}
.flexBox {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px 15px 10px 15px;
}
.left {
  vertical-align: center;
  float: left;
}
.leftIconBox {
  vertical-align: center;
  flex-basis: 20px;
  margin: 0 10px 0 0;
  height: 20px;
}
.right {
  vertical-align: center;
  float: right;
}
.spacing {
  vertical-align: center;
  flex-grow: 1;
}
</style>
