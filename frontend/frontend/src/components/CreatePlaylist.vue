<template>
  <h1>Create a new Playlist</h1>
  <FormKit
    type="form"
    #default="{ value }"
    submit-label="Create Playlist"
    @submit="handleSubmit"
    :value="playlist"
  >
    <FormKit
      type="text"
      name="name"
      id="name"
      label="Playlist Name"
      placeholder="My Playlist"
      validation="required|name"
    />
    <FormKit
      type="textarea"
      name="description"
      id="description"
      label="Description"
      placeholder="(Optional)"
      :help="`${value.description.length} / 300`"
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
    <pre wrap>{{ value }}</pre>
  </FormKit>
</template>

<script>
import "@formkit/themes/genesis";

export default {
  name: "CreatePlaylist",
  data() {
    return {
      playlist: {
        name: "Playlist Name",
        description: "",
        public: false,
      },
    };
  },
};
</script>
