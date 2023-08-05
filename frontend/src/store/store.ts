// store/index.js
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  state: {
    loading_songs: true,
    loading_modal: true,
  },
  mutations: {
    setLoadingSongs(state, newValue) {
      state.loading_songs = newValue;
    },
    setLoadingModal(state, newValue) {
      state.loading_modal = newValue;
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
  },
  plugins: [createPersistedState()],
});

export default store;
