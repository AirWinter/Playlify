<template>
  <ModalTemplate v-if="store.getters.getShowErrorModal" @close="closeError()">
    <template v-slot:header> ERROR </template>
    <template v-slot:body>
      Oops something went wrong, we'll redirect you to the homepage.
    </template>
    <template v-slot:footer> To Homepage </template>
  </ModalTemplate>
</template>
<script setup lang="ts">
import { useStore } from "vuex";
import ModalTemplate from "./ModalTemplate.vue";
import router from "@/router/index";

const store = useStore();

const closeError = () => {
  document.body.style.overflow = "";
  localStorage.clear();
  sessionStorage.clear();
  router.push("/");
};
</script>
