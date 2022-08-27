import { createRouter, createWebHistory } from "vue-router";
import Home from './pages/Home.vue';
import Render from './pages/Render.vue'
import Generated from './pages/Generated.vue'

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/renders",
    name: "render",
    component: Render,
  },
  {
    path: '/generated',
    name: 'generated',
    component: Generated,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;