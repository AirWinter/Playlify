<template>
  <FormKit type="text" label="Talk Title" validation="required" />
  <FormKit
    type="textarea"
    label="Talk Brief"
    validation="required|length:100"
    help="What is your talk about?"
  />
  <FormKit
    type="radio"
    label="Talk Track"
    help="Which track are you submitting for?"
    :options="['Development', 'Testing', 'Leadership']"
  />
</template>
