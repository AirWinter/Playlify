<template>
  <FormKit type="step" name="filters" label="Filters">
    <div>
      <p class="p-1 font-bold text-black text-sm max-sm:text-xs">
        Genres to add to your playlist (Optional)
      </p>
      <Multiselect
        mode="tags"
        v-model="local_filters.genres"
        :groups="true"
        :options="genres_options"
        :close-on-select="true"
        class="multiselect-green"
        :classes="{
          container:
            'relative mx-auto w-full flex items-center justify-end box-border cursor-pointer border-[1px] border-outer rounded bg-white text-base leading-snug',
          tag: 'bg-lime text-white text-xs font-semibold py-0.5 pl-2 rounded-full mr-1 mb-1 flex items-center whitespace-nowrap rtl:pl-0 rtl:pr-0 rtl:mr-0 rtl:ml-0',
          groupLabel:
            'flex text-m box-border items-center justify-start text-white text-left py-1 px-3 font-bold bg-lime cursor-default leading-normal',
        }"
        name="GenresMultiselect"
        placeholder="Genres"
        :searchable="true"
      />
      <p class="p-0.5 font text-slate-700 text-xs max-sm:text-2xs">
        Add songs that match any of these genres
      </p>
    </div>
    <div>
      <p class="p-1 font-bold text-black text-sm max-sm:text-xs">
        Artists for your playlist (Optional)
      </p>
      <Multiselect
        mode="tags"
        v-model="local_filters.artists"
        :options="artist_options"
        class="multiselect-green"
        :classes="{
          container:
            'relative mx-auto w-full flex items-center justify-end box-border cursor-pointer border-[1px] border-outer rounded bg-white text-base leading-snug',
          tag: 'bg-lime text-white text-xs font-semibold py-0.5 pl-2 rounded-full mr-1 mb-1 flex items-center whitespace-nowrap rtl:pl-0 rtl:pr-2 rtl:mr-0 rtl:ml-1',
        }"
        name="ArtistsMultiselect"
        placeholder="Artists"
        :searchable="true"
      />
      <p class="p-0.5 font text-slate-700 text-xs max-sm:text-2xs">
        Add songs from any of these artists
      </p>
    </div>
    <div class="p-1"></div>
    <FormKit
      type="month"
      v-model="local_filters.created_after_month"
      help="Add songs created after this date"
      label="Songs Created After (Optional)"
      name="created_after_month"
    />

    <FormKit
      type="month"
      v-model="local_filters.created_before_month"
      help="Add songs created before this date"
      label="Songs Created Before (Optional)"
      name="created_before_month"
    />
    <!-- Go back to basic Information -->
    <template #stepPrevious="{ handlers, node }">
      <button
        type="button"
        class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs hover:bg-green text-white font-bold rounded-full"
        @click="handlers.incrementStep(-1, node.context)()"
      >
        Previous
      </button>
    </template>
    <!-- Go to validation step-->
    <template #stepNext="{ handlers, node }">
      <button
        type="button"
        v-if="
          local_filters.created_before_month >
            local_filters.created_after_month ||
          local_filters.created_before_month == '' ||
          local_filters.created_after_month == ''
        "
        class="btn-sm bg-lime text-base h-10 w-24 max-sm:h-8 max-sm:w-20 max-sm:text-xs hover:bg-green text-white font-bold rounded-full"
        @click="handlers.incrementStep(1, node.context)()"
        data-next="true"
      >
        Validate
      </button>
      <div v-else>Invalid Date range</div>
    </template>
  </FormKit>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref } from "vue";
import Multiselect from "@vueform/multiselect";
import { Artist_Options, Filters, Genre_Options } from "./types";

const props = defineProps<{
  genres_options: Array<Genre_Options>;
  artist_options: Array<Artist_Options>;
  filters: Filters;
}>();

defineEmits(["change_month"]);

let local_filters = ref(props.filters);
</script>

<style>
@import "@vueform/multiselect/themes/default.css";

#myelement {
  width: 300px;
}
@media only screen and (min-width: 800px) {
  #myelement {
    width: 490px;
  }
}
</style>
