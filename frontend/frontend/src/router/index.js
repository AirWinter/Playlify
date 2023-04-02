import { createRouter, createWebHistory } from "vue-router";
import GetStarted from "../components/GetStarted.vue";
import PlaylistItem from "../components/PlaylistItem.vue";

const routes = [
  {
    path: "/get-started",
    name: "GetStarted",
    component: GetStarted,
  },
  {
    path: "/my-playlists",
    name: "PlaylistItem",
    component: PlaylistItem,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
