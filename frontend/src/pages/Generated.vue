<template>
  <img :src="'data:image/jpg;base64,' + itemPreviewImage" id="generated_image" />
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
  console.log(typeof generatedImage.data);
  const image = new Image();
  const reader = new FileReader();

  reader.onload = (evt) => {
    itemPreviewImage.value = evt.target.result;
  };

  reader.readAsDataURL(generatedImage.data);
});
</script>