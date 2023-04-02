import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
// install bootstrap first
import "bootstrap/dist/css/bootstrap.css";
// install formkit before
import { plugin, defaultConfig } from "@formkit/vue";

createApp(App).use(router).use(plugin, defaultConfig).mount("#app");
