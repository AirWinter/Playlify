<template>
  <!-- Top Header with logo -->
  <TopHeader />
  <!-- Log Out Button -->
  <div class="absolute top-3 right-12 max-sm:top-2 max-sm:right-4">
    <a :href="this.urlBase + 'logout'"
      ><button
        type="button"
        class="btn bg-snow h-10 w-28 max-sm:h-8 max-sm:w-20 max-sm:text-sm font-semibold rounded-full text-black hover:underline"
        @click="handleLogout()"
      >
        Log Out
      </button>
    </a>
  </div>
  <!-- Main Content-->
  <div class="bg-dark min-h-screen w-full">
    <!-- Table Container -->
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <div class="max-sm:w-full w-1/2 flex justify-start">
            <button
              class="btn bg-lime font-semibold text-white rounded-full hover:bg-green w-44 max-sm:w-40 max-sm:text-sm"
              @click="handleShow()"
            >
              <p v-if="this.show">Hide My Playlists</p>
              <p v-else>Show My Playlists</p>
            </button>
            <a href="/create-playlist"
              ><button
                type="button"
                class="btn bg-lime font-semibold rounded-full text-white hover:bg-green ml-2 max-sm:text-sm"
              >
                Create Playlist
              </button></a
            >
          </div>
          <br />
          <!-- Create table containing existing playlists-->
          <table
            v-if="this.show"
            class="table text-white text-center max-sm:text-xs"
          >
            <!-- Table Header-->
            <thead>
              <tr>
                <!-- Table Header Cells: Playlist Name, Date-Created, Public (true/false)-->
                <th class="max-sm:w-28 w-44" scope="col">Playlist Name</th>
                <th scope="col">Description</th>
                <th class="w-10" scope="col">Public?</th>
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
import TopHeader from "../components/TopHeader.vue";
const getUtils = () => import("../utils.js");

export default {
  name: "PlaylistItem",
  components: { TopHeader },
  data() {
    return {
      show: false,
      playlists: [],
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
      sessionStorage.clear();
    },
    handleShow() {
      this.getPlaylists();
      this.show = !this.show;
    },
  },
  created() {
    this.handleShow();
  },
};
</script>
