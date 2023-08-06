// store/index.js
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import type {
  Artist_Options,
  Genre_Options,
  Song,
} from "@/components/MultiStep/types";

export interface State {
  loading_songs: boolean;
  loading_modal: boolean;
  songs: Record<string, Song>;
  recommended_songs: Record<string, Song>;
  artist_options: Array<Artist_Options>;
  genre_options: Array<Genre_Options>;
  TTL: number;
}

const store = createStore<State>({
  state: {
    loading_songs: true,
    loading_modal: true,
    songs: {},
    recommended_songs: {},
    artist_options: [],
    genre_options: [],
    TTL: 0,
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
    setArtistOptions(state, newValue) {
      state.artist_options = newValue;
    },
    setGenreOptions(state, newValue) {
      state.genre_options = newValue;
    },
    resetTTL(state) {
      state.TTL = Date.now();
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
    getArtistOptions(state) {
      return state.artist_options;
    },
    getGenreOptions(state) {
      return state.genre_options;
    },
    getTTL(state) {
      return state.TTL;
    },
  },
  plugins: [createPersistedState()],
});

export default store;