<template>
  <!-- Log Out Button -->
  <div class="absolute top-3 right-12 max-sm:top-2 max-sm:right-4">
    <a :href="this.urlBase + 'logout'"
      ><button
        type="button"
        class="btn bg-snow h-10 w-28 max-sm:h-8 max-sm:w-20 max-sm:text-sm font-semibold rounded-full text-black hover:underline"
        @click="handleLogout()"
      >
        Log Out
      </button>
    </a>
  </div>
</template>

<script>
export default {
  name: "LogOutButton",
  data() {
    return {
      urlBase: "https://airwinter.pythonanywhere.com/",
      //   urlBase: "http://localhost:5000/",
    };
  },
  methods: {
    handleLogout() {
      localStorage.clear();
      sessionStorage.clear();
    },
  },
};
</script>
