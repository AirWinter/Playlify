import { Component } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import type { Route } from "./types";

function lazyLoadView(view: string): Component {
  return () => import(`../views/${view}.vue`);
}

function dynamicPropsFn(route: Route) {
  const { access_token, refresh_token, expires_at } = route.query;
  if (
    access_token == null ||
    refresh_token == null ||
    expires_at == null ||
    access_token === "undefined" ||
    refresh_token === "undefined"
  ) {
    return;
  }
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("refresh_token", refresh_token);
  localStorage.setItem("expires_at", expires_at.toString());

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
    name: "PlaylistsView",
    component: lazyLoadView("PlaylistsView"),
    props: dynamicPropsFn,
  },
  {
    path: "/create-playlist",
    name: "CreatePlaylistView",
    component: lazyLoadView("CreatePlaylistView"),
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
