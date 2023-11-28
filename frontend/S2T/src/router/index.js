import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import SignUp from '@/views/SignUp.vue'
import Dashboard from '@/views/Dashboard.vue'
import UserStats from '@/views/UserStats.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
      name: 'home',
      component: Login,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter() {
        if (localStorage.getItem("access_token") && localStorage.getItem("username")) {
          return "/dashboard";
        }
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,
      beforeEnter() {
        if (localStorage.getItem("access_token") && localStorage.getItem("username")) {
          return "/dashboard";
        }
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      beforeEnter() {
        if (!localStorage.getItem("access_token") && !localStorage.getItem("username")) {
          return "/login";
        }
      }
    },
    {
      path: '/insights',
      'name': 'insights',
      component: UserStats,
      beforeEnter() {
        if (!localStorage.getItem("access_token") && !localStorage.getItem("username")) {
          return "/dashboard";
        }
      }
    },
    {
      path: "/logout",
      name: "logout",
      beforeEnter() {
        localStorage.clear();
        return "/login";
      }
    }
  ]
})

export default router
