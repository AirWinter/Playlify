<template>
  <!-- Set the background colour everywhere -->
  <div class="bg-dark min-h-screen">
    <!-- Top Header with Log Out Button -->
    <TopHeader />
    <LogOutButton />
    <!-- Main Content -->
    <div class="w-full h-full relative overflow-y-scroll">
      <div class="px-2 py-3">
        <!-- Recently Played Text -->
        <div class="flex items-center justify-between">
          <h1 class="pl-2 py-2 text-4xl text-white font-bold tracking-wide">
            Your Playlists
          </h1>
        </div>
        <!-- Cards -->
        <div class="w-full flex flex-wrap">
          <!-- Hardcoded Create Playlist -->
          <div :class="styling_string">
            <a href="/create-playlist" style="text-decoration: none">
              <div
                class="bg-card_bg opacity-80 hover:opacity-95 w-full h-full p-3 rounded-lg shadow-md"
              >
                <img src="PlusSign.png" class="h-4/5 w-full shadow rounded" />

                <h1
                  class="text-xl mb-[12px] mt-3 font-semibold truncate text-white text-center tracking-wide"
                >
                  Create Playlist
                </h1>
              </div>
            </a>
          </div>
          <!-- All of their playlists -->
          <div
            v-for="playlist in playlists"
            :key="playlists.indexOf(playlist)"
            :class="styling_string"
          >
            <!-- Card -->
            <a
              :href="playlist.link"
              target="_blank"
              style="text-decoration: none"
            >
              <div
                class="bg-card_bg opacity-80 hover:opacity-100 w-full h-full pb-4 p-3 rounded-lg shadow-md"
              >
                <!-- Playlist Cover Photo -->
                <img
                  v-if="playlist.imageUrl != ''"
                  :src="playlist.imageUrl"
                  class="h-4/5 w-full object-cover shadow mb-2 rounded"
                />
                <img
                  v-else
                  src="PlaceholderIcon.png"
                  class="h-36 w-36 object-cover shadow mb-2 rounded"
                />
                <!-- Playlist Title -->
                <h1
                  class="text-base font-semibold text-white tracking-wide truncate"
                >
                  {{ playlist.name }}
                </h1>
                <!-- Playlist Description -->
                <h2
                  v-if="playlist.description != ''"
                  class="text-sm text-lightest tracking-wide truncate line-clamp-2 mb-1"
                >
                  {{ playlist.description }}
                </h2>
                <h2
                  v-else
                  class="text-sm text-lightest tracking-wide truncate line-clamp-2 mb-1"
                >
                  {{ "By " + playlist.creator }}
                </h2>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import TopHeader from "../components/TopHeader.vue";
import LogOutButton from "../components/LogOutButton.vue";
import { Ref, ref, onBeforeMount } from "vue";
import type { Playlist } from "./types";
import { getPlaylists } from "../services/playlists";

var playlists: Ref<Playlist[]> = ref([]);

onBeforeMount(async () => {
  document.body.style.overscrollBehavior = "none";
  playlists.value = await getPlaylists();
});

const styling_string =
  "p-2 w-1/2 h-11/12 md:w-1/4 lg:w-1/5 xl:w-1/6 2xl:w-[12.5%] 3xl:w-1/12 ";
</script>
