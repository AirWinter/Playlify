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
              ({ currentStep, targetStep, delta }) => {
                // Prevent skipping steps
                if (Math.abs(delta) > 1) {
                  return false;
                }
                if (targetStep.stepName == 'Filters') {
                  handleNextOne();
                }
                if (targetStep.stepName == 'Validation') {
                  this.playlist.filters.created_after_month =
                    currentStep.value.created_after_month;
                  this.playlist.filters.created_before_month =
                    currentStep.value.created_before_month;
                  getSongsToAdd(this.playlist.filters);
                }
                return true;
              }
            "
          >
            <FormKit
              type="step"
              name="playlistInformation"
              label="Basic Information"
            >
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
            <!-- Step Two: Defining filters-->
            <FormKit type="step" name="filters" label="Filters">
              <div>
                <p class="p-1 font-bold text-black text-sm max-sm:text-xs">
                  Genres to add to your playlist (Optional)
                </p>
                <Multiselect
                  mode="tags"
                  v-model="this.playlist.filters.genres"
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
                  v-model="this.playlist.filters.artists"
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
            <FormKit type="step" name="validation" label="Validation">
              <div class="overflow-y-auto overflow-x-contain h-96 text-center">
                <!-- Loading Sign-->
                <div
                  role="status"
                  class="relative -translate-x-1/2 -translate-y-1/2 top-1/4 left-1/2"
                  v-if="loading_songs"
                >
                  <div
                    :aria-hidden="loading_songs"
                    class="w-20 h-20 spinner-border text-green"
                  ></div>
                </div>
                <div v-else>
                  <!-- Sum of total songs that will be added -->
                  <div class="">
                    <p
                      class="text-center text-2xl text-darkest font-bold max-sm:text-sm"
                    >
                      Total Suggested Songs:
                      {{
                        Object.keys(this.songs).length +
                        Object.keys(this.recommended_songs).length
                      }}
                    </p>
                  </div>
                  <!-- Create table containing songs from user's library -->
                  <div
                    class="bg-white drop-shadow-lg rounded bg-white m-2 max-sm:m-1"
                  >
                    <div class="flex items-center justify-start">
                      <!-- Button for opening/closing suggested songs table -->
                      <button
                        class="bg-transparent inline-flex opacity-80 hover:opacity-100"
                        type="button"
                        @click="handleShowSongs()"
                      >
                        <img
                          v-if="!this.show_songs"
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
                            Object.keys(this.songs).length
                          }})</span
                        >
                      </button>
                    </div>
                    <div class="container text-center" v-if="this.show_songs">
                      <table
                        class="table table-fixed text-sm max-sm:text-xs"
                        v-if="!this.loading_songs"
                      >
                        <!-- Table Header-->
                        <thead class="sticky top-0 bg-white">
                          <tr>
                            <th class="w-16 max-sm:w-6" scope="col">Name</th>
                            <th class="w-16 max-sm:w-6" scope="col">
                              Artist(s)
                            </th>
                            <th class="w-10 max-sm:w-4" scope="col">Remove</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(song, index) in songs" :key="index">
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
                                @click="removeSong(index)"
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
                          v-if="!this.show_recommended"
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
                            Object.keys(this.recommended_songs).length
                          }})</span
                        >
                      </button>
                    </div>
                    <div
                      class="container text-center"
                      v-if="this.show_recommended"
                    >
                      <table
                        class="table table-fixed text-sm max-sm:text-xs"
                        v-if="!this.loading_songs"
                      >
                        <!-- Table Header-->
                        <thead class="sticky top-0 bg-white">
                          <tr>
                            <th class="w-16 max-sm:w-6" scope="col">Name</th>
                            <th class="w-16 max-sm:w-6" scope="col">
                              Artist(s)
                            </th>
                            <th class="w-10 max-sm:w-4" scope="col">Remove</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(song, index) in recommended_songs"
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
                                @click="removeRecommendedSong(index)"
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
                        @click="getRecommendations(this.playlist.filters)"
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
                  :class="
                    this.loading_songs ? 'hover:bg-lime' : 'hover:bg-green'
                  "
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
                  :class="
                    this.loading_songs ? 'hover:bg-lime' : 'hover:bg-green'
                  "
                  @click="handleSubmit(value)"
                  data-next="true"
                  :disabled="this.loading_songs"
                >
                  Submit
                </button>
              </template>
            </FormKit>
          </FormKit>
        </div>
      </FormKit>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const getUtils = () => import("../utils.ts");
