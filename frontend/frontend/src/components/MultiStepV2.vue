<script>
import axios from "axios";
export default {
  name: "MultiStepV2",
  data() {
    return {
      playlist: {
        playlistInformation: {
          name: "Playlist Name",
          description: "",
          public: false,
        },
        filters: {
          genre: "any",
          created_after_month: "-------",
          created_before_month: "-------",
        },
      },
      genre_options: [
        { label: "Any", value: "any" },
        { label: "Pop", value: "pop" },
        { label: "Rock", value: "rock" },
        { label: "Rap", value: "rap" },
        { label: "Indie", value: "indie" },
        { label: "R&B", value: "r-n-b" },
      ],
      loading: false,
    };
  },
  methods: {
    async handleNextOne(value) {
      //   console.log("HERE");
      //   console.log(value);
      //   console.log(value.playlistInformation.name);
      this.playlistInformation = value.playlistInformation;
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getAllMyGenres",
      }).then((value) => console.log(value)((this.genre_options = value.data)));
    },
    async handleSubmit(param) {
      this.loading = true;
      console.log(param.playlistInformation);
      console.log(param.filters);
      //   const token =
      //     "AQCwQsBThaF00FfAXH1p9P04Myn_8UyoLhk8TOrgX4T6bosRPj4SjY0P3Ypbn3PlEGWO4JRmoitqefPvLBj5DHrTXAV_mgsUhY_kZN1TaAzRHgxWYtfKR4qpL2SndI6Bgz0";

      await axios({
        method: "get",
        url: "http://localhost:5000/backend/loadAllTracksFromLibrary",
        withCredentials: true,
      }).then((value) => console.log(value.data));

      var songs_to_add_array = null;
      await axios({
        method: "get",
        url: "http://localhost:5000/backend/getSongsToAdd",

        params: {
          genre: param.filters.genre,
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
            type="select"
            label="Genre of your playlist"
            name="genre"
            :options="genre_options"
          />

          <FormKit
            type="month"
            help="Add songs created after this date"
            label="Songs Created After"
            name="created_after_month"
          />
          <FormKit
            type="month"
            help="Add songs created before this date"
            label="Songs Created Before"
            name="created_before_month"
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
            <FormKit type="submit" @click="handleSubmit(value)" />
          </template>
        </FormKit>
        <pre wrap>{{ value }}</pre>
      </FormKit>
      <pre wrap>{{ playlist }}</pre>
    </FormKit>
  </div>
</template>
