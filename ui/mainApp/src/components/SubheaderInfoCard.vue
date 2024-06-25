<template>
  <div class="infoCard">
    <div class="infoIcon">i</div>
    <div>{{ info }}</div>
  </div>
</template>

<script>
export default {
  name: "SubheaderInfoCard",
  props: {
    info: String,
  },
};
</script>

<style scoped>
.infoCard {
  display: flex;
  justify-content: start;
  align-items: center;
  background-color: #ffffff;
  border-radius: 3px;
  border-color: #dddddd;
  border-style: solid;
  border-width: 1px;
  margin-top: 12px;
  padding: 10px 12px 10px 18px;
}

.infoIcon {
  width: 16px;
  height: 16px;
  border-radius: 8px;
  background-color: #5798d9;
  color: #ffffff;
  text-align: center;
  font-size: small;
  margin-right: 12px;
  margin-top: 4px; /* 汉字文本在视觉上略偏下，将图标向下调整，可使效果看起来在同一高度上 */
}
</style>
