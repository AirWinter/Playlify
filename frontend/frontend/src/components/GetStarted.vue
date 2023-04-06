<template>
  <div>
    <button
      type="button"
      class="btn btn-primary"
      href="http://localhost:5000/login"
    >
      {{ msg }}
    </button>
  </div>
</template>

<script>
export default {
  name: "GetStarted",
  data() {
    return {
      msg: "Get Started!",
    };
  },
};
</script>
