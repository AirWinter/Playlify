<template>
  <!-- Set the background colour everywhere -->
  <div class="bg-dark min-h-screen">
    <!-- Top Header with Log Out Button -->
    <TopHeader />
    <LogOutButton />
    <!-- Main Content -->
    <div class="w-full h-full relative overflow-y-scroll">
      <div class="px-2 py-3">
        <!-- Recently Played Text -->
        <div class="flex items-center justify-between">
          <h1 class="pl-2 py-2 text-4xl text-white font-bold tracking-wide">
            Your Playlists
          </h1>
        </div>
        <!-- Cards -->
        <div class="w-full flex flex-wrap">
          <!-- Hardcoded Create Playlist -->
          <div class="p-2 w-48 h-64 max-sm:w-44">
            <a href="/create-playlist" style="text-decoration: none">
              <div
                class="bg-card_bg opacity-90 hover:opacity-100 w-full h-full p-3 rounded-lg shadow-md"
              >
                <img src="PlusSign.png" class="h-36 w-36 shadow rounded" />

                <h1
                  class="text-xl mt-3 font-semibold text-white text-center tracking-wide"
                >
                  Create Playlist
                </h1>
              </div>
            </a>
          </div>
          <!-- All of their playlists -->
          <div
            v-for="playlist in this.playlists"
            :key="playlist.key"
            class="p-2 w-48 h-64 max-sm:w-44"
          >
            <!-- Card -->
            <a
              :href="playlist.link"
              target="_blank"
              style="text-decoration: none"
            >
              <div
                class="bg-card_bg opacity-90 hover:opacity-100 w-full h-full p-3 rounded-lg shadow-md"
              >
                <!-- Playlist Cover Photo -->
                <img
                  :src="playlist.image"
                  class="h-36 w-36 object-cover shadow mb-2 rounded"
                />
                <!-- Playlist Title -->
                <h1
                  class="text-base font-semibold text-white tracking-wide truncate"
                >
                  {{ playlist.name }}
                </h1>
                <!-- Playlist Description -->
                <h2
                  v-if="playlist.description != ''"
                  class="text-sm text-lightest tracking-wide line-clamp-2 mb-1"
                >
                  {{ playlist.description }}
                </h2>
                <h2
                  v-else
                  class="text-sm text-lightest tracking-wide line-clamp-2 mb-1"
                >
                  {{ "By " + playlist.creator }}
                </h2>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TopHeader from "../components/TopHeader.vue";
import LogOutButton from "../components/LogOutButton.vue";
import axios from "axios";
const getUtils = () => import("../utils.js");

export default {
  name: "PlaylistsView",
  components: {
    TopHeader,
    LogOutButton,
  },
  data() {
    return {
      urlBase: "https://airwinter.pythonanywhere.com",
      //   urlBase: "http://localhost:5000",
      playlists: [
        {
          image:
            "https://mosaic.scdn.co/640/ab67616d0000b2730ae4f4d42e4a09f3a29f64adab67616d0000b2735c8cfe4b2c4aa89c9c92108eab67616d0000b2736abad6915a2216dc18e7e3a7ab67616d0000b273f48a2a4e66094853072c3b79",
          name: "EDM",
          description: "",
          link: "https://open.spotify.com/playlist/0JRzdWJ6LeZwcwuGa9luxC",
        },
        {
          image:
            "https://mosaic.scdn.co/640/ab67616d0000b2736b62c541105dbc157b9ab7bfab67616d0000b273726d48d93d02e1271774f023ab67616d0000b2739b19c107109de740bad72df5ab67616d0000b273dbb3dd82da45b7d7f31b1b42",
          name: "Eminem Songs",
          description: "All my Eminem Songs",
          link: "https://open.spotify.com/playlist/2XmySKuyO52KAwoJrvz7Ox",
        },
        {
          image:
            "https://mosaic.scdn.co/640/ab67616d0000b273029c7ad2659fcc983ba27b51ab67616d0000b2738dc0d801766a5aa6a33cbe37ab67616d0000b273935d8d5369bc55e74a39303eab67616d0000b273cd945b4e3de57edd28481a3f",
          name: "Drake Songs",
          description: "All my drake songs",
          link: "https://open.spotify.com/playlist/0KPKReEpzxRorFmQ6WHnXP",
        },
      ],
    };
  },
  methods: {
    async getPlaylists() {
      await axios({
        method: "get",
        url: `${this.urlBase}/backend/getPlaylists`,
        headers: {
          Token: (await getUtils()).accessToken,
        },
      })
        .then((value) => (this.playlists = value.data))
        .catch((error) => {
          console.log(error);
          this.$router.push("/"); // If user is not logged in then redirect to home page
        });
    },
  },
  created() {
    this.getPlaylists();
  },
};
</script>
