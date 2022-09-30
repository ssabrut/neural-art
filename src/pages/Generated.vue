<template>
  <img :src="imagePath" id="generated_image" />
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const imagePath = ref(null);
const itemPreviewImage = ref(null);

onMounted(async () => {
  const route = useRoute();
  const generatedImage = await axios.get(`http://localhost:3000/api/generated/${route.query.id}`);
  const base64Image = btoa(
    new Uint8Array(generatedImage).reduce(
      (data, byte) => data + String.fromCharCode(byte),
      ""
    )
  );
  console.log(generatedImage.data);
});
</script>