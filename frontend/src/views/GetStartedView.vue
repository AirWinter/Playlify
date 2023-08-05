<template>
  <div class="bg-dark min-h-screen">
    <!-- Top Header with logo-->
    <TopHeader />
    <PageLinks />
    <!-- Main Content-->
    <div class="md:flex">
      <!-- Container-->
      <div class="w-full h-full relative bg-darkgr">
        <!-- Welcome Header -->
        <div class="w-full top-0 bg-dark max-sm:py-4 py-10">
          <p class="text-center text-4xl md:text-7xl text-white font-bold">
            Welcome to Playlify
          </p>
        </div>
        <!-- Link to Login -->
        <div class="w-full bg-dark flex flex-col items-center">
          <a :href="urlBase + '/authentication/login'">
            <button
              class="btn h-12 w-40 md:h-20 md:w-64 bg-green border-0 text-black text-xl md:text-3xl font-semibold hover:scale-105 hover:text-black rounded-full"
            >
              Get Started
            </button>
          </a>
        </div>
        <!-- Gap between get started and text areas below-->
        <div class="p-1 bg-dark"></div>
        <!-- Text Area-->
        <div
          class="w-full bg-dark grid grid-cols-1 md:grid-cols-2"
          style="height: 49vh"
        >
          <!-- Left Text Area-->
          <div
            class="bg-dark flex flex-col items-center md:items-end max-sm:py-2 py-6 px-2"
          >
            <div
              class="flex flex-col items-center rounded-xl bg-white opacity-95 max-sm:h-auto max-sm:w-4/5 h-80 w-96 max-sm:p-1 p-6"
            >
              <!-- Section Title-->
              <p
                class="text-center text-darker font-semibold text-xl md:text-4xl"
              >
                What is Playlify?
              </p>
              <!-- Section Text-->
              <p
                class="text-center text-dark text-sm md:text-xl font-normal p-1 mb-1"
              >
                Playlify is a tool to help you automatically create playlists in
                Spotify. Playlify goes through your entire library and selects
                songs that match all your filters. Filters include: song genre,
                artists and release date. If you don't define any filters, all
                your songs will be added.
              </p>
            </div>
          </div>
          <!-- Right Text Area-->
          <div
            class="bg-dark flex flex-col items-center md:items-start max-sm:py-2 py-6 px-2"
          >
            <div
              class="flex flex-col items-center rounded-xl bg-white opacity-95 max-sm:h-auto max-sm:w-4/5 h-80 w-96 max-sm:p-1 p-6"
            >
              <!-- Section Title-->
              <p
                class="text-center text-darker font-semibold text-xl md:text-4xl mb-1"
              >
                How does it work?
              </p>
              <!-- Section Text-->
              <p
                class="text-center text-dark text-sm md:text-xl font-normal p-1"
              >
                1. Enter basic information
              </p>
              <p
                class="text-center text-dark text-sm md:text-xl font-normal p-1"
              >
                2. Define filters to apply
              </p>
              <p
                class="text-center text-dark text-sm md:text-xl font-normal p-1"
              >
                3. Validate suggested songs
              </p>
              <p
                class="text-center text-dark text-sm md:text-xl font-normal p-1 mb-1"
              >
                4. Submit to create the playlist
              </p>
            </div>
            <!-- Note only for phones -->
            <div class="p-2"></div>
            <div
              class="rounded-xl bg-white opacity-95 h-auto w-4/5 p-1 md:invisible"
            >
              <p class="text-center text-darker text-sm font-semibold">
                NOTE: We recommend accessing playlify through a computer.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="w-full bg-darkest h-8"
      style="position: fixed; bottom: 0; width: 100%"
    >
      <span class="py-1 px-2" style="float: right">
        <b class="text-white text-l font-normal"
          >Created By:
          <a
            class="text-white text-l font-normal"
            href="https://github.com/AirWinter"
            target="_blank"
          >
            AirWinter
          </a>
        </b>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import TopHeader from "@/components/TopHeader.vue";
import PageLinks from "@/components/PageLinks.vue";
import { onBeforeMount } from "vue";

const urlBase: string = process.env.VUE_APP_URL_BASE!;

onBeforeMount(() => {
  document.body.style.overscrollBehavior = "none";
});
</script>
