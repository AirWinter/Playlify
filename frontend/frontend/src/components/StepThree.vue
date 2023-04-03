<template>
  <!-- Ask the user to share how they heard about us -->
  <h2>Thank you for taking the time to submit your talk</h2>
  <p>If you don't mind we'd love to know how you heard about VueUniverse.</p>
  <FormKit
    type="radio"
    label="How did you hear about VueUniverse?"
    :options="['Online Ad', 'Friend or Coworker', 'Search Results', 'Other']"
  />
</template>
