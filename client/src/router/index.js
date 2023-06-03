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
    {
      path: '/ping',
      name: 'ping',
      component: () => import('/@/app/pages/Ping.vue'),
    },
    {
      path: '/books',
      name: 'Books',
      component: () => import('/@/app/pages/Books.vue'),
    },
  ],
})

export default router
