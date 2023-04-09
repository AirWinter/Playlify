import { createRouter, createWebHistory } from "vue-router";
import PlaylistItem from "../components/PlaylistItem.vue";
import CreatePlaylist from "../components/CreatePlaylist.vue";
import MultiStep from "../components/MultiStep.vue";
import MultiStepV2 from "../components/MultiStepV2.vue";
import MultiSelect from "../components/MultiSelect.vue";
import GetStartedView from "../views/GetStartedView.vue";

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
    path: "/create-playlist",
    name: "CreatePlaylist",
    component: CreatePlaylist,
  },
  {
    path: "/multi-step",
    name: "MultiStep",
    component: MultiStep,
  },
  {
    path: "/multi-step-v2",
    name: "MultiStepV2",
    component: MultiStepV2,
  },
  {
    path: "/multi-select",
    name: "MultiSelect",
    component: MultiSelect,
  },

  //TODO: Create the PageNotFound component
  // {
  //   path: '/:catchAll(.*)*',
  //   name: "PageNotFound",
  //   component: PageNotFound,
  //  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
