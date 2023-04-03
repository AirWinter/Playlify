<template>
  <FormKit type="step" name="contactInformation">
    <FormKit
      type="text"
      name="name"
      id="name"
      label="Playlist Name"
      placeholder="Name"
      validation="required|name"
    />
    <FormKit
      type="textarea"
      name="description"
      id="description"
      label="Description (optional)"
      placeholder="Description"
      validation="length:0,300"
      validation-visibility="live"
      :validation-messages="{
        length: 'Description cannot be more than 300 characters.',
      }"
    />
    <FormKit
      type="checkbox"
      label="Public"
      help="Do you want your playlist to be public?"
      name="public"
    />
  </FormKit>
</template>
