import { createRouter, createWebHistory } from "vue-router";
import GetStarted from "../components/GetStarted.vue";
import PlaylistItem from "../components/PlaylistItem.vue";
import CreatePlaylist from "../components/CreatePlaylist.vue";
import MultiStep from "../components/MultiStep.vue";

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
  {
    path: "/create-playlist",
    name: "CreatePlaylist",
    component: CreatePlaylist,
  },
  {
    path: "/multi-step",
    name: "MultiStep",
    component: MultiStep,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
