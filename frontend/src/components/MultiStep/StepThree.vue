<template>
  <FormKit type="step" name="validation" label="Validation">
    <div class="overflow-y-auto overflow-x-contain h-96 w-full text-center">
      <!-- Loading Sign-->
      <div
        role="status"
        class="relative -translate-x-1/2 -translate-y-1/2 top-1/4 left-1/2"
        v-if="props.loading_songs"
      >
        <div
          :aria-hidden="props.loading_songs"
          class="w-20 h-20 spinner-border text-green"
        ></div>
      </div>
      <div v-else>
        <!-- Sum of total songs that will be added -->
        <div>
          <p class="text-center text-2xl text-darkest font-bold max-sm:text-sm">
            Total Suggested Songs:
            {{
              Object.keys(props.songs).length +
              Object.keys(props.recommended_songs).length
            }}
          </p>
        </div>
        <!-- Create table containing songs from user's library -->
        <TableDropdown
          title="Songs From Your Library"
          :songs="props.songs"
          :get_more="false"
          @remove-song="(index) => emit('remove-song', index)"
        />
        <!-- Create table containing recommended songs -->
        <TableDropdown
          title="Recommended Songs"
          :songs="props.recommended_songs"
          :get_more="true"
          @remove-song="(index) => emit('remove-recommended-song', index)"
          @get-more="emit('get-recommendations')"
        />
      </div>
    </div>
    <div class="py-1"></div>
    <!-- Go back to filters -->
    <template #stepPrevious="{ handlers, node }">
      <button
        type="button"
        class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs text-white font-bold rounded-full"
        :class="loading_songs ? 'hover:bg-lime' : 'hover:bg-green'"
        @click="handlers.incrementStep(-1, node.context)()"
        :disabled="loading_songs"
      >
        Go Back
      </button>
    </template>
    <!-- Submit Button -->
    <template #stepNext>
      <button
        type="button"
        class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs text-white font-bold rounded-full"
        :class="loading_songs ? 'hover:bg-lime' : 'hover:bg-green'"
        @click="emit('submit')"
        data-next="true"
        :disabled="loading_songs"
      >
        Submit
      </button>
    </template>
  </FormKit>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import { Song } from "./types";
import TableDropdown from "./TableDropdown.vue";

const props = defineProps<{
  loading_songs: boolean;
  songs: Record<string, Song>;
  recommended_songs: Record<string, Song>;
}>();

const emit = defineEmits<{
  // eslint-disable-next-line
  (e: "remove-song", index: string): void;
  // eslint-disable-next-line
  (e: "remove-recommended-song", index: string): void;
  // eslint-disable-next-line
  (e: "get-recommendations"): void;
  // eslint-disable-next-line
  (e: "submit"): void;
}>();
</script>
