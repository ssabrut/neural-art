<template>
  <h1>Render page</h1>
</template>

<script setup>
import { onMounted } from "vue";
import axios from "axios";

onMounted(async () => {
  axios.get("http://127.0.0.1:3000/api/test").then((res) => {
    console.log(res.data);
  });
});
</script>