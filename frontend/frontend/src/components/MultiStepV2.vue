<script>
export default {
  name: "MultiStepV2",
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
  methods: {
    handleSubmit() {},
  },
};
</script>

<template>
  <h1>Create a Playlist</h1>
  <!-- we'll get rid of the default form actions -->
  <FormKit type="form" :actions="false">
    <FormKit type="multi-step" tab-style="progress">
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
          :model-value="this.public"
        />
        <template #stepNext="{ handlers, node }">
          <!-- incrementStep returns a callable function -->
          <FormKit
            type="button"
            @click="handlers.incrementStep(1, node.context)()"
            label="Next Step"
            data-next="true"
          />
        </template>
      </FormKit>

      <FormKit type="step" name="description">
        <FormKit type="text" label="Name" prefix-icon="avatarMan" />
        <template #stepPrevious="{ handlers, node }">
          <!-- incrementStep returns a callable function -->
          <FormKit
            type="button"
            @click="handlers.incrementStep(-1, node.context)()"
            label="Custom Previous"
          />
        </template>
        <template #stepNext="{ handlers, node }">
          <!-- incrementStep returns a callable function -->
          <FormKit
            type="button"
            @click="handlers.incrementStep(1, node.context)()"
            label="Custom Next"
            data-next="true"
          />
        </template>
      </FormKit>

      <FormKit type="step" name="references">
        <FormKit
          type="textarea"
          label="Please supply contact information for 2 references"
          validation="required"
        />

        <template #stepPrevious="{ handlers, node }">
          <!-- incrementStep returns a callable function -->
          <FormKit
            type="button"
            @click="handlers.incrementStep(-1, node.context)()"
            label="Custom Previous"
          />
        </template>
        <!-- 
      normally there is no stepNext section rendered
      on the last step of a multi-step. But we can
      supply our own.
       -->
        <template #stepNext>
          <FormKit type="submit" />
        </template>
      </FormKit>
    </FormKit>
  </FormKit>
</template>
