// store/index.js
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import type { Song } from "@/components/MultiStep/types";

export interface State {
  loading_songs: boolean;
  loading_modal: boolean;
  songs: Record<string, Song>;
  recommended_songs: Record<string, Song>;
}

const store = createStore<State>({
  state: {
    loading_songs: true,
    loading_modal: true,
    songs: {},
    recommended_songs: {},
  },
  mutations: {
    setLoadingSongs(state, newValue) {
      state.loading_songs = newValue;
    },
    setLoadingModal(state, newValue) {
      state.loading_modal = newValue;
    },
    setSongs(state, newValue) {
      state.songs = newValue;
    },
    appendRecommendedSongs(state, songs_to_add) {
      state.recommended_songs = Object.assign(
        state.recommended_songs,
        songs_to_add
      );
    },
    clearRecommendedSongs(state) {
      state.recommended_songs = {};
    },
  },
  actions: {
    // Your action functions go here
  },
  getters: {
    // Your getter functions go here
    getLoadingSongs(state) {
      return state.loading_songs;
    },
    getLoadingModal(state) {
      return state.loading_modal;
    },
    getSongs(state) {
      return state.songs;
    },
    getRecommendedSongs(state) {
      return state.recommended_songs;
    },
  },
  plugins: [createPersistedState()],
});

export default store;
