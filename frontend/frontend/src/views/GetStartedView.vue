<template>
  <div
    class="bg-darkest h-screen"
    @scroll.prevent
    @touchmove.prevent
    @wheel.prevent
  >
    <!-- Main Content-->
    <div class="flex" style="height: 93vh">
      <!-- Container-->
      <div class="w-full h-full relative bg-blue-400">
        <!-- Top Header with logo-->
        <div class="w-full top-0 bg-darkest p-10">
          <img src="SpotifyLogoWhite.png" class="h-10" />
        </div>
        <!-- Welcome Header -->
        <div class="w-full top-0 bg-dark p-10">
          <p class="text-center text-7xl text-white font-bold">
            Welcome to Playlify
          </p>
        </div>
        <!-- Link to Login -->
        <div class="w-full top-0 bg-dark p-10">
          <p class="text-center text-4xl font-semibold text-white">
            <a href="http://localhost:5000/login">Get Started</a>
          </p>
        </div>
        <!-- Text Area-->
        <div class="w-full h-96 bg-green grid grid-cols-2">
          <!-- Left Text Area-->
          <div class="bg-dark">
            <!-- Section Title-->
            <p class="text-center text-white font-semibold text-3xl p-4">
              What is Playlify?
            </p>
            <!-- Section Text-->
            <p>Lorem ipsum dolor</p>
          </div>
          <!-- Right Text Area-->
          <div class="bg-dark">
            <!-- Section Title-->
            <p class="text-center text-white font-semibold text-3xl p-4">
              How does it work?
            </p>
            <!-- Section Text-->
          </div>
        </div>
      </div>
    </div>
    <div class="w-full bg-darkest align-bottom" style="height: 7vh">
      <span class="p-3" style="float: right">
        <b class="text-white text-xl"
          >Created By:
          <a class="text-white text-xl" href="https://github.com/AirWinter">
            AirWinter
          </a>
        </b>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "GetStartedView",
  data: function () {
    return {};
  },
  methods: {},
};
</script>
