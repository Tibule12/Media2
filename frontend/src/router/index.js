import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import PostFeed from '../components/PostFeed.vue'
import PostCreate from '../components/PostCreate.vue'
import PostDetail from '../components/PostDetail.vue'
import Welcome from '../components/Welcome.vue'

import Logout from '../components/Logout.vue'

import PasswordReset from '../components/PasswordReset.vue'

import UserProfile from '../components/UserProfile.vue'

import Notifications from '../components/Notifications.vue'

import Chat from '../components/Chat.vue'

import Search from '../components/Search.vue'

const routes = [
  { path: '/', component: Welcome },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },
  { path: '/password-reset', component: PasswordReset },
  { path: '/profile', component: UserProfile },
  { path: '/notifications', component: Notifications },
  { path: '/chat', component: Chat },
  { path: '/search', component: Search },
  { path: '/create', component: PostCreate },
  { path: '/post/:id', component: PostDetail, props: true },
]

import store from '../store' // Assuming a Vuex store or similar for auth state

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const publicPages = ['/', '/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = store.getters.isAuthenticated // Adjust based on actual auth state

  if (authRequired && !loggedIn) {
    return next('/login')
  }
  next()
})

export default router
