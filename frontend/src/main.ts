import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/store";
// install bootstrap first
import "bootstrap/dist/css/bootstrap.css";
// FormKit imports
import { plugin as formKitPlugin, defaultConfig } from "@formkit/vue";
import { createMultiStepPlugin } from "@formkit/addons";
import "@formkit/themes/genesis";
import "@formkit/addons/css/multistep";
import "./assets/tailwind.css";

createApp(App)
  .use(
    formKitPlugin,
    defaultConfig({
      plugins: [
        createMultiStepPlugin({ tabStyle: "progress", allowIncomplete: false }),
      ],
      // inputs: {basicTagsList},
    })
  )
  .use(router)
  .use(store)
  .mount("#app");
