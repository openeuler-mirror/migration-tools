<template>
  <div id="app">
       <router-view v-if="isShow"></router-view>
 
  </div>
</template>

<script>
export default {
  data(){
    return{
      isShow:true
    }
  },
  provide(){
    return{
      reload:this.reload
    }
  },
  methods: {
    reload(){
      this.isShow=false
      this.$nextTick(()=>{
        this.isShow=true
      })
    }
  },

}
</script>

<style >
*{
  padding: 0;
  margin: 0;
}

</style>
