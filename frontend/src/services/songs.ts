import axios from "axios";
import router from "../router/index";
const getUtils = () => import("../utils");
import store from "@/store/store";
import type { Filters } from "@/components/MultiStep/types";

const urlBase: string = process.env.VUE_APP_URL_BASE ?? "";

export const getAllTracksFromLibrary = async () => {
  if (
    sessionStorage.getItem("all_songs") == null ||
    sessionStorage.getItem("all_artists") == null ||
    sessionStorage.getItem("all_genres") == null ||
    sessionStorage.getItem("all_songs") == "undefined" ||
    sessionStorage.getItem("all_artists") == "undefined" ||
    sessionStorage.getItem("all_genres") == "undefined"
  ) {
    const token_string = await (await getUtils()).getAccessToken();
    try {
      const response = await axios.get(`${urlBase}/tracks/get-all`, {
        headers: {
          Token: token_string,
        },
      });
      sessionStorage.setItem(
        "all_songs",
        JSON.stringify(response.data.all_songs)
      );
      sessionStorage.setItem(
        "all_artists",
        JSON.stringify(response.data.all_artists)
      );
      sessionStorage.setItem(
        "all_genres",
        JSON.stringify(response.data.all_genres)
      );
    } catch (error) {
      console.log(error);
      localStorage.clear();
      sessionStorage.clear();
      router.push("/"); // If there's an error go to home page
    }
  }
  store.commit("setLoadingModal", false);
};

export const getSongsToAdd = async (param: Filters) => {
  store.commit("setLoadingSongs", true);
  const all_my_songs = sessionStorage.getItem("all_songs");
  const all_my_artists = sessionStorage.getItem("all_artists");

  try {
    // Use POST to avoid 414
    const response = await axios.post(`${urlBase}/tracks/get-tracks-to-add`, {
      genres:
        param.genres.length > 0
          ? param.genres.reduce((f: string, s: string) => `${f};${s}`)
          : "",
      artists:
        param.artists.length > 0
          ? param.artists.reduce((a: string, b: string) => `${a};${b}`)
          : "",
      created_after_month: param.created_after_month,
      created_before_month: param.created_before_month,
      all_my_songs: all_my_songs,
      all_my_artists: all_my_artists,
    });

    store.commit("setSongs", response.data);
  } catch (error) {
    console.log(error);
    localStorage.clear();
    sessionStorage.clear();
    router.push("/"); // If there's an error go to home page
  }
  await getRecommendations(param);
  store.commit("setLoadingSongs", false);
};

export const getRecommendations = async (param: Filters) => {
  const songs_to_add_array = store.getters.getSongs;
  // Get recommended songs: order of seeds genres > tracks > artists
  const token_string = await (await getUtils()).getAccessToken();
  const genre_seed_string =
    param.genres.length > 0
      ? param.genres
          .slice(0, Math.min(param.genres.length, 5))
          .reduce((f, s) => `${f};${s}`)
      : "";
  const artist_seed_string =
    param.artists.length > 0
      ? param.artists
          .slice(0, Math.min(param.artists.length, 5))
          .reduce((a, b) => `${a};${b}`)
      : "";
  let track_seed_string: string = "";
  Object.keys(songs_to_add_array).forEach(function (key, index) {
    if (index < 5) {
      if (index > 0) {
        track_seed_string += ";";
      }
      track_seed_string += key;
    }
  });
  try {
    const response = await axios.get(`${urlBase}/tracks/get-recommendations`, {
      headers: {
        Token: token_string,
      },
      params: {
        genre_seeds: genre_seed_string,
        artist_seeds: artist_seed_string,
        track_seeds: track_seed_string,
      },
    });
    store.commit("appendRecommendedSongs", response.data);
  } catch (error) {
    console.log(error);
  }
};

export const removeSong = (index: string) => {
  delete store.state.songs[index];
};

export const removeRecommendedSong = (index: string) => {
  delete store.state.recommended_songs[index];
};
