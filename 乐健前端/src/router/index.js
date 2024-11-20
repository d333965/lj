import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/create", // 添加这一行
  },
  {
    path: "/create",
    component: () => import("../views/create.vue"),
  },
  {
    path: "/getInfo",
    component: () => import("../views/getInfo.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;