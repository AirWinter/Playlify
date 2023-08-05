import axios from "axios";
import router from "../router/index";
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
      localStorage.clear();
      sessionStorage.clear();
      router.push("/"); // If there's an error go to home page
    }
  }
};
