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
  show_empty_library_modal: boolean;
  show_error_modal: boolean;
}

const store = createStore<State>({
  state: {
    loading_songs: true,
    loading_modal: true,
    songs: {},
    recommended_songs: {},
    artist_options: [],
    genre_options: [],
    show_empty_library_modal: false,
    show_error_modal: false,
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
    setShowEmptyLibraryModal(state, newValue) {
      state.show_empty_library_modal = newValue;
    },
    setShowErrorModal(state, newValue) {
      state.show_error_modal = newValue;
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
    getShowEmptyLibraryModal(state) {
      return state.show_empty_library_modal;
    },
    getShowErrorModal(state) {
      return state.show_error_modal;
    },
  },
  plugins: [createPersistedState()],
});

export default store;
