<template>
  <!-- Top Header with logo-->
  <div class="w-full top-0 bg-darkest h-16 py-3 px-10">
    <img src="PoweredBySpotify.png" class="h-8" />
    <!-- Log Out Button-->
    <div class="absolute top-3 right-12">
      <a :href="this.urlBase + 'logout'"
        ><button
          type="button"
          class="btn bg-snow h-10 w-28 font-semibold rounded-full text-black hover:underline"
          @click="handleLogout()"
        >
          Log Out
        </button>
      </a>
    </div>
  </div>
  <!-- Main Content-->
  <div class="bg-dark min-h-screen w-full">
    <!-- Table Container -->
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <div class="w-1/2 flex justify-start">
            <button
              class="btn bg-lime font-semibold text-white rounded-full hover:bg-green w-44"
              @click="handleShow()"
            >
              <p v-if="this.show">Hide My Playlists</p>
              <p v-else>Show My Playlists</p>
            </button>
            <a href="/create-playlist"
              ><button
                type="button"
                class="btn bg-lime font-semibold rounded-full text-white hover:bg-green ml-2"
              >
                Create Playlist
              </button></a
            >
          </div>
          <br />
          <!-- Create table containing existing playlists-->
          <table v-if="this.show" class="table text-white">
            <!-- Table Header-->
            <thead>
              <tr>
                <!-- Table Header Cells: Playlist Name, Date-Created, Public (true/false)-->
                <th scope="col">Playlist Name</th>
                <th scope="col">Description</th>
                <th scope="col">Public?</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(playlist, index) in playlists"
                :key="index"
                class="opacity-90 hover:opacity-100"
              >
                <td>{{ playlist.name }}</td>
                <td>{{ playlist.description }}</td>
                <td>
                  <span v-if="playlist.public">Yes</span>
                  <span v-else>No</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// {
//   accessToken;
// }
// () => import("../utils");
const getUtils = () => import("../utils.js");

export default {
  name: "PlaylistItem",
  data() {
    return {
      show: false,
      playlists: [],
      // urlBase: process.env.URL_BASE,
      urlBase: "https://airwinter.pythonanywhere.com/",
      // urlBase: "http://localhost:5000/",
    };
  },
  methods: {
    async getPlaylists() {
      await axios({
        method: "get",
        url: `${this.urlBase}backend/getPlaylists`,
        headers: {
          Token: (await getUtils()).accessToken,
        },
      })
        .then((value) => (this.playlists = value.data))
        .catch(() => this.$router.push("/")); // If user is not logged in then redirect to home page
    },
    handleLogout() {
      localStorage.clear();
    },
    handleShow() {
      this.getPlaylists();
      this.show = !this.show;
    },
  },
};
</script>
