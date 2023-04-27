<template>
  <!-- Form Container -->
  <div class="grid place-items-center bg-dark w-full py-4 max-sm:text-xs">
    <div class="bg-white opacity-90 px-4 py-2 rounded-xl">
      <!-- Form -->
      <FormKit type="form" :actions="false">
        <!-- Conditional CSS for the width of the form -->
        <div id="myelement" class="text-black h-full">
          <!-- Loading Sign-->
          <div
            role="status"
            class="absolute -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2"
            v-if="loading"
          >
            <div
              :aria-hidden="loading"
              class="w-20 h-20 spinner-border text-green"
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
                <!-- Create table containing existing playlists-->
                <p
                  class="text-center text-xl text-darkest font-bold max-sm:text-sm"
                >
                  Suggested Songs ({{ Object.keys(this.songs).length }})
                </p>
                <div class="py-2"></div>
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
                <div class="container text-center">
                  <table
                    class="table table-fixed text-sm max-sm:text-xs"
                    v-if="!this.loading_songs"
                  >
                    <!-- Table Header-->
                    <thead class="sticky top-0 bg-white">
                      <tr>
                        <th class="w-16 max-sm:w-8" scope="col">Name</th>
                        <th class="w-20 max-sm:w-8" scope="col">Artist(s)</th>
                        <th class="w-8 max-sm:w-4" scope="col">Remove</th>
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
                            class="bg-white px-1"
                            type="button"
                            @click="removeSong(index)"
                          >
                            <img
                              src="trash-can.png"
                              class="h-6 w-6 opacity-80 hover:opacity-100 bg-transparent"
                            />
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
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
const getUtils = () => import("../utils.js");
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
    };
  },
  methods: {
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
      this.loading_songs = false;
    },
    removeSong(index) {
      delete this.songs[index];
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
      var songs_to_add_array = Object.keys(this.songs);
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
/* @import "@vueform/multiselect/themes/default.css"; */

.multiselect {
  align-items: center;
  background: var(--ms-bg, #fff);
  border: var(--ms-border-width, 1px) solid var(--ms-border-color, #d1d5db);
  border-radius: var(--ms-radius, 4px);
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  font-size: var(--ms-font-size, 1rem);
  justify-content: flex-end;
  margin: 0 auto;
  min-height: calc(
    var(--ms-border-width, 1px) * 2 + var(--ms-font-size, 1rem) *
      var(--ms-line-height, 1.375) + var(--ms-py, 0.5rem) * 2
  );
  outline: none;
  position: relative;
  width: 100%;
}
.multiselect.is-open {
  border-radius: var(--ms-radius, 4px) var(--ms-radius, 4px) 0 0;
}
.multiselect.is-open-top {
  border-radius: 0 0 var(--ms-radius, 4px) var(--ms-radius, 4px);
}
.multiselect.is-disabled {
  background: var(--ms-bg-disabled, #f3f4f6);
  cursor: default;
}
.multiselect.is-active {
  border: var(--ms-border-width-active, var(--ms-border-width, 1px)) solid
    var(--ms-border-color-active, var(--ms-border-color, #d1d5db));
  box-shadow: 0 0 0 var(--ms-ring-width, 3px)
    var(--ms-ring-color, rgba(16, 185, 129, 0.188));
}
.multiselect-wrapper {
  align-items: center;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  justify-content: flex-end;
  margin: 0 auto;
  min-height: calc(
    var(--ms-border-width, 1px) * 2 + var(--ms-font-size, 1rem) *
      var(--ms-line-height, 1.375) + var(--ms-py, 0.5rem) * 2
  );
  outline: none;
  position: relative;
  width: 100%;
}
.multiselect-multiple-label,
.multiselect-placeholder,
.multiselect-single-label {
  align-items: center;
  background: transparent;
  box-sizing: border-box;
  display: flex;
  height: 100%;
  left: 0;
  line-height: var(--ms-line-height, 1.375);
  max-width: 100%;
  padding-left: var(--ms-px, 0.875rem);
  padding-right: calc(1.25rem + var(--ms-px, 0.875rem) * 3);
  pointer-events: none;
  position: absolute;
  top: 0;
}
.multiselect-placeholder {
  color: var(--ms-placeholder-color, #9ca3af);
}
.multiselect-single-label-text {
  display: block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.multiselect-search {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: var(--ms-bg, #fff);
  border: 0;
  border-radius: var(--ms-radius, 4px);
  bottom: 0;
  box-sizing: border-box;
  font-family: inherit;
  font-size: inherit;
  height: 100%;
  left: 0;
  outline: none;
  padding-left: var(--ms-px, 0.875rem);
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
}
.multiselect-search::-webkit-search-cancel-button,
.multiselect-search::-webkit-search-decoration,
.multiselect-search::-webkit-search-results-button,
.multiselect-search::-webkit-search-results-decoration {
  -webkit-appearance: none;
}
.multiselect-tags {
  align-items: center;
  display: flex;
  flex-grow: 1;
  flex-shrink: 1;
  flex-wrap: wrap;
  margin: var(--ms-tag-my, 0.25rem) 0 0;
  padding-left: var(--ms-py, 0.5rem);
}
.multiselect-tag {
  align-items: center;
  background: var(--ms-tag-bg, #10b981);
  border-radius: var(--ms-tag-radius, 4px);
  color: var(--ms-tag-color, #fff);
  display: flex;
  font-size: var(--ms-tag-font-size, 0.875rem);
  font-weight: var(--ms-tag-font-weight, 600);
  line-height: var(--ms-tag-line-height, 1.25rem);
  margin-bottom: var(--ms-tag-my, 0.25rem);
  margin-right: var(--ms-tag-mx, 0.25rem);
  padding: var(--ms-tag-py, 0.125rem) 0 var(--ms-tag-py, 0.125rem)
    var(--ms-tag-px, 0.5rem);
  white-space: nowrap;
}
.multiselect-tag.is-disabled {
  background: var(--ms-tag-bg-disabled, #9ca3af);
  color: var(--ms-tag-color-disabled, #fff);
  padding-right: var(--ms-tag-px, 0.5rem);
}
.multiselect-tag-remove {
  align-items: center;
  border-radius: var(--ms-tag-remove-radius, 4px);
  display: flex;
  justify-content: center;
  margin: var(--ms-tag-remove-my, 0) var(--ms-tag-remove-mx, 0.125rem);
  padding: var(--ms-tag-remove-py, 0.25rem) var(--ms-tag-remove-px, 0.25rem);
}
.multiselect-tag-remove:hover {
  background: rgba(0, 0, 0, 0.063);
}
.multiselect-tag-remove-icon {
  background-color: currentColor;
  display: inline-block;
  height: 0.75rem;
  -webkit-mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m207.6 256 107.72-107.72c6.23-6.23 6.23-16.34 0-22.58l-25.03-25.03c-6.23-6.23-16.34-6.23-22.58 0L160 208.4 52.28 100.68c-6.23-6.23-16.34-6.23-22.58 0L4.68 125.7c-6.23 6.23-6.23 16.34 0 22.58L112.4 256 4.68 363.72c-6.23 6.23-6.23 16.34 0 22.58l25.03 25.03c6.23 6.23 16.34 6.23 22.58 0L160 303.6l107.72 107.72c6.23 6.23 16.34 6.23 22.58 0l25.03-25.03c6.23-6.23 6.23-16.34 0-22.58L207.6 256z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m207.6 256 107.72-107.72c6.23-6.23 6.23-16.34 0-22.58l-25.03-25.03c-6.23-6.23-16.34-6.23-22.58 0L160 208.4 52.28 100.68c-6.23-6.23-16.34-6.23-22.58 0L4.68 125.7c-6.23 6.23-6.23 16.34 0 22.58L112.4 256 4.68 363.72c-6.23 6.23-6.23 16.34 0 22.58l25.03 25.03c6.23 6.23 16.34 6.23 22.58 0L160 303.6l107.72 107.72c6.23 6.23 16.34 6.23 22.58 0l25.03-25.03c6.23-6.23 6.23-16.34 0-22.58L207.6 256z'/%3E%3C/svg%3E");
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
  opacity: 0.8;
  width: 0.75rem;
}
.multiselect-tags-search-wrapper {
  display: inline-block;
  flex-grow: 1;
  flex-shrink: 1;
  height: 100%;
  margin: 0 var(--ms-tag-mx, 4px) var(--ms-tag-my, 4px);
  position: relative;
}
.multiselect-tags-search-copy {
  display: inline-block;
  height: 1px;
  visibility: hidden;
  white-space: pre-wrap;
  width: 100%;
}
.multiselect-tags-search {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border: 0;
  bottom: 0;
  box-sizing: border-box;
  font-family: inherit;
  font-size: inherit;
  left: 0;
  outline: none;
  padding: 0;
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
}
.multiselect-tags-search::-webkit-search-cancel-button,
.multiselect-tags-search::-webkit-search-decoration,
.multiselect-tags-search::-webkit-search-results-button,
.multiselect-tags-search::-webkit-search-results-decoration {
  -webkit-appearance: none;
}
.multiselect-inifite {
  align-items: center;
  display: flex;
  justify-content: center;
  min-height: calc(
    var(--ms-border-width, 1px) * 2 + var(--ms-font-size, 1rem) *
      var(--ms-line-height, 1.375) + var(--ms-py, 0.5rem) * 2
  );
  width: 100%;
}
.multiselect-inifite-spinner,
.multiselect-spinner {
  animation: multiselect-spin 1s linear infinite;
  background-color: var(--ms-spinner-color, #10b981);
  flex-grow: 0;
  flex-shrink: 0;
  height: 1rem;
  -webkit-mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 512 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m456.433 371.72-27.79-16.045c-7.192-4.152-10.052-13.136-6.487-20.636 25.82-54.328 23.566-118.602-6.768-171.03-30.265-52.529-84.802-86.621-144.76-91.424C262.35 71.922 256 64.953 256 56.649V24.56c0-9.31 7.916-16.609 17.204-15.96 81.795 5.717 156.412 51.902 197.611 123.408 41.301 71.385 43.99 159.096 8.042 232.792-4.082 8.369-14.361 11.575-22.424 6.92z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 512 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m456.433 371.72-27.79-16.045c-7.192-4.152-10.052-13.136-6.487-20.636 25.82-54.328 23.566-118.602-6.768-171.03-30.265-52.529-84.802-86.621-144.76-91.424C262.35 71.922 256 64.953 256 56.649V24.56c0-9.31 7.916-16.609 17.204-15.96 81.795 5.717 156.412 51.902 197.611 123.408 41.301 71.385 43.99 159.096 8.042 232.792-4.082 8.369-14.361 11.575-22.424 6.92z'/%3E%3C/svg%3E");
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
  width: 1rem;
  z-index: 10;
}
.multiselect-spinner {
  margin: 0 var(--ms-px, 0.875rem) 0 0;
}
.multiselect-clear {
  display: flex;
  flex-grow: 0;
  flex-shrink: 0;
  opacity: 1;
  padding: 0 var(--ms-px, 0.875rem) 0 0;
  position: relative;
  transition: 0.3s;
  z-index: 10;
}
.multiselect-clear:hover .multiselect-clear-icon {
  background-color: var(--ms-clear-color-hover, #000);
}
.multiselect-clear-icon {
  background-color: var(--ms-clear-color, #999);
  display: inline-block;
  -webkit-mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m207.6 256 107.72-107.72c6.23-6.23 6.23-16.34 0-22.58l-25.03-25.03c-6.23-6.23-16.34-6.23-22.58 0L160 208.4 52.28 100.68c-6.23-6.23-16.34-6.23-22.58 0L4.68 125.7c-6.23 6.23-6.23 16.34 0 22.58L112.4 256 4.68 363.72c-6.23 6.23-6.23 16.34 0 22.58l25.03 25.03c6.23 6.23 16.34 6.23 22.58 0L160 303.6l107.72 107.72c6.23 6.23 16.34 6.23 22.58 0l25.03-25.03c6.23-6.23 6.23-16.34 0-22.58L207.6 256z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='m207.6 256 107.72-107.72c6.23-6.23 6.23-16.34 0-22.58l-25.03-25.03c-6.23-6.23-16.34-6.23-22.58 0L160 208.4 52.28 100.68c-6.23-6.23-16.34-6.23-22.58 0L4.68 125.7c-6.23 6.23-6.23 16.34 0 22.58L112.4 256 4.68 363.72c-6.23 6.23-6.23 16.34 0 22.58l25.03 25.03c6.23 6.23 16.34 6.23 22.58 0L160 303.6l107.72 107.72c6.23 6.23 16.34 6.23 22.58 0l25.03-25.03c6.23-6.23 6.23-16.34 0-22.58L207.6 256z'/%3E%3C/svg%3E");
  transition: 0.3s;
}
.multiselect-caret,
.multiselect-clear-icon {
  height: 1.125rem;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
  width: 0.625rem;
}
.multiselect-caret {
  background-color: var(--ms-caret-color, #999);
  flex-grow: 0;
  flex-shrink: 0;
  margin: 0 var(--ms-px, 0.875rem) 0 0;
  -webkit-mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M31.3 192h257.3c17.8 0 26.7 21.5 14.1 34.1L174.1 354.8c-7.8 7.8-20.5 7.8-28.3 0L17.2 226.1C4.6 213.5 13.5 192 31.3 192z'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 320 512' fill='currentColor' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M31.3 192h257.3c17.8 0 26.7 21.5 14.1 34.1L174.1 354.8c-7.8 7.8-20.5 7.8-28.3 0L17.2 226.1C4.6 213.5 13.5 192 31.3 192z'/%3E%3C/svg%3E");
  pointer-events: none;
  position: relative;
  transform: rotate(0deg);
  transition: transform 0.3s;
  z-index: 10;
}
.multiselect-caret.is-open {
  pointer-events: auto;
  transform: rotate(180deg);
}
.multiselect-dropdown {
  -webkit-overflow-scrolling: touch;
  background: var(--ms-dropdown-bg, #fff);
  border: var(--ms-dropdown-border-width, 1px) solid
    var(--ms-dropdown-border-color, #d1d5db);
  border-radius: 0 0 var(--ms-dropdown-radius, 4px)
    var(--ms-dropdown-radius, 4px);
  bottom: 0;
  display: flex;
  flex-direction: column;
  left: calc(var(--ms-border-width, 1px) * -1);
  margin-top: calc(var(--ms-border-width, 1px) * -1);
  max-height: var(--ms-max-height, 10rem);
  outline: none;
  overflow-y: scroll;
  position: absolute;
  right: calc(var(--ms-border-width, 1px) * -1);
  transform: translateY(100%);
  z-index: 100;
}
.multiselect-dropdown.is-top {
  border-radius: var(--ms-dropdown-radius, 4px) var(--ms-dropdown-radius, 4px) 0
    0;
  bottom: auto;
  top: var(--ms-border-width, 1px);
  transform: translateY(-100%);
}
.multiselect-dropdown.is-hidden {
  display: none;
}
.multiselect-options {
  display: flex;
  flex-direction: column;
  list-style: none;
  margin: 0;
  padding: 0;
}
.multiselect-group {
  margin: 0;
  padding: 0;
}
.multiselect-group-label {
  align-items: center;
  background: var(--ms-group-label-bg, #e5e7eb);
  box-sizing: border-box;
  color: var(--ms-group-label-color, #374151);
  cursor: default;
  display: flex;
  font-size: 0.875rem;
  font-weight: 600;
  justify-content: flex-start;
  line-height: var(--ms-group-label-line-height, 1.375);
  padding: var(--ms-group-label-py, 0.3rem) var(--ms-group-label-px, 0.75rem);
  text-align: left;
  text-decoration: none;
}
.multiselect-group-label.is-pointable {
  cursor: pointer;
}
.multiselect-group-label.is-pointed {
  background: var(--ms-group-label-bg-pointed, #d1d5db);
  color: var(--ms-group-label-color-pointed, #374151);
}
.multiselect-group-label.is-selected {
  background: var(--ms-group-label-bg-selected, #059669);
  color: var(--ms-group-label-color-selected, #fff);
}
.multiselect-group-label.is-disabled {
  background: var(--ms-group-label-bg-disabled, #f3f4f6);
  color: var(--ms-group-label-color-disabled, #d1d5db);
  cursor: not-allowed;
}
.multiselect-group-label.is-selected.is-pointed {
  background: var(--ms-group-label-bg-selected-pointed, #0c9e70);
  color: var(--ms-group-label-color-selected-pointed, #fff);
}
.multiselect-group-label.is-selected.is-disabled {
  background: var(--ms-group-label-bg-selected-disabled, #75cfb1);
  color: var(--ms-group-label-color-selected-disabled, #d1fae5);
}
.multiselect-group-options {
  margin: 0;
  padding: 0;
}
.multiselect-option {
  align-items: center;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  font-size: var(--ms-option-font-size, 1rem);
  justify-content: flex-start;
  line-height: var(--ms-option-line-height, 1.375);
  padding: var(--ms-option-py, 0.5rem) var(--ms-option-px, 0.75rem);
  text-align: left;
  text-decoration: none;
}
.multiselect-option.is-pointed {
  background: var(--ms-option-bg-pointed, #f3f4f6);
  color: var(--ms-option-color-pointed, #1f2937);
}
.multiselect-option.is-selected {
  background: var(--ms-option-bg-selected, #10b981);
  color: var(--ms-option-color-selected, #fff);
}
.multiselect-option.is-disabled {
  background: var(--ms-option-bg-disabled, #fff);
  color: var(--ms-option-color-disabled, #d1d5db);
  cursor: not-allowed;
}
.multiselect-option.is-selected.is-pointed {
  background: var(--ms-option-bg-selected-pointed, #26c08e);
  color: var(--ms-option-color-selected-pointed, #fff);
}
.multiselect-option.is-selected.is-disabled {
  background: var(--ms-option-bg-selected-disabled, #87dcc0);
  color: var(--ms-option-color-selected-disabled, #d1fae5);
}
.multiselect-no-options,
.multiselect-no-results {
  color: var(--ms-empty-color, #4b5563);
  padding: var(--ms-option-py, 0.5rem) var(--ms-option-px, 0.75rem);
}
.multiselect-fake-input {
  background: transparent;
  border: 0;
  bottom: -1px;
  font-size: 0;
  height: 1px;
  left: 0;
  outline: none;
  padding: 0;
  position: absolute;
  right: 0;
  width: 100%;
}
.multiselect-fake-input:active,
.multiselect-fake-input:focus {
  outline: none;
}
.multiselect-assistive-text {
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  position: absolute;
  width: 1px;
}
.multiselect-spacer {
  display: none;
}
[dir="rtl"] .multiselect-multiple-label,
[dir="rtl"] .multiselect-placeholder,
[dir="rtl"] .multiselect-single-label {
  left: auto;
  padding-left: calc(1.25rem + var(--ms-px, 0.875rem) * 3);
  padding-right: var(--ms-px, 0.875rem);
  right: 0;
}
[dir="rtl"] .multiselect-search {
  padding-left: 0;
  padding-right: var(--ms-px, 0.875rem);
}
[dir="rtl"] .multiselect-tags {
  padding-left: 0;
  padding-right: var(--ms-py, 0.5rem);
}
[dir="rtl"] .multiselect-tag {
  margin-left: var(--ms-tag-mx, 0.25rem);
  margin-right: 0;
  padding: var(--ms-tag-py, 0.125rem) var(--ms-tag-px, 0.5rem)
    var(--ms-tag-py, 0.125rem) 0;
}
[dir="rtl"] .multiselect-tag.is-disabled {
  padding-left: var(--ms-tag-px, 0.5rem);
}
[dir="rtl"] .multiselect-caret,
[dir="rtl"] .multiselect-spinner {
  margin: 0 0 0 var(--ms-px, 0.875rem);
}
[dir="rtl"] .multiselect-clear {
  padding: 0 0 0 var(--ms-px, 0.875rem);
}
@keyframes multiselect-spin {
  0% {
    transform: rotate(0);
  }
  to {
    transform: rotate(1turn);
  }
}
#myelement {
  width: 44vh;
}
@media only screen and (min-width: 800px) {
  #myelement {
    width: 65vh;
  }
}
/* @media only screen and (min-width: 800px) {
  .multiselect-placeholder {
    font-size: medium;
    text-align: left;
    padding-right: 80%;
  }
} */
</style>
