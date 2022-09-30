<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <div>
    <Navbar title="neuralart" version="alpha" />
    <router-view> </router-view>
  </div>
</template>
