<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <p>Playlist Item View</p>
        <hr />
        <br />
        <button type="button" class="btn btn-success">
          Create new Playlist
        </button>
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
  data() {
    return {
      playlists: [],
    };
  },
  methods: {
    getPlaylists() {
      const path = "http://localhost:5000/backend/getPlaylists";
      const token =
        "AQCwQsBThaF00FfAXH1p9P04Myn_8UyoLhk8TOrgX4T6bosRPj4SjY0P3Ypbn3PlEGWO4JRmoitqefPvLBj5DHrTXAV_mgsUhY_kZN1TaAzRHgxWYtfKR4qpL2SndI6Bgz0";
      const config = {
        headers: {
          refresh_token: token,
        },
      };
      axios
        .get(path, config)
        .then((res) => {
          this.playlists = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getPlaylists();
  },
};
</script>
