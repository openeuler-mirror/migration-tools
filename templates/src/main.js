import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI);

import './plugins/element.js'
// 引入axios
import  './plugins/axios'


import dayjs from "dayjs"
Vue.prototype.dayjs=dayjs

// import VueResource from "vue-resource"

Vue.config.productionTip = false

// import qs from 'qs'
// Vue.prototype.$qs = qs





new Vue({
  // VueResource,
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
