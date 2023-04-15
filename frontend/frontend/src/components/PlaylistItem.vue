<template>
  <!-- Top Header with logo-->
  <div class="w-full top-0 bg-darkest h-20 py-4 px-10">
    <img src="PoweredBySpotify.png" class="h-10" />
    <!-- Log Out Button-->
    <div class="absolute top-5 right-12">
      <a :href="this.baseUrl + 'logout'"
        ><button
          type="button"
          class="btn bg-snow h-10 w-28 font-semibold rounded-full text-black hover:underline"
        >
          Log Out
        </button>
      </a>
    </div>
  </div>
  <!-- Main Content-->
  <div class="bg-dark">
    <!-- Table Container -->
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <a href="/multi-step-v2"
            ><button
              type="button"
              class="btn bg-lime font-semibold rounded-full text-white hover:bg-green"
            >
              Create Playlist
            </button></a
          >
          <br /><br />
          <!-- Create table containing existing playlists-->
          <table class="table text-white">
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

export default {
  name: "PlaylistItem",
  data() {
    return {
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
        withCredentials: true,
      })
        .then((value) => (this.playlists = value.data))
        .catch(() => this.$router.push("/")); // If user is not logged in then redirect to home page
    },
  },
  created() {
    this.getPlaylists();
  },
};
</script>
