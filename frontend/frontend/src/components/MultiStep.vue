<script>
import StepOne from "./StepOne.vue";
import StepTwo from "./StepTwo.vue";
import StepThree from "./StepThree.vue";

export default {
  components: {
    StepOne,
    StepTwo,
    StepThree,
  },
};
</script>

<template>
  <h1>Create a Playlist</h1>
  <FormKit type="form">
    <FormKit type="multi-step">
      <FormKit type="step" name="information" label="Basic Information">
        <StepOne />
      </FormKit>

      <FormKit type="step" name="filters" label="Filtering">
        <StepTwo />
      </FormKit>

      <FormKit type="step" name="validation" label="Validation">
        <StepThree />
      </FormKit>
    </FormKit>
  </FormKit>
</template>
