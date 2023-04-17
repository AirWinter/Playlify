<template>
  <div class="bg-dark min-h-screen">
    <!-- Main Content-->
    <div class="flex">
      <!-- Container-->
      <div class="w-full h-full relative bg-blue-400">
        <!-- Top Header with logo-->
        <div class="w-full top-0 bg-darkest h-16 py-3 px-10">
          <img src="PoweredBySpotify.png" class="h-8" />
        </div>
        <!-- Welcome Header -->
        <div class="w-full top-0 bg-dark p-10">
          <p class="text-center text-7xl text-white font-bold">
            Welcome to Playlify
          </p>
        </div>
        <!-- Link to Login -->
        <div class="w-full bg-dark flex flex-col items-center">
          <a :href="this.urlBase + 'login'">
            <button
              class="btn h-20 w-64 bg-green border-0 text-black text-3xl font-semibold hover:scale-105 hover:text-black rounded-full"
            >
              Get Started
            </button>
          </a>
        </div>
        <!-- Gap between get started and text areas below-->
        <div class="p-4 bg-dark"></div>
        <!-- Text Area-->
        <div class="w-full bg-green grid grid-cols-2" style="height: 49vh">
          <!-- Left Text Area-->
          <div class="bg-dark flex flex-col items-end p-2">
            <div class="rounded-xl bg-white opacity-95 h-80 w-96 p-3">
              <!-- Section Title-->
              <p
                class="text-center text-darker font-semibold text-4xl py-2 px-4"
              >
                What is Playlify?
              </p>
              <!-- Section Text-->
              <p class="text-center text-dark text-xl font-normal p-1">
                Playlify is a tool to help you automatically create playlists.
                Playlify goes through your entire library and selects songs that
                match all your filters. Filters include: song genre, artists and
                release date. If you don't define any filters, all your songs
                will be added.
              </p>
            </div>
          </div>
          <!-- Right Text Area-->
          <div class="bg-dark flex flex-col items-start py-2 px-4">
            <div class="rounded-xl bg-white opacity-95 h-80 w-96 p-3">
              <!-- Section Title-->
              <p class="text-center text-darker font-semibold text-4xl p-2">
                How does it work?
              </p>
              <!-- Section Text-->
              <p class="text-center text-dark text-xl font-normal p-2">
                1. Enter basic information
              </p>
              <p class="text-center text-dark text-xl font-normal p-2">
                2. Define filters to apply
              </p>
              <p class="text-center text-dark text-xl font-normal p-2">
                3. Validate suggested songs
              </p>
              <p class="text-center text-dark text-xl font-normal p-2">
                4. Submit to create the playlist
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="w-full bg-darkest bottom-0" style="height: 5vh">
      <span class="py-2 px-4" style="float: right">
        <b class="text-white text-l font-normal"
          >Created By:
          <a
            class="text-white text-l font-normal"
            href="https://github.com/AirWinter"
          >
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
    return {
      urlBase: "https://airwinter.pythonanywhere.com/",
      // urlBase: "http://localhost:5000/",
    };
  },
  methods: {},
};
</script>
