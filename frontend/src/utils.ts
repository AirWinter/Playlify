import axios from "axios";

const urlBase = process.env.VUE_APP_URL_BASE;

async function getAccessToken() {
  // If token is expired hit "/refresh endpoint"
  if (isExpired() || localStorage.getItem("access_token") === "undefined") {
    // If there is no refresh token available
    if (
      localStorage.getItem("refresh_token") === null ||
      localStorage.getItem("refresh_token") === "undefined"
    ) {
      localStorage.clear();
      return;
    }
    const refresh_token = localStorage.getItem("refresh_token");
    await axios({
      method: "get",
      url: `${urlBase}/refresh`,
      headers: {
        RefreshToken: refresh_token,
      },
    }).then((res) => {
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      localStorage.setItem("expires_at", res.data.expires_at);
    });
    return localStorage.getItem("access_token");
  } else {
    return localStorage.getItem("access_token");
  }
}

const isExpired = () => {
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

export const accessToken = getAccessToken().then((value) => value);