import Multiselect from "@vueform/multiselect";

export default {
  name: "MultiStepComponent",
  components: {
    Multiselect,
  },
  data() {
    return {
      urlBase: process.env.VUE_APP_URL_BASE,
      playlist: {
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
      },
      genres_options: [{ label: "Any", options: [] }],
      artist_options: [{ label: "Any", value: "any" }],
      loading: true,
      loading_songs: true,
      songs: {},
      recommended_songs: {},
      show_songs: false,
      show_recommended: false,
    };
  },
  methods: {
    handleShowSongs() {
      this.show_songs = !this.show_songs;
    },
    handleShowRecommended() {
      this.show_recommended = !this.show_recommended;
    },
    async getSongsToAdd(param) {
      this.loading_songs = true;
      var songs_to_add_array = null;
      const all_my_songs = sessionStorage.getItem("all_songs");
      const all_my_artists = sessionStorage.getItem("all_artists");

      // Use POST to avoid 414
      await axios({
        method: "post",
        url: `${this.urlBase}/backend/getSongsToAdd`,
        data: {
          genres:
            param.genres.length > 0
              ? param.genres.reduce((f, s) => `${f};${s}`)
              : "",
          artists:
            param.artists.length > 0
              ? param.artists.reduce((a, b) => `${a};${b}`)
              : "",
          created_after_month: param.created_after_month,
          created_before_month: param.created_before_month,
          all_my_songs: all_my_songs,
          all_my_artists: all_my_artists,
        },
      })
        .then((value) => (songs_to_add_array = value.data))
        .catch((error) => {
          console.log(error);
          localStorage.clear();
          sessionStorage.clear();
          this.$router.push("/"); // If there's an error go to home page
        });
      this.songs = songs_to_add_array;
      this.recommended_songs = {};
      await this.getRecommendations(param);
      this.loading_songs = false;
    },
    async getRecommendations(param) {
      var songs_to_add_array = this.songs;
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
      var track_seed_string = "";
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
        url: `${this.urlBase}/backend/getRecommendations`,
        headers: {
          Token: token_string,
        },
        params: {
          genre_seeds: genre_seed_string,
          artist_seeds: artist_seed_string,
          track_seeds: track_seed_string,
        },
      }).then((res) => {
        this.recommended_songs = Object.assign(
          this.recommended_songs,
          res.data
        );
      });
    },
    removeSong(index) {
      delete this.songs[index];
    },
    removeRecommendedSong(index) {
      delete this.recommended_songs[index];
    },
    async handleNextOne() {
      // Get all genres from session storage
      if (
        sessionStorage.getItem("all_genres") != null &&
        sessionStorage.getItem("all_genres") != "undefined"
      ) {
        this.genres_options = JSON.parse(sessionStorage.getItem("all_genres"));
      }
      // Get all artists from session storage
      if (
        sessionStorage.getItem("all_artists") != null &&
        sessionStorage.getItem("all_artists") != "undefined"
      ) {
        var all_artists = JSON.parse(sessionStorage.getItem("all_artists"));
        Object.keys(all_artists).forEach((key) => {
          all_artists[key] = all_artists[key]["name"];
        });
        this.artist_options = all_artists;
      }
    },
    async getAllTracksFromLibrary() {
      if (
        sessionStorage.getItem("all_songs") != null &&
        sessionStorage.getItem("all_artists") != null &&
        sessionStorage.getItem("all_genres") != null &&
        sessionStorage.getItem("all_songs") != "undefined" &&
        sessionStorage.getItem("all_artists") != "undefined" &&
        sessionStorage.getItem("all_genres") != "undefined"
      ) {
        this.loading = false;
      } else {
        const token_string = await (await getUtils()).accessToken;
        await axios({
          method: "get",
          url: `${this.urlBase}/backend/getAllTracksFromLibrary`,
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
            this.$router.push("/"); // If there's an error go to home page
          });
        this.loading = false;
      }
    },
    async handleSubmit(param) {
      this.loading = true;
      const token_string = await (await getUtils()).accessToken;
      var songs_to_add_array =
        Object.keys(this.songs) + "," + Object.keys(this.recommended_songs);
      // Create the playlist
      await axios({
        method: "post",
        url: `${this.urlBase}/backend/createPlaylist`,
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
        this.$router.push("/"); // If there's an error go to home page
      });
      this.$router.push("/my-playlists");
      this.loading = false;
    },
  },
  created() {
    this.getAllTracksFromLibrary();
  },
};
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
