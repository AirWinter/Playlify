import axios from "axios";

const urlBase = process.env.VUE_APP_URL_BASE;

export async function getAccessToken(): Promise<string> {
  // If token is expired hit "/refresh endpoint"
  if (isExpired() || localStorage.getItem("access_token") === "undefined") {
    // If there is no refresh token available
    if (
      localStorage.getItem("refresh_token") === null ||
      localStorage.getItem("refresh_token") === "undefined"
    ) {
      localStorage.clear();
      return "";
    }
    const refresh_token = localStorage.getItem("refresh_token");
    const config = {
      headers: {
        RefreshToken: refresh_token,
      },
    };
    const response = await axios.get(
      `${urlBase}/authentication/refresh`,
      config
    );
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("refresh_token", response.data.refresh_token);
    localStorage.setItem("expires_at", response.data.expires_at);

    // await axios({
    //   method: "get",
    //   url: `${urlBase}/authentication/refresh`,
    //   headers: {
    //     RefreshToken: refresh_token,
    //   },
    // }).then((res) => {
    //   localStorage.setItem("access_token", res.data.access_token);
    //   localStorage.setItem("refresh_token", res.data.refresh_token);
    //   localStorage.setItem("expires_at", res.data.expires_at);
    // });
    return localStorage.getItem("access_token") ?? "";
  } else {
    return localStorage.getItem("access_token") ?? "";
  }
}

export const isExpired = () => {
  if (
    localStorage.getItem("expires_at") === null ||
    localStorage.getItem("expires_at") === "undefined"
  ) {
    return true;
  }
  // console.log(Date.now() / 1000);
  // console.log(localStorage.getItem("expires_at"));
  return Date.now() / 1000 > Number(localStorage.getItem("expires_at")) - 60;
};
