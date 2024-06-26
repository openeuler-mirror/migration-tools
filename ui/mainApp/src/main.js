import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { makeServer } from "./server";

import axios from "axios";
import VueAxios from "vue-axios";
import installElementPlus from "./plugins/element";

if (process.env.NODE_ENV === "development") {
  makeServer();
}

const app = createApp(App);

app.use(VueAxios, axios);
installElementPlus(app);
app.use(router);
app.mount("#app");
