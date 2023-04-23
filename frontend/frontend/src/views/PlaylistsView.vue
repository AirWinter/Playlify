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
                  v-if="playlist.image != ''"
                  :src="playlist.image"
                  class="h-36 w-36 object-cover shadow mb-2 rounded"
                />
                <img
                  v-else
                  src="PlaceholderIcon.png"
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
      playlists: [],
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
