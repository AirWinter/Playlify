<script>
import axios from "axios";

export default {
  name: "MultiStepV2",

  data() {
    return {
      playlist: {
        playlistInformation: {
          name: "Name",
          description: "",
          public: false,
        },
        filters: {
          genres: [],
          artists: [],
          created_after_month: "",
          created_before_month: "",
        },
      },
      genres_options: [
        { label: "Any", value: "any" },
        { label: "Pop", value: "pop" },
        { label: "Rock", value: "rock" },
        { label: "Rap", value: "rap" },
        { label: "Indie", value: "indie" },
        { label: "R&B", value: "r-n-b" },
      ],
      artist_options: [{ label: "Any", value: "any" }],
      loading: true,
      loading_songs: true,
      songs: {},
    };
  },
  methods: {
    async getSongsToAdd(param) {
      this.loading_songs = true;
      var songs_to_add_array = null;
      // Get the songs to dd
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getSongsToAdd",

        params: {
          genres:
            param.filters.genres.length > 0
              ? param.filters.genres.reduce((f, s) => `${f};${s}`)
              : [],
          artists:
            param.filters.artists.length > 0
              ? param.filters.artists.reduce((a, b) => `${a};${b}`)
              : [],
          created_after_month: param.filters.created_after_month,
          created_before_month: param.filters.created_before_month,
        },
      }).then((value) => (songs_to_add_array = value.data));
      this.songs = songs_to_add_array;
      this.loading_songs = false;
    },
    removeSong(index) {
      delete this.songs[index];
    },
    async handleNextOne(value) {
      this.playlistInformation = value.playlistInformation;
      // Get all the genres from backend
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getAllMyGenres",
      }).then((value) => (this.genres_options = value.data));
      // Get all the artists from backend
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getAllMyArtists",
      }).then((value) => (this.artist_options = value.data));
    },
    async loadAllTracksFromLibrary() {
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/loadAllTracksFromLibrary",
        withCredentials: true,
      });
      this.loading = false;
    },
    async handleSubmit(param) {
      this.loading = true;
      var songs_to_add_array = Object.keys(this.songs);
      // Create the playlist
      await axios({
        method: "post",
        url: "http://localhost:5000/backend/createPlaylist",
        withCredentials: true,
        data: {
          name: param.playlistInformation.name,
          description: param.playlistInformation.description,
          public: param.playlistInformation.public,
          songs_to_add: songs_to_add_array,
        },
      });
      this.loading = false;
      this.$router.push("/my-playlists");
    },
  },
  created() {
    this.loadAllTracksFromLibrary();
  },
};
</script>

