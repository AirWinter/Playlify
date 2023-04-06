<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <p>Playlist Item View</p>
        <hr />
        <br />
        <a href="/multi-step-v2"
          ><button type="button" class="btn btn-success">
            Create new Playlist
          </button></a
        >
        <br /><br />
        <!-- Create table containing existing playlists-->
        <table class="table table-hover">
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
            <tr v-for="(playlist, index) in playlists" :key="index">
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
</template>

<script>
import axios from "axios";

export default {
  name: "PlaylistItem",
  data() {
    return {
      playlists: [],
    };
  },
  methods: {
    async getPlaylists() {
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getPlaylists",
        withCredentials: true,
      }).then((value) => (this.playlists = value.data));
    },
  },
  created() {
    this.getPlaylists();
  },
};
</script>
