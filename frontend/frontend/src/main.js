import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
// install bootstrap first
import "bootstrap/dist/css/bootstrap.css";
// FormKit imports
import { plugin as formKitPlugin, defaultConfig } from "@formkit/vue";
import { createMultiStepPlugin } from "@formkit/addons";
import "@formkit/themes/genesis";
import "@formkit/addons/css/multistep";
import "@formkit/pro/genesis";
import { createProPlugin, inputs } from "@formkit/pro";
import "./assets/tailwind.css";
// import BasicTagsList from "./components/shared/molecules/BasicTagsList.vue";

const pro = createProPlugin("fk-8a4f44be10", inputs);

// const basicTagsList = createInput(BasicTagsList, {
//       props: ["tags"],
//     });

createApp(App)
  .use(
    formKitPlugin,
    defaultConfig({
      plugins: [
        createMultiStepPlugin({ tabStyle: "progress", allowIncomplete: false }),
        pro,
      ],
      // inputs: {basicTagsList},
    })
  )
  .use(router)
  .mount("#app");
