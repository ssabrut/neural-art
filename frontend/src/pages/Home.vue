<template>
  <div class="container mx-auto">
    <header>
      <vue-load-image>
        <template v-slot:image>
          <div class="relative text-center">
            <img
              class="
                w-[1280px]
                h-[512px]
                mx-auto
                object-fill
                border border-black
              "
              :src="'/src/assets/images/generated/' + image.generated"
            />
            <div class="absolute bg-white px-2 pt-2" :class="position.content">
              <img
                class="w-56 h-auto object-contain"
                :src="'/src/assets/images/contents/' + image.content"
              />
              <p class="py-2 font-semibold">Content Image</p>
            </div>
            <div class="absolute bg-white px-2 pt-2" :class="position.style">
              <img
                class="w-56 h-36"
                :src="'/src/assets/images/styles/' + image.style"
              />
              <p class="py-2 font-semibold">Style Image</p>
            </div>
          </div>
        </template>
      </vue-load-image>
      <div class="mx-36 mt-6">
        <p class="text-3xl font-semibold mb-6">Turn your photos into artwork.</p>
        <router-link class="bg-blue-500 px-3 py-2 rounded-full text-white ring ring-blue-500 cursor-pointer hover:bg-blue-400 hover:ring-blue-400" to="/renders">Create your art now</router-link>
      </div>
    </header>
  </div>
</template>

<script>
import VueLoadImage from "vue-load-image";

let content = {
  contentImages: ["louvre.jpg", "flower.jpg", "horse.jpg"],
  contentPosition: ["top-4 left-36", "bottom-4 right-36"],
};

let style = {
  styleImages: ["starry-night.jpg", "impressionism.jpg", "wheat-field.jpg"],
  stylePosition: ["top-4 right-36", "bottom-4 left-36"],
};

let generated = [
  "louvre_starry.jpg",
  "flower_impresionism.jpg",
  "horse_wheat.jpg",
];

function getRandomImage() {
  let randomIndex = Math.floor(Math.random() * content.contentImages.length);
  return {
    content: content.contentImages[randomIndex],
    style: style.styleImages[randomIndex],
    generated: generated[randomIndex],
  };
}

function getRandomPosition() {
  let randomIndex = Math.floor(Math.random() * content.contentPosition.length);
  return {
    content: content.contentPosition[randomIndex],
    style: style.stylePosition[randomIndex],
  };
}

export default {
  components: {
    "vue-load-image": VueLoadImage,
  },
  data() {
    return {
      image: getRandomImage(),
      position: getRandomPosition(),
    };
  },
};
</script>