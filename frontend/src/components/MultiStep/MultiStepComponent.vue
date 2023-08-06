<template>
  <!-- Form Container -->
  <div class="grid place-items-center bg-dark w-full py-4 max-sm:text-xs">
    <div class="bg-white opacity-90 px-4 py-2 rounded-xl">
      <!-- Form -->
      <FormKit type="form" :actions="false">
        <!-- Conditional CSS for the width of the form -->
        <div id="myelement" class="text-black h-full relative">
          <!-- Loading Sign, Positioning within relative div-->
          <div
            role="status"
            class="absolute -translate-x-1/2 -translate-y-1/3 top-1/3 left-1/2"
            v-if="store.state.loading_modal"
          >
            <div
              :aria-hidden="store.state.loading_modal"
              class="w-24 h-24 max-sm:w-20 max-sm:h-20 spinner-border text-green"
            ></div>
          </div>
          <FormKit
            type="multi-step"
            tab-style="progress"
            #default="{ value }"
            :value="playlist"
            :disabled="store.state.loading_modal"
            :before-step-change="
              ({ currentStep, targetStep, delta }: Step) => {
                // Prevent skipping steps
                if (Math.abs(delta) > 1) {
                  return false;
                }
                if (targetStep.stepName == 'Validation') {
                  playlist.filters.created_after_month =
                    currentStep.value.created_after_month;
                  playlist.filters.created_before_month =
                    currentStep.value.created_before_month;
                  getSongsToAdd(playlist.filters);
                  store.commit('clearRecommendedSongs');
                }
                return true;
              }
            "
          >
            <!-- Step One: Basic Information-->
            <StepOne :value="playlist" />
            <!-- Step Two: Defining filters-->
            <StepTwo
              :genres_options="store.getters.getGenreOptions"
              :artist_options="store.getters.getArtistOptions"
              :filters="playlist.filters"
            />
            <!-- Step Three: Validation -->
            <StepThree
              :loading_songs="store.getters.getLoadingSongs"
              :songs="store.getters.getSongs"
              :recommended_songs="store.getters.getRecommendedSongs"
              @remove-song="(index) => removeSong(index)"
              @remove-recommended-song="(index) => removeRecommendedSong(index)"
              @get-recommendations="getRecommendations(playlist.filters)"
              @submit="createPlaylist(value)"
            />
          </FormKit>
        </div>
      </FormKit>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount } from "vue";
import { useStore } from "vuex";
import StepOne from "./StepOne.vue";
import StepTwo from "./StepTwo.vue";
import StepThree from "./StepThree.vue";
import { createPlaylist } from "@/services/playlists";
import {
  getAllTracksFromLibrary,
  getRecommendations,
  removeRecommendedSong,
  removeSong,
  getSongsToAdd,
} from "@/services/songs";
import type {
  // eslint-disable-next-line no-unused-vars
  Step,
  Playlist,
} from "./types";

const store = useStore();

let playlist: Playlist = {
  playlistInformation: {
    name: "",
    description: "",
    display: false,
  },
  filters: {
    genres: [],
    artists: [],
    created_after_month: "",
    created_before_month: "",
  },
};

onBeforeMount(() => {
  if (store.getters.getLoadingModal) {
    getAllTracksFromLibrary();
  }
});
</script>

<style>
.formkit-outer {
  padding: 0px;
}
</style>
