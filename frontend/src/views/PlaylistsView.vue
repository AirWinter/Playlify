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
          <div class="p-2 w-48 h-64 max-sm:w-44">
            <a href="/create-playlist" style="text-decoration: none">
              <div
                class="bg-card_bg opacity-80 hover:opacity-95 w-full h-full p-3 rounded-lg shadow-md"
              >
                <img src="PlusSign.png" class="h-36 w-36 shadow rounded" />

                <h1
                  class="text-xl mt-3 font-semibold text-white text-center tracking-wide"
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
            class="p-2 w-48 h-64 max-sm:w-44"
          >
            <!-- Card -->
            <a
              :href="playlist.link"
              target="_blank"
              style="text-decoration: none"
            >
              <div
                class="bg-card_bg opacity-80 hover:opacity-100 w-full h-full p-3 rounded-lg shadow-md"
              >
                <!-- Playlist Cover Photo -->
                <img
                  v-if="playlist.imageUrl != ''"
                  :src="playlist.imageUrl"
                  class="h-36 w-36 object-cover shadow mb-2 rounded"
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
                  class="text-sm text-lightest tracking-wide line-clamp-2 mb-1"
                >
                  {{ playlist.description }}
                </h2>
                <h2
                  v-else
                  class="text-sm text-lightest tracking-wide line-clamp-2 mb-1"
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
import axios from "axios";
import { Ref, ref, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import type { Playlist } from "./types";
const getUtils = () => import("../utils");

const router = useRouter();
const urlBase: string = process.env.VUE_APP_URL_BASE;
var playlists: Ref<Playlist[]> = ref([]);

const getPlaylists = async () => {
  const token_string: string = await (await getUtils()).accessToken; // lazy import and then await async function
  if (token_string === "") {
    router.push("/");
  } else {
    await axios({
      method: "get",
      url: `${urlBase}/backend/getPlaylists`,
      headers: {
        Token: token_string,
      },
    })
      .then((value) => {
        playlists.value = value.data;
      })
      .catch((error) => {
        console.log(error);
        localStorage.clear();
        sessionStorage.clear();
        router.push("/"); // If there's an error go to home page
      });
  }
};

onBeforeMount(() => {
  document.body.style.overscrollBehavior = "none";
  getPlaylists();
});
</script>
