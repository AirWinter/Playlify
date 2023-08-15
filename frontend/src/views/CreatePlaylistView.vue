<template>
  <DefaultErrorModalVue />
  <TopHeader />
  <LogOutButton />
  <!-- Main Content-->
  <div class="bg-dark min-h-screen w-full py-4">
    <p class="text-center text-4xl md:text-6xl text-white font-bold">
      Create a Playlist
    </p>
    <MultiStepComponent />
  </div>
</template>

<script setup lang="ts">
import TopHeader from "../components/TopHeader.vue";
import MultiStepComponent from "../components/MultiStep/MultiStepComponent.vue";
import LogOutButton from "../components/LogOutButton.vue";
import { onBeforeMount } from "vue";
import DefaultErrorModalVue from "@/components/DefaultErrorModal.vue";

onBeforeMount(() => {
  document.body.style.overscrollBehavior = "none";
});
</script>
