<script>
import StepOne from "./StepOne.vue";
import StepTwo from "./StepTwo.vue";
import StepThree from "./StepThree.vue";

export default {
  data() {
    return {
      playlist: {
        name: "Playlist Name",
        description: "Description",
        public: false,
        filters: {},
      },
    };
  },
  components: {
    StepOne,
    StepTwo,
    StepThree,
  },
  methods: {
    handleSubmit() {
      console.log("PRE");
      console.log(this.playlist.name);
      console.log(this.playlist.description);
      console.log(this.playlist.public);
      // Update the relevant properties in the playlist object
      this.playlist.name = this.$refs.stepOne.playlistName;
      this.playlist.description = this.$refs.stepOne.playlistDescription;
      this.playlist.public = this.$refs.stepOne.playlistPublic;
      console.log("POST");
      console.log(this.playlist.name);
      console.log(this.playlist.description);
      console.log(this.playlist.public);
    },
  },
};
</script>

<template>
  <FormKit type="form" submit-label="Create Playlist" @submit="handleSubmit">
    <h1>Create a Playlist</h1>
    <FormKit type="multi-step">
      <FormKit type="step" name="information" label="Basic Information">
        <StepOne
          ref="stepOne"
          :playlistName="playlist.name"
          :playlistDescription="playlist.description"
          :playlistPublic="playlist.public"
        />
      </FormKit>

      <FormKit type="step" name="filters" label="Filtering">
        <StepTwo data="value" />
      </FormKit>

      <FormKit type="step" name="validation" label="Validation">
        <StepThree data="value" />
      </FormKit>
    </FormKit>
    <pre wrap>{{ this.playlist }}</pre>
  </FormKit>
</template>
