<template>
  <FormKit type="step" name="validation" label="Validation">
    <div class="overflow-y-auto overflow-x-contain h-96 text-center">
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
        <div class="">
          <p class="text-center text-2xl text-darkest font-bold max-sm:text-sm">
            Total Suggested Songs:
            {{
              Object.keys(props.songs).length +
              Object.keys(props.recommended_songs).length
            }}
          </p>
        </div>
        <!-- Create table containing songs from user's library -->
        <div class="bg-white drop-shadow-lg rounded bg-white m-2 max-sm:m-1">
          <div class="flex items-center justify-start">
            <!-- Button for opening/closing suggested songs table -->
            <button
              class="bg-transparent inline-flex opacity-80 hover:opacity-100"
              type="button"
              @click="handleShowSongs()"
            >
              <img
                v-if="!show_songs"
                src="arrow_right.png"
                class="h-12 w-12 max-sm:h-8 max-sm:w-8 bg-transparent"
              />
              <img
                v-else
                src="arrow_down.png"
                class="h-12 w-12 max-sm:h-8 max-sm:w-8 bg-transparent"
              />
              <span
                class="text-center text-lg text-darkest font-semibold max-sm:text-xs py-2.5 max-sm:py-2"
                >Songs From Your Library ({{
                  Object.keys(props.songs).length
                }})</span
              >
            </button>
          </div>
          <div class="container text-center" v-if="show_songs">
            <table
              class="table table-fixed text-sm max-sm:text-xs"
              v-if="!loading_songs"
            >
              <!-- Table Header-->
              <thead class="sticky top-0 bg-white">
                <tr>
                  <th class="w-16 max-sm:w-6" scope="col">Name</th>
                  <th class="w-16 max-sm:w-6" scope="col">Artist(s)</th>
                  <th class="w-10 max-sm:w-4" scope="col">Remove</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(song, index) in props.songs" :key="index">
                  <td class="py-3">
                    <a :href="song.song_url" target="_blank">{{
                      song.song_name
                    }}</a>
                  </td>
                  <td class="py-3">
                    <a
                      v-for="(artist, index) in song.artists"
                      :key="index"
                      :href="artist.external_url"
                      target="_blank"
                      >{{
                        artist.name +
                        (index < Object.keys(song.artists).length - 1
                          ? ", "
                          : "")
                      }}</a
                    >
                  </td>
                  <td>
                    <button
                      class="bg-transparent px-1"
                      type="button"
                      @click="$emit('remove-song', index)"
                    >
                      <img
                        src="trash-can.png"
                        class="h-6 w-6 opacity-80 hover:opacity-100"
                      />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- Create table containing recommended songs -->
        <div class="bg-white rounded drop-shadow-lg m-2">
          <div class="flex items-center justify-start">
            <!-- Button for opening/closing recommended songs table -->
            <button
              class="bg-transparent inline-flex opacity-80 hover:opacity-100"
              type="button"
              @click="handleShowRecommended()"
            >
              <img
                v-if="!show_recommended"
                src="arrow_right.png"
                class="h-12 w-12 max-sm:h-8 max-sm:w-8 bg-transparent"
              />
              <img
                v-else
                src="arrow_down.png"
                class="h-12 w-12 max-sm:h-8 max-sm:w-8 bg-transparent"
              />
              <span
                class="text-center text-lg text-darkest font-semibold max-sm:text-xs py-2.5 max-sm:py-2"
                >Recommended Songs ({{
                  Object.keys(props.recommended_songs).length
                }})</span
              >
            </button>
          </div>
          <div class="container text-center" v-if="show_recommended">
            <table
              class="table table-fixed text-sm max-sm:text-xs"
              v-if="!loading_songs"
            >
              <!-- Table Header-->
              <thead class="sticky top-0 bg-white">
                <tr>
                  <th class="w-16 max-sm:w-6" scope="col">Name</th>
                  <th class="w-16 max-sm:w-6" scope="col">Artist(s)</th>
                  <th class="w-10 max-sm:w-4" scope="col">Remove</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(song, index) in props.recommended_songs"
                  :key="index"
                >
                  <td class="py-3">
                    <a :href="song.song_url" target="_blank">{{
                      song.song_name
                    }}</a>
                  </td>
                  <td class="py-3">
                    <a
                      v-for="(artist, index) in song.artists"
                      :key="index"
                      :href="artist.external_url"
                      target="_blank"
                      >{{
                        artist.name +
                        (index < Object.keys(song.artists).length - 1
                          ? ", "
                          : "")
                      }}</a
                    >
                  </td>
                  <td>
                    <button
                      class="bg-transparent px-1"
                      type="button"
                      @click="$emit('remove-recommended-song', index)"
                    >
                      <img
                        src="trash-can.png"
                        class="h-6 w-6 opacity-80 hover:opacity-100"
                      />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <button
              type="button"
              class="bg-white border-2 border-black text-sm h-8 w-20 max-sm:h-8 max-sm:w-20 max-sm:text-xs rounded-full text-black opacity-90 hover:opacity-100 font-bold mb-1"
              @click="$emit('get-recommendations')"
            >
              Get More
            </button>
          </div>
        </div>
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
        @click="$emit('submit')"
        data-next="true"
        :disabled="loading_songs"
      >
        Submit
      </button>
    </template>
  </FormKit>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, Ref } from "vue";
import { Song } from "./types";

const props = defineProps<{
  loading_songs: boolean;
  songs: Record<string, Song>;
  recommended_songs: Record<string, Song>;
}>();

defineEmits([
  "remove-song",
  "remove-recommended-song",
  "get-recommendations",
  "submit",
]);

let show_songs: Ref<boolean> = ref(false);
let show_recommended: Ref<boolean> = ref(false);

const handleShowSongs = () => {
  show_songs.value = !show_songs.value;
};

const handleShowRecommended = () => {
  show_recommended.value = !show_recommended.value;
};
</script>