<template>
  <!-- Top Header with logo-->
  <div class="w-full top-0 bg-darkest h-20 py-4 px-10">
    <img src="PoweredBySpotify.png" class="h-10" />
  </div>
  <!-- Main Content-->
  <div class="bg-dark w-full p-4" style="height: 91vh">
    <p class="text-center text-7xl text-lightest font-bold">
      Create a Playlist
    </p>

    <!-- Form Container -->
    <div class="grid place-items-center bg-dark w-full p-4">
      <div class="bg-white opacity-90 px-8 py-2 rounded-xl">
        <!-- Form -->
        <FormKit type="form" :actions="false">
          <div class="text-black h-full text-center" style="width: 60vh">
            <div
              role="status"
              class="absolute -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2"
              v-if="loading"
            >
              <div
                :aria-hidden="loading"
                class="w-20 h-20 spinner-border text-green"
              ></div>
            </div>
            <FormKit
              type="multi-step"
              tab-style="progress"
              #default="{ value }"
              :value="playlist"
              :disabled="loading"
            >
              <!-- <template #tabs=""> -->
              <FormKit
                type="step"
                name="playlistInformation"
                label="Basic Information"
              >
                <FormKit
                  type="text"
                  name="name"
                  id="name"
                  label="Playlist Name"
                  placeholder="Name"
                  validation="required|name"
                />
                <FormKit
                  type="textarea"
                  name="description"
                  id="description"
                  label="Description (optional)"
                  placeholder="Description"
                  :help="
                    value.playlistInformation?.description !== undefined
                      ? `${value.playlistInformation.description.length} / 300`
                      : `0 / 300`
                  "
                  validation="length:0,300"
                  validation-visibility="live"
                  :validation-messages="{
                    length: 'Description cannot be more than 300 characters.',
                  }"
                />
                <FormKit
                  type="checkbox"
                  label="Public"
                  help="Do you want your playlist to be public?"
                  name="public"
                />
                <!-- Go Back To My Playlists -->
                <template #stepPrevious="">
                  <a href="/my-playlists">
                    <button
                      type="button"
                      class="btn btn-sm py-2 px-3 rounded-full bg-white border-2 border-slate-700 hover:border-black text-black hover:text-black font-bold"
                    >
                      Cancel
                    </button>
                  </a>
                </template>
                <!-- Next Button Page 1-->
                <template #stepNext="{ handlers, node }">
                  <div class="relative bottom-0 right-0">
                    <button
                      type="button"
                      class="bg-lime hover:bg-green text-white font-bold py-2 px-3 rounded-full btn btn-sm"
                      @click="
                        handleNextOne(value),
                          handlers.incrementStep(1, node.context)()
                      "
                      data-next="true"
                    >
                      Next
                    </button>
                  </div>
                </template>
              </FormKit>

              <FormKit type="step" name="filters" label="Filters">
                <FormKit
                  type="taglist"
                  name="genres"
                  label="Genre of your playlist (Optional)"
                  help="Add all the genres of songs you want to be added to your playlist"
                  :options="genres_options"
                />
                <FormKit
                  type="taglist"
                  name="artists"
                  label="Artists to add to your playlist (Optional)"
                  help="Add all songs from the artists specified"
                  :options="artist_options"
                />
                <FormKit
                  type="month"
                  help="Add songs created after this date"
                  label="Songs Created After (Optional)"
                  name="created_after_month"
                  :validation="`$date_before:{{value.filters.created_before_month}}`"
                  validation-visibility="live"
                  :validation-messages="{
                    date_before: 'Date range invalid',
                  }"
                />
                <FormKit
                  type="month"
                  help="Add songs created before this date"
                  label="Songs Created Before (Optional)"
                  name="created_before_month"
                  :validation="`$date_after:{{value.filters.created_after_month}}`"
                  validation-visibility="live"
                  :validation-messages="{
                    date_after: 'Date range invalid',
                  }"
                />
                <!-- Go back to basic Information -->
                <template #stepPrevious="{ handlers, node }">
                  <button
                    type="button"
                    class="bg-lime hover:bg-green text-white font-bold py-2 px-4 rounded-full btn-sm"
                    @click="handlers.incrementStep(-1, node.context)()"
                  >
                    Previous
                  </button>
                </template>
                <!-- Go to validation step-->
                <template #stepNext="{ handlers, node }">
                  <button
                    type="button"
                    v-if="
                      value.filters.created_before_month >
                        value.filters.created_after_month ||
                      value.filters.created_before_month == '' ||
                      value.filters.created_after_month == ''
                    "
                    class="bg-lime hover:bg-green text-white font-bold py-2 px-4 rounded-full btn-sm"
                    @click="
                      getSongsToAdd(value),
                        handlers.incrementStep(1, node.context)()
                    "
                    data-next="true"
                  >
                    Validate
                  </button>
                </template>
              </FormKit>
              <FormKit type="step" name="validation" label="Validation">
                <div class="overflow-y-auto h-96">
                  <!-- Create table containing existing playlists-->
                  <p class="text-center text-xl text-darkest font-bold">
                    Suggested Songs ({{ Object.keys(this.songs).length }})
                  </p>
                  <div class="py-2"></div>
                  <table class="table w-full" v-if="!this.loading_songs">
                    <!-- Table Header-->
                    <thead class="sticky top-0 bg-white">
                      <tr>
                        <!-- Table Header Cells: Playlist Name, Date-Created, Public (true/false)-->
                        <th scope="col">Song Name</th>
                        <th scope="col">Artist(s)</th>
                        <th scope="col">Remove</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(song, index) in songs" :key="index">
                        <td class="py-3">{{ song.song_name }}</td>
                        <td class="py-3">{{ song.artists }}</td>
                        <td>
                          <button
                            class="bg-white hover:bg-gray-400 px-3"
                            type="button"
                            @click="removeSong(index)"
                          >
                            <img src="trash-can.png" class="h-6 w-6" />
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="py-1"></div>
                <!-- Go back to filters -->
                <template #stepPrevious="{ handlers, node }">
                  <button
                    type="button"
                    class="bg-lime hover:bg-green text-white font-bold py-2 px-4 rounded-full btn-sm"
                    @click="handlers.incrementStep(-1, node.context)()"
                  >
                    Go Back
                  </button>
                </template>
                <!-- Submit Button -->
                <template #stepNext>
                  <button
                    type="submit"
                    class="bg-lime h-9 w-24 text-white font-bold py-2 px-4 rounded-full btn-sm"
                    :class="
                      this.loading_songs ? 'hover:bg-lime' : 'hover:bg-green'
                    "
                    @click="handleSubmit(value)"
                    data-next="true"
                    :disabled="this.loading_songs"
                  >
                    <p v-if="!this.loading_songs">Submit</p>
                    <p v-else class="spinner-border spinner-border-sm"></p>
                  </button>
                </template>
              </FormKit>
            </FormKit>
          </div>
        </FormKit>
      </div>
    </div>
  </div>
</template>
