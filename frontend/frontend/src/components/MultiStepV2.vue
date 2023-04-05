<script>
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
          created_after_month: "2023-02",
          created_before_month: "2023-04",
        },
      },
    };
  },
  methods: {
    handleNextOne(value) {
      console.log("HERE");
      console.log(value);
      console.log(value.playlistInformation.name);
      this.playlistInformation = value.playlistInformation;
    },
    handleSubmit(value) {
      console.log("HEREeeeeeee");
      console.log(value.filters.created_after_month);
    },
  },
};
</script>

<template>
  <h1>Create a Playlist</h1>
  <!-- we'll get rid of the default form actions -->
  <FormKit type="form" :actions="false">
    <FormKit
      type="multi-step"
      tab-style="progress"
      #default="{ value }"
      :value="playlist"
    >
      <FormKit type="step" name="playlistInformation" label="Basic Information">
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
          :options="[
            { label: 'Pop', value: 'pop' },
            { label: 'Rock', value: 'rock' },
            { label: 'Rap', value: 'rap' },
            { label: 'Indie', value: 'indie' },
            { label: 'R&B', value: 'r-n-b' },
            { label: 'Any', value: 'any' },
          ]"
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
</template>
