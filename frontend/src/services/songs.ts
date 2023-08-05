import axios from "axios";
import router from "../router/index";
const getUtils = () => import("../utils");
import store from "@/store/store";

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
