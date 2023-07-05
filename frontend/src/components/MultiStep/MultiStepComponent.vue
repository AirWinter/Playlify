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
            v-if="loading"
          >
            <div
              :aria-hidden="loading"
              class="w-24 h-24 max-sm:w-20 max-sm:h-20 spinner-border text-green"
            ></div>
          </div>
          <FormKit
            type="multi-step"
            tab-style="progress"
            #default="{ value }"
            :value="playlist"
            :disabled="loading"
            :before-step-change="
              ({ currentStep, targetStep, delta }: Step) => {
                // Prevent skipping steps
                if (Math.abs(delta) > 1) {
                  return false;
                }
                if (targetStep.stepName == 'Filters') {
                  handleNextOne();
                }
                if (targetStep.stepName == 'Validation') {
                  playlist.filters.created_after_month =
                    currentStep.value.created_after_month;
                  playlist.filters.created_before_month =
                    currentStep.value.created_before_month;
                  getSongsToAdd(playlist.filters);
                }
                return true;
              }
            "
          >
            <!-- Step One: Basic Information-->
            <StepOne :value="playlist" />
            <!-- Step Two: Defining filters-->
            <FormKit type="step" name="filters" label="Filters">
              <div>
                <p class="p-1 font-bold text-black text-sm max-sm:text-xs">
                  Genres to add to your playlist (Optional)
                </p>
                <Multiselect
                  mode="tags"
                  v-model="playlist.filters.genres"
                  :groups="true"
                  :options="genres_options"
                  :close-on-select="true"
                  class="multiselect-green"
                  :classes="{
                    container:
                      'relative mx-auto w-full flex items-center justify-end box-border cursor-pointer border-[1px] border-outer rounded bg-white text-base leading-snug',
                    tag: 'bg-lime text-white text-xs font-semibold py-0.5 pl-2 rounded-full mr-1 mb-1 flex items-center whitespace-nowrap rtl:pl-0 rtl:pr-0 rtl:mr-0 rtl:ml-0',
                    groupLabel:
                      'flex text-m box-border items-center justify-start text-white text-left py-1 px-3 font-bold bg-lime cursor-default leading-normal',
                  }"
                  name="GenresMultiselect"
                  placeholder="Genres"
                  :searchable="true"
                />
                <p class="p-0.5 font text-slate-700 text-xs max-sm:text-2xs">
                  Add songs that match any of these genres
                </p>
              </div>
              <div>
                <p class="p-1 font-bold text-black text-sm max-sm:text-xs">
                  Artists for your playlist (Optional)
                </p>
                <Multiselect
                  mode="tags"
                  v-model="playlist.filters.artists"
                  :options="artist_options"
                  class="multiselect-green"
                  :classes="{
                    container:
                      'relative mx-auto w-full flex items-center justify-end box-border cursor-pointer border-[1px] border-outer rounded bg-white text-base leading-snug',
                    tag: 'bg-lime text-white text-xs font-semibold py-0.5 pl-2 rounded-full mr-1 mb-1 flex items-center whitespace-nowrap rtl:pl-0 rtl:pr-2 rtl:mr-0 rtl:ml-1',
                  }"
                  name="ArtistsMultiselect"
                  placeholder="Artists"
                  :searchable="true"
                />
                <p class="p-0.5 font text-slate-700 text-xs max-sm:text-2xs">
                  Add songs from any of these artists
                </p>
              </div>
              <div class="p-1"></div>
              <FormKit
                type="month"
                help="Add songs created after this date"
                label="Songs Created After (Optional)"
                name="created_after_month"
                :validation="`$date_before:{{value.filters.created_before_month}}`"
                validation-visibility="live"
                :validation-messages="{
                  date_before: 'Date range invalid',
                }"
              />
              <FormKit
                type="month"
                help="Add songs created before this date"
                label="Songs Created Before (Optional)"
                name="created_before_month"
                :validation="`$date_after:{{value.filters.created_after_month}}`"
                validation-visibility="live"
                :validation-messages="{
                  date_after: 'Date range invalid',
                }"
              />
              <!-- Go back to basic Information -->
              <template #stepPrevious="{ handlers, node }">
                <button
                  type="button"
                  class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs hover:bg-green text-white font-bold rounded-full"
                  @click="handlers.incrementStep(-1, node.context)()"
                >
                  Previous
                </button>
              </template>
              <!-- Go to validation step-->
              <template #stepNext="{ handlers, node }">
                <button
                  type="button"
                  v-if="
                    value.filters.created_before_month >
                      value.filters.created_after_month ||
                    value.filters.created_before_month == '' ||
                    value.filters.created_after_month == ''
                  "
                  class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs hover:bg-green text-white font-bold rounded-full"
                  @click="handlers.incrementStep(1, node.context)()"
                  data-next="true"
                >
                  Validate
                </button>
              </template>
            </FormKit>
            <!-- Step Three: Validation -->
            <StepThree
              :loading_songs="loading_songs"
              :songs="songs"
              :recommended_songs="recommended_songs"
              @remove-song="(index) => removeSong(index)"
              @remove-recommended-song="(index) => removeRecommendedSong(index)"
              @get-recommendations="getRecommendations(playlist.filters)"
              @submit="handleSubmit(value)"
            />
          </FormKit>
        </div>
      </FormKit>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { ref, Ref, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
const getUtils = () => import("../../utils");
import Multiselect from "@vueform/multiselect";
import StepOne from "./StepOne.vue";
import StepThree from "./StepThree.vue";
import type {
  // eslint-disable-next-line no-unused-vars
  Step,
  Genre_Options,
  Artist_Options,
  Song,
  Playlist,
  Filters,
} from "./types";

const router = useRouter();

const urlBase: string = process.env.VUE_APP_URL_BASE;
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

let genres_options: Array<Genre_Options> = [{ label: "Any", options: [] }];
let artist_options: Array<Artist_Options> = [{ label: "Any", value: "any" }];
let loading: Ref<boolean> = ref(true);
let loading_songs: Ref<boolean> = ref(true);
let songs: Ref<Record<string, Song>> = ref({});
let recommended_songs: Ref<Record<string, Song>> = ref({});

const getSongsToAdd = async (param: Filters) => {
  console.log(param);
  loading_songs.value = true;
  const all_my_songs = sessionStorage.getItem("all_songs");
  const all_my_artists = sessionStorage.getItem("all_artists");

  // Use POST to avoid 414
  await axios({
    method: "post",
    url: `${urlBase}/backend/getSongsToAdd`,
    data: {
      genres:
        param.genres.length > 0
          ? param.genres.reduce((f: string, s: string) => `${f};${s}`)
          : "",
      artists:
        param.artists.length > 0
          ? param.artists.reduce((a: string, b: string) => `${a};${b}`)
          : "",
      created_after_month: param.created_after_month,
      created_before_month: param.created_before_month,
      all_my_songs: all_my_songs,
      all_my_artists: all_my_artists,
    },
  })
    .then((response) => {
      songs.value = response.data;
    })
    .catch((error) => {
      console.log(error);
      localStorage.clear();
      sessionStorage.clear();
      router.push("/"); // If there's an error go to home page
    });
  recommended_songs.value = {};
  await getRecommendations(param);
  loading_songs.value = false;
};

const getRecommendations = async (param: Filters) => {
  var songs_to_add_array = songs.value;
  // Get recommended songs: order of seeds genres > tracks > artists
  const token_string = await (await getUtils()).accessToken;
  const genre_seed_string =
    param.genres.length > 0
      ? param.genres
          .slice(0, Math.min(param.genres.length, 5))
          .reduce((f, s) => `${f};${s}`)
      : "";
  const artist_seed_string =
    param.artists.length > 0
      ? param.artists
          .slice(0, Math.min(param.artists.length, 5))
          .reduce((a, b) => `${a};${b}`)
      : "";
  var track_seed_string: string = "";
  Object.keys(songs_to_add_array).forEach(function (key, index) {
    if (index < 5) {
      if (index > 0) {
        track_seed_string += ";";
      }
      track_seed_string += key;
    }
  });
  // const track_seed_string = JSON.stringify(this.songs);
  await axios({
    method: "get",
    url: `${urlBase}/backend/getRecommendations`,
    headers: {
      Token: token_string,
    },
    params: {
      genre_seeds: genre_seed_string,
      artist_seeds: artist_seed_string,
      track_seeds: track_seed_string,
    },
  }).then((res) => {
    recommended_songs.value = Object.assign(recommended_songs.value, res.data);
  });
};

const removeSong = (index: string) => {
  delete songs.value[index];
};

const removeRecommendedSong = (index: any) => {
  delete recommended_songs.value[index];
};

const handleNextOne = async () => {
  // Get all genres from session storage
  if (
    sessionStorage.getItem("all_genres") != null &&
    sessionStorage.getItem("all_genres") != "undefined"
  ) {
    genres_options = JSON.parse(sessionStorage.getItem("all_genres") ?? "");
  }
  // Get all artists from session storage
  if (
    sessionStorage.getItem("all_artists") != null &&
    sessionStorage.getItem("all_artists") != "undefined"
  ) {
    var all_artists = JSON.parse(sessionStorage.getItem("all_artists") ?? "");
    Object.keys(all_artists).forEach((key) => {
      all_artists[key] = all_artists[key]["name"];
    });
    artist_options = all_artists;
  }
};

const getAllTracksFromLibrary = async () => {
  if (
    sessionStorage.getItem("all_songs") != null &&
    sessionStorage.getItem("all_artists") != null &&
    sessionStorage.getItem("all_genres") != null &&
    sessionStorage.getItem("all_songs") != "undefined" &&
    sessionStorage.getItem("all_artists") != "undefined" &&
    sessionStorage.getItem("all_genres") != "undefined"
  ) {
    loading.value = false;
  } else {
    const token_string = await (await getUtils()).accessToken;
    await axios({
      method: "get",
      url: `${urlBase}/backend/getAllTracksFromLibrary`,
      headers: {
        Token: token_string,
      },
    })
      .then((response) => {
        sessionStorage.setItem(
          "all_songs",
          JSON.stringify(response.data.all_songs)
        );
        sessionStorage.setItem(
          "all_artists",
          JSON.stringify(response.data.all_artists)
        );
        sessionStorage.setItem(
          "all_genres",
          JSON.stringify(response.data.all_genres)
        );
      })
      .catch((error) => {
        console.log(error);
        localStorage.clear();
        sessionStorage.clear();
        router.push("/"); // If there's an error go to home page
      });
    loading.value = false;
  }
};

const handleSubmit = async (param: Playlist) => {
  loading.value = true;
  const token_string: string = await (await getUtils()).accessToken;
  var songs_to_add_array =
    Object.keys(songs.value) + "," + Object.keys(recommended_songs.value);
  // Create the playlist
  await axios({
    method: "post",
    url: `${urlBase}/backend/createPlaylist`,
    headers: {
      Token: token_string,
    },
    data: {
      name: param.playlistInformation.name,
      description: param.playlistInformation.description,
      display: param.playlistInformation.display,
      songs_to_add: songs_to_add_array,
    },
  }).catch((error) => {
    console.log(error);
    localStorage.clear();
    sessionStorage.clear();
    router.push("/"); // If there's an error go to home page
  });
  router.push("/my-playlists");
  loading.value = false;
};

onBeforeMount(() => {
  getAllTracksFromLibrary();
});
</script>

<style>
@import "@vueform/multiselect/themes/default.css";

#myelement {
  width: 300px;
}
@media only screen and (min-width: 800px) {
  #myelement {
    width: 490px;
  }
}
</style>
