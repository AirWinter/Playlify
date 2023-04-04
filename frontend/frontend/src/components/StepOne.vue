<script>
export default {
  props: {
    playlistName: {
      type: String,
      required: true,
    },
    playlistDescription: {
      type: String,
      required: false,
    },
    playlistPublic: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      // Use the name prop as the initial value of the component's "name" data property
      name: this.playlistName,
      description: this.playlistDescription,
      public: this.playlistPublic,
    };
  },
  methods: {
    handleSubmit(values) {
      console.log("VALUES");
      console.log(values);
      (this.name = values.name),
        (this.description = values.description),
        (this.public = values.public);
    },
  },
};
</script>

<template>
  <FormKit type="step" name="playlistInformation" @submit="handleSubmit">
    <FormKit
      type="text"
      name="name"
      id="name"
      label="Playlist Name"
      placeholder="Name"
      validation="required|name"
      :model-value="this.name"
    />
    <FormKit
      type="textarea"
      name="description"
      id="description"
      label="Description (optional)"
      placeholder="Description"
      validation="length:0,300"
      validation-visibility="live"
      :validation-messages="{
        length: 'Description cannot be more than 300 characters.',
      }"
      :model-value="this.description"
    />
    <FormKit
      type="checkbox"
      label="Public"
      help="Do you want your playlist to be public?"
      name="public"
      :model-value="this.public"
    />
    <pre wrap>{{ this.playlistName }}</pre>
  </FormKit>
</template>
