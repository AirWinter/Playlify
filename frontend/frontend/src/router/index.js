import { createRouter, createWebHistory } from "vue-router";

function lazyLoadComponent(component) {
  return () => import(`../components/${component}.vue`);
}

function lazyLoadView(view) {
  return () => import(`../views/${view}.vue`);
}

function dynamicPropsFn(route) {
  const { access_token, refresh_token, expires_at } = route.query;
  if (
    access_token == null ||
    refresh_token == null ||
    expires_at == null ||
    access_token === "undefined" ||
    refresh_token === "undefined" ||
    expires_at === "underfined"
  ) {
    return;
  }
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("refresh_token", refresh_token);
  localStorage.setItem("expires_at", expires_at);

  return {
    access_token: access_token,
    refresh_token: refresh_token,
    expires_at: expires_at,
  };
}

const routes = [
  {
    path: "/",
    name: "GetStartedView",
    component: lazyLoadView("GetStartedView"),
  },
  {
    path: "/my-playlists",
    name: "PlaylistItem",
    component: lazyLoadComponent("PlaylistItem"),
    props: dynamicPropsFn,
  },
  {
    path: "/create-playlist",
    name: "MultiStepV2",
    component: lazyLoadComponent("MultiStepV2"),
  },
  {
    path: "/:catchAll(.*)*",
    name: "PageNotFoundView",
    component: lazyLoadView("PageNotFoundView"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
