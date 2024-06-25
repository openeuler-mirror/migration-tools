<template>
  <div class="styledHeaderBlock">
    <div class="styledHeaderDecorateLine"></div>
    <h1 class="styledHeaderText">{{ subHeader }}</h1>
  </div>
</template>

<script>
export default {
  name: "StyledSubheaderBlock",
  props: {
    subHeader: String,
  },
};
</script>

<style scoped>
.styledHeaderBlock {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.styledHeaderText {
  margin: 5px 0px 5px 0px;
  color: #555555;
}

.styledHeaderDecorateLine {
  height: 18px;
  width: 3px;
  background-color: #003296;
  margin-right: 10px;
  margin-top: 2px;
}
</style>
