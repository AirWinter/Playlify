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
            <StepTwo
              :genres_options="genres_options"
              :artist_options="artist_options"
              :filters="playlist.filters"
            />
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
import StepOne from "./StepOne.vue";
import StepTwo from "./StepTwo.vue";
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
let artist_options: Ref<Array<Artist_Options>> = ref([]);
let loading: Ref<boolean> = ref(true);
let loading_songs: Ref<boolean> = ref(true);
let songs: Ref<Record<string, Song>> = ref({});
let recommended_songs: Ref<Record<string, Song>> = ref({});

const getSongsToAdd = async (param: Filters) => {
  loading_songs.value = true;
  const all_my_songs = sessionStorage.getItem("all_songs");
  const all_my_artists = sessionStorage.getItem("all_artists");

  // Use POST to avoid 414
  await axios({
    method: "post",
    url: `${urlBase}/tracks/get-tracks-to-add`,
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
    url: `${urlBase}/tracks/get-recommendations`,
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

const removeRecommendedSong = (index: string) => {
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
      artist_options.value.push({
        value: key,
        label: all_artists[key]["name"],
      });
    });
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
      url: `${urlBase}/tracks/get-all`,
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
  var songs_string =
    Object.keys(songs.value).length > 0 ? Object.keys(songs.value) + "," : "";
  var songs_to_add_array = songs_string + Object.keys(recommended_songs.value);
  // Create the playlist
  await axios({
    method: "post",
    url: `${urlBase}/playlist/create-playlist`,
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
.formkit-outer {
  padding: 0px;
}
</style>
