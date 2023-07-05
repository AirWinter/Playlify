<template>
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
        props.value.playlistInformation?.description !== undefined
          ? `${props.value.playlistInformation.description.length} / 300`
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
      label="Display on profile"
      help="Do you want your playlist to be shown on your spotify profile?"
      name="display"
    />
    <!-- Go Back To My Playlists -->
    <template #stepPrevious="">
      <a href="/my-playlists">
        <button
          type="button"
          class="btn btn-sm text-base h-10 w-20 max-sm:h-8 max-sm:w-16 max-sm:text-xs rounded-full bg-white border-2 border-slate-700 hover:border-black text-black hover:text-black font-bold"
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
          class="btn btn-sm text-base bg-lime hover:bg-green text-white font-bold h-10 w-20 max-sm:h-8 max-sm:w-16 max-sm:text-xs rounded-full"
          @click="handlers.incrementStep(1, node.context)()"
          data-next="true"
        >
          Next
        </button>
      </div>
    </template>
  </FormKit>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

const props = defineProps<{
  value: any;
}>();
</script>
