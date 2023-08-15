<template>
  <div class="modal-container fixed h-full w-full z-50 bg-transparent/[0.3]">
    <div
      class="modal bg-white w-full h-full md:top-1/3 md:left-1/3 md:w-1/3 md:h-1/3 flex flex-col rounded-xl text-center shadow-lg"
    >
      <section
        class="modal-header text-3xl font-semibold inline border-none p-0 mt-2"
        id="modalHeader"
      >
        <slot name="header"></slot>
      </section>
      <section class="modal-body text-xl p-2" id="modalDescription">
        <slot name="body"></slot>
      </section>

      <footer class="modal-footer border-none flex flex-col">
        <button
          type="button"
          class="btn btn-m bg-lime font-semibold px-4 rounded-full hover:scale-105"
          @click="handleClose"
          aria-label="Close modal"
        >
          <slot name="footer"> Close </slot>
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits } from "vue";

// Prevent scrolling in background when modal is open
document.body.style.overflow = "hidden";
const emit = defineEmits<{
  // eslint-disable-next-line
  (e: "close"): void;
}>();

const handleClose = () => {
  emit("close");
};
</script>
