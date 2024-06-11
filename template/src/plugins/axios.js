import Vue from 'vue'
import axios from 'axios'
// axios.defaults.withCredentials=true;
axios.defaults.baseURL="http://10.12.21.202:9999"

Vue.prototype.$http=axios