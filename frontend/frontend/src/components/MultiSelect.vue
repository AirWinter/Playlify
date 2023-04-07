<template>
  <div>
    <Multiselect
      v-model="value"
      mode="tags"
      :close-on-select="false"
      :searchable="true"
      :options="[
        { value: 'batman', label: 'Batman' },
        { value: 'robin', label: 'Robin' },
        { value: 'joker', label: 'Joker' },
      ]"
    />
    <p>{{ value }}</p>
  </div>
</template>

<script>
import Multiselect from "@vueform/multiselect";

export default {
  components: {
    Multiselect,
  },
  data() {
    return {
      value: null,
      options: ["Batman", "Robin", "Joker"],
    };
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css"></style>
