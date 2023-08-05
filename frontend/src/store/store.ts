// store/index.js
import { createStore } from "vuex";

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
  },
});

export default store;
