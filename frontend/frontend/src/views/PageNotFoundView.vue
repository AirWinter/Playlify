<template>
  <!-- Prevent scrolling on the entire page-->
  <div @scroll.prevent @touchmove.prevent @wheel.prevent>
    <!-- Top Header with logo-->
    <div class="w-full top-0 bg-darkest h-20 py-4 px-10">
      <img src="PoweredBySpotify.png" class="h-10" />
    </div>
    <div class="flex" style="height: 93vh">
      <div class="w-full h-full relative bg-dark">
        <div class="h-40"></div>
        <!-- Page Not Found Message -->
        <div class="w-full top-0 bg-dark p-16">
          <p class="text-center text-7xl text-white font-bold">
            Page Not Found
          </p>
        </div>
        <!-- Return Home Button-->
        <div class="w-full bg-dark flex flex-col items-center">
          <a href="/">
            <button
              class="btn h-20 w-64 bg-green border-0 text-black text-3xl font-semibold hover:scale-105 hover:text-black rounded-full"
            >
              Go Home
            </button>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PageNotFoundView",
  data: function () {
    return {};
  },
  methods: {},
};
</script>
