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
    };
  },
  methods: {
    async handleNextOne(value) {
      this.playlistInformation = value.playlistInformation;
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getAllMyGenres",
      }).then((value) => (this.genres_options = value.data));
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
      console.log(param);
      this.loading = true;
      var songs_to_add_array = null;
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

      console.log("SONGS TO ADD");
      console.log(songs_to_add_array);

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
  <h1>Create a Playlist</h1>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <!-- we'll get rid of the default form actions -->
    <FormKit type="form" :actions="false">
      <FormKit
        type="multi-step"
        tab-style="progress"
        #default="{ value }"
        :value="playlist"
      >
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
          <template #stepNext="{ handlers, node }">
            <!-- incrementStep returns a callable function -->
            <FormKit
              type="button"
              @click="
                handleNextOne(value), handlers.incrementStep(1, node.context)()
              "
              label="Next Step"
              data-next="true"
            />
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
          <template #stepPrevious="{ handlers, node }">
            <!-- incrementStep returns a callable function -->
            <FormKit
              type="button"
              @click="handlers.incrementStep(-1, node.context)()"
              label="Custom Previous"
            />
          </template>
          <template #stepNext>
            <FormKit
              v-if="
                value.filters.created_before_month >
                  value.filters.created_after_month ||
                value.filters.created_before_month == '' ||
                value.filters.created_after_month == ''
              "
              type="submit"
              @click="handleSubmit(value)"
            />
            <a v-else>Invalid Date Range!!! </a>
          </template>
        </FormKit>
      </FormKit>
    </FormKit>
  </div>
</template>
