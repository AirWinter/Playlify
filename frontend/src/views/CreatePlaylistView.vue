<template>
  <TopHeader />
  <!-- Main Content-->
  <div class="bg-dark min-h-screen w-full py-4">
    <p class="text-center text-5xl text-white font-bold max-sm:text-3xl">
      Create a Playlist
    </p>
    <MultiStepComponent />
  </div>
</template>

<script>
import TopHeader from "../components/TopHeader.vue";
import MultiStepComponent from "../components/MultiStepComponent.vue";

export default {
  name: "CreatePlaylistView",
  components: {
    TopHeader,
    MultiStepComponent,
  },
  data() {
    return {};
  },
};
</script>
