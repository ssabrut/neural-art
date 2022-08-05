<template>
  <div class="container mx-auto">
    <form @submit.prevent="submit" enctype="multipart/form-data">
      <input
        @change="handleFileUpload"
        type="file"
        name="content_image"
        ref="newCover"
      />
      <img src="" id="content_placeholder" />
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const newCover = ref(null);
const realCover = ref(null);

onMounted(async () => {
  axios
    .get("http://localhost:3000/api/test")
    .then((res) => {
      console.log(res.data);
    })
    .catch((e) => {
      console.error(e);
    });
});

const handleFileUpload = () => {
  let reader = new FileReader();
  if (newCover.value.files) {
    if (/.(jpe?g|png|gif)$/i.test(newCover.value.files[0].name)) {
      reader.readAsDataURL(newCover.value.files[0]);
      realCover.value = newCover.value.files[0];
      reader.onload = (e) => {
        document.getElementById("content_placeholder").src = e.target.result;
      };
    }
  }
};

const submit = async () => {
  const formData = new FormData();
  formData.append("file", realCover.value);
  axios
    .post("http://localhost:3000/api/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((res) => {
      console.log(res.data);
    })
    .catch((e) => {
      console.error(e);
    });
};
</script>