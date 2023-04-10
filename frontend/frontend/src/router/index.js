import { createRouter, createWebHistory } from "vue-router";
import PlaylistItem from "../components/PlaylistItem.vue";
import MultiStepV2 from "../components/MultiStepV2.vue";
import GetStartedView from "../views/GetStartedView.vue";
import PageNotFoundView from "../views/PageNotFoundView.vue";

const routes = [
  {
    path: "/",
    name: "GetStartedView",
    component: GetStartedView,
  },
  {
    path: "/my-playlists",
    name: "PlaylistItem",
    component: PlaylistItem,
  },
  {
    path: "/multi-step-v2",
    name: "MultiStepV2",
    component: MultiStepV2,
  },
  {
    path: "/:catchAll(.*)*",
    name: "PageNotFoundView",
    component: PageNotFoundView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
