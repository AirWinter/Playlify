<template>
  <div class="bg-white drop-shadow-lg rounded bg-white md:m-2 m-1">
    <div class="flex sticky top-0 bg-white items-center justify-start z-40">
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
          >{{ props.title }} ({{ Object.keys(props.songs).length }})</span
        >
      </button>
    </div>
    <div class="container text-center" v-if="show_songs">
      <table class="table table-fixed text-[8px] md:text-sm">
        <!-- Table Header-->
        <thead class="sticky top-5 md:top-10 bg-white z-30">
          <tr>
            <th class="w-8 max-sm:w-4" scope="col">Preview</th>
            <th class="w-16 max-sm:w-6" scope="col">Name</th>
            <th class="w-16 max-sm:w-6" scope="col">Artist(s)</th>
            <th class="w-10 max-sm:w-4" scope="col">Remove</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(song, index) in props.songs" :key="index">
            <!-- Play Button to preview-->
            <td class="align-middle">
              <button
                v-if="song.preview_url != undefined && song.preview_url != ''"
                type="button"
                @click="handleClickSong(song)"
                class="h-4 w-4 md:h-6 md:w-6 opacity-80"
              >
                <img
                  v-if="song_playing == song.song_name && playing"
                  src="pause.svg"
                />
                <img v-else src="play.svg" />
              </button>
            </td>
            <td class="py-3 align-middle overflow-hidden">
              <a :href="song.song_url" target="_blank">{{ song.song_name }}</a>
            </td>
            <td class="py-3 align-middle">
              <a
                v-for="(artist, index) in song.artists"
                :key="index"
                :href="artist.external_url"
                target="_blank"
                >{{
                  artist.name +
                  (index < Object.keys(song.artists).length - 1 ? ", " : "")
                }}</a
              >
            </td>
            <td class="align-middle overflow-hidden">
              <button
                class="bg-transparent px-1"
                type="button"
                @click="handleRemoveSong(index)"
              >
                <img
                  src="trash-can.png"
                  class="h-4 w-4 md:h-6 md:w-6 opacity-80 hover:opacity-100"
                />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button
        v-if="props.get_more"
        type="button"
        class="bg-white border-2 border-black text-sm h-8 w-20 max-sm:h-8 max-sm:w-20 max-sm:text-xs rounded-full text-black opacity-90 hover:opacity-100 font-bold mb-1"
        @click="emit('get-more')"
      >
        Get More
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Ref, ref, defineEmits, defineProps } from "vue";
import type { Song } from "./types";

const emit = defineEmits<{
  // eslint-disable-next-line
  (e: "remove-song", index: string): void;
  // eslint-disable-next-line
  (e: "get-more"): void;
}>();

const props = defineProps<{
  title: string;
  songs: Record<string, Song>;
  get_more: boolean;
}>();

let show_songs: Ref<boolean> = ref(false);

var song_playing: Ref<string> = ref("");
var playing: Ref<boolean> = ref(false);

const handleShowSongs = () => {
  show_songs.value = !show_songs.value;
  if (!show_songs.value) {
    handlePauseSong();
  }
};

const endEventListener = () => {
  handlePauseSong();
};

var player: HTMLAudioElement;

const handlePlaySong = (song: Song) => {
  if (player != undefined) {
    player.pause();
  }
  if (song.song_name != song_playing.value) {
    player = new Audio(song.preview_url);
    player.addEventListener("ended", endEventListener);
    song_playing.value = song.song_name;
  }
  player.play();
  playing.value = true;
};

const handlePauseSong = () => {
  player.pause();
  playing.value = false;
};

const handleClickSong = (song: Song) => {
  if (song.song_name == song_playing.value && playing.value) {
    handlePauseSong();
  } else {
    handlePlaySong(song);
  }
};

const handleRemoveSong = (index: string) => {
  if (playing.value) {
    handlePauseSong();
  }
  emit("remove-song", index);
};
</script>
