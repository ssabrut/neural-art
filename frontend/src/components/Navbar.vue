<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  version: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <nav class="grid place-items-center py-5 bg-white">
    <a href="/">
      <span class="text-2xl font-semibold">{{ title }}</span>
      <sup>
        <span class="text-xs pl-px text-blue-500 font-semibold">{{ version }}</span>
      </sup>
    </a>
  </nav>
</template>