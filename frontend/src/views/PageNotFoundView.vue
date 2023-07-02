<template>
  <!-- Prevent scrolling on the entire page-->
  <div
    @scroll.prevent
    @touchmove.prevent
    @wheel.prevent
    class="bg-dark min-h-screen w-full"
  >
    <TopHeader />
    <div class="relative">
      <div class="h-24 md:h-40"></div>
      <!-- Page Not Found Message -->
      <div class="w-full top-0 bg-dark p-8 md:p-16">
        <p class="text-center text-5xl md:text-7xl text-white font-bold">
          Page Not Found
        </p>
      </div>
      <!-- Return Home Button-->
      <div class="w-full bg-dark flex flex-col items-center">
        <a href="/">
          <button
            class="btn h-14 w-36 md:h-20 md:w-64 bg-green border-0 text-black text-2xl md:text-4xl font-semibold hover:scale-105 hover:text-black rounded-full"
          >
            Go Home
          </button>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import TopHeader from "@/components/TopHeader.vue";
</script>
