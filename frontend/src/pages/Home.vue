<template>
  <div class="container mx-auto">
    <header>
      <vue-load-image>
        <template v-slot:image>
          <div class="relative text-center">
            <img
              class="w-[1280px] h-[512px] mx-auto"
              :src="'/src/assets/images/contents/' + image.content"
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
        <p class="text-3xl font-semibold">Turn your photos into artwork.</p>
        <router-link to="/renders">Create your art now</router-link>
      </div>
    </header>
  </div>
</template>

<script>
import VueLoadImage from "vue-load-image";

let content = {
  contentImages: [
    "person.jpg",
    "car.jpg",
    "flower.jpg",
    "horse.jpg",
    "louvre.jpg",
  ],
  contentPosition: ["top-4 left-36", "bottom-4 right-36"],
};

let style = {
  styleImages: [
    "abstract.jpg",
    "abstract2.jpg",
    "impressionism.jpg",
    "van-gogh.jpg",
    "wheat-field.jpg",
  ],
  stylePosition: ["top-4 right-36", "bottom-4 left-36"],
};

function getRandomImage() {
  let randomIndex = Math.floor(Math.random() * content.contentImages.length);
  return {
    content: content.contentImages[randomIndex],
    style: style.styleImages[randomIndex],
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