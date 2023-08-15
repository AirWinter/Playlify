import axios from "axios";
import router from "../router/index";
import { Playlist } from "@/components/MultiStep/types";
import store from "@/store/store";
const getUtils = () => import("../utils");

const urlBase: string = process.env.VUE_APP_URL_BASE ?? "";

export const getPlaylists = async () => {
  const token_string: string = await (await getUtils()).getAccessToken(); // lazy import and then await async function
  if (token_string === "") {
    router.push("/");
  } else {
    try {
      const response = await axios.get(`${urlBase}/playlist/get-playlists`, {
        headers: {
          Token: token_string,
        },
      });
      return response.data;
    } catch (error) {
      console.log(error);
      store.commit("setShowErrorModal", true);
    }
  }
};

export const createPlaylist = async (param: Playlist) => {
  store.commit("setLoadingModal", true);
  const token_string: string = await (await getUtils()).getAccessToken();
  const songs_string =
    Object.keys(store.getters.getSongs).length > 0
      ? Object.keys(store.getters.getSongs) + ","
      : "";
  const songs_to_add_array =
    songs_string + Object.keys(store.getters.getRecommendedSongs);
  // Create the playlist
  try {
    await axios.post(
      `${urlBase}/playlist/create-playlist`,
      {
        name: param.playlistInformation.name,
        description: param.playlistInformation.description,
        display: param.playlistInformation.display,
        songs_to_add: songs_to_add_array,
      },
      {
        headers: {
          Token: token_string,
        },
      }
    );
  } catch (error) {
    console.log(error);
    store.commit("setShowErrorModal", true);
  }

  router.push("/my-playlists");
  store.commit("setLoadingModal", false);
};
