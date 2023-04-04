<template>
  <FormKit
    type="select"
    label="Genre of your playlist"
    name="genre"
    :options="[
      { label: 'Pop', value: 'pop' },
      { label: 'Rock', value: 'rock' },
      { label: 'Rap', value: 'rap' },
      { label: 'Indie', value: 'indie' },
      { label: 'R&B', value: 'r-n-b' },
    ]"
  />
  <div class="double">
    <FormKit
      type="month"
      help="Add songs created after this date"
      label="Songs Created After"
      name="created-after-month"
    />
    <FormKit
      type="month"
      help="Add songs created before this date"
      label="Songs Created Before"
      name="created-before-month"
    />
  </div>
</template>
