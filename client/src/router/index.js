import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'homepage',
      component: () => import('/@/app/pages/HomePage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('/@/app/pages/Login.vue'),
    },
  ],
})

export default router
