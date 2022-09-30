<template>
  <div class="container mx-auto mb-8">
    <form @submit.prevent="submit" enctype="multipart/form-data">
      <div class="text-end mb-4">
        <button class="bg-blue-500 px-3 py-1 rounded-full text-white ring ring-blue-500 cursor-pointer hover:bg-blue-400 hover:ring-blue-400" type="submit">Create Art</button>
      </div>
      <div class="border rounded mb-8">
        <div class="bg-gray-50 p-4 border-b">
          <div class="flex justify-between items-center">
            <p class="font-semibold">Content image</p>
            <label class="bg-blue-500 px-3 py-1 rounded text-white ring ring-blue-500 cursor-pointer hover:bg-blue-400 hover:ring-blue-400" for="content_image">Upload</label>
            <input
              class="hidden"
              @change="handleContentUpload"
              type="file"
              name="content_image"
              id="content_image"
              ref="contentCover"
            />
          </div>
        </div>
        <div class="my-6 mx-4 grid place-items-center" id="content_placeholder">
          <p>You have no content photo uploaded, please upload your photo!</p>
        </div>
      </div>
      <div class="border rounded">
        <div class="bg-gray-50 p-4 border-b">
          <div class="flex justify-between items-center">
            <p class="font-semibold">Style image</p>
            <label class="bg-blue-500 px-3 py-1 rounded text-white ring ring-blue-500 cursor-pointer hover:bg-blue-400 hover:ring-blue-400" for="style_image">Upload</label>
            <input
              class="hidden"
              @change="handleStyleUpload"
              type="file"
              name="style_image"
              id="style_image"
              ref="styleCover"
            />
          </div>
        </div>
        <div class="my-6 mx-4 grid place-items-center" id="style_placeholder">
          <p>You have no style photo uploaded, please upload your photo!</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const contentCover = ref(null);
const realContent = ref(null);
const styleCover = ref(null);
const realStyle = ref(null);
const router = useRouter();

const handleContentUpload = () => {
  let reader = new FileReader();
  if (contentCover.value.files) {
    if (/.(jpe?g|png|gif)$/i.test(contentCover.value.files[0].name)) {
      reader.readAsDataURL(contentCover.value.files[0]);
      realContent.value = contentCover.value.files[0];
      reader.onload = (e) => {
        const contentPlaceholder = document.getElementById("content_placeholder");
        contentPlaceholder.removeChild(contentPlaceholder.firstChild);
        const imagePlaceholder = document.createElement('img');
        imagePlaceholder.classList.add('w-[288px]', 'h-[288px]', 'object-cover', 'shadow-lg', 'rounded');
        contentPlaceholder.appendChild(imagePlaceholder).src = e.target.result;
      };
    }
  }
};

const handleStyleUpload = () => {
  let reader = new FileReader();
  if (styleCover.value.files) {
    if (/.(jpe?g|png|gif)$/i.test(styleCover.value.files[0].name)) {
      reader.readAsDataURL(styleCover.value.files[0]);
      realStyle.value = styleCover.value.files[0];
      reader.onload = (e) => {
        const stylePlaceholder = document.getElementById("style_placeholder");
        stylePlaceholder.removeChild(stylePlaceholder.firstChild);
        const imagePlaceholder = document.createElement('img');
        imagePlaceholder.classList.add('w-[288px]', 'h-[288px]', 'object-cover', 'shadow-lg', 'rounded');
        stylePlaceholder.appendChild(imagePlaceholder).src = e.target.result;
      };
    }
  }
};

const submit = async () => {
  const formData = new FormData();
  formData.append("files", realContent.value);
  formData.append("files", realStyle.value);
  
  const res = await axios.post('http://localhost:3000/api/upload', formData, {
    params: {
      event1: "contents",
      event2: "styles",
    },
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  router.push(res.data);

  // const res1 = await axios.get('http://localhost:3000/api/download/', {
  //   data: {
  //     path: res.data[0],
  //   },
  // });

  // const res2 = await axios.get('http://localhost:3000/api/download/', {
  //   data: {
  //     path: res.data[1],
  //   }
  // });
};
</script>