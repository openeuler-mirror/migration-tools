import { createApp } from 'vue'
import App from './App.vue'
import installElementPlus from './plugins/element'
import axios from 'axios'
import VueAxios from 'vue-axios'


const app = createApp(App);
app.use(VueAxios, axios);
installElementPlus(app);
app.mount('#app');