import axios from "axios";

const getAccessToken = () => {
  console.log("Getting access token");
  // If token is expired hit "/refresh endpoint"
  if (isExpired() || localStorage.getItem("access_token") === "undefined") {
    console.log("Use refresh token");
    // If there is no refresh token available
    if (
      localStorage.getItem("refresh_token") === null ||
      localStorage.getItem("refresh_token") === "undefined"
    ) {
      localStorage.clear();
      return;
    }
    const refresh_token = localStorage.getItem("refresh_token");
    axios({
      method: "get",
      url: `${process.env.URL_BASE}/refresh`,
      headers: {
        refresh_token: refresh_token,
      },
    }).then((res) => {
      console.log(res.data);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      localStorage.setItem("expires_at", res.data.expires_at);
    });
  } else {
    return localStorage.getItem("access_token");
  }
};

const isExpired = () => {
  console.log(Date.now() / 1000);
  console.log(localStorage.getItem("expires_at"));
  return Date.now() / 1000 > localStorage.getItem("expires_at") - 60;
};

export const accessToken = getAccessToken();
