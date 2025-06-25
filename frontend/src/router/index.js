import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  { path: '/', component: () => import('../components/Welcome.vue') },
  { path: '/login', component: () => import('../components/Login.vue') },
  { path: '/register', component: () => import('../components/Register.vue') },
  { path: '/logout', component: () => import('../components/Logout.vue') },
  { path: '/password-reset', component: () => import('../components/PasswordReset.vue') },
  { path: '/profile', component: () => import('../components/UserProfile.vue') },
  { path: '/notifications', component: () => import('../components/Notifications.vue') },
  { path: '/chat', component: () => import('../components/Chat.vue') },
  { path: '/search', component: () => import('../components/Search.vue') },
  { path: '/create', component: () => import('../components/PostCreate.vue') },
  { path: '/post/:id', component: () => import('../components/PostDetail.vue'), props: true },
  { path: '/feed', component: () => import('../components/PostFeed.vue') },
  { path: '/story/create', component: () => import('../components/StoryCreate.vue') },
]

import store from '../store' // Assuming a Vuex store or similar for auth state

const router = createRouter({
  history: createWebHistory(),
  routes,
})

import axios from 'axios'

// Navigation guard to protect routes and handle initial redirect
router.beforeEach(async (to, from, next) => {
  const publicPages = ['/', '/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = store.getters.isAuthenticated // Adjust based on actual auth state

  if (!loggedIn) {
    // Check if user is registered by calling backend or checking token
    try {
      await axios.get('/api/users/me/')
      // User is registered but not logged in, redirect to login
      if (to.path === '/') {
        return next('/login')
      }
    } catch {
      // User not registered, redirect to register page if at root
      if (to.path === '/') {
        return next('/register')
      }
    }
  }

  if (authRequired && !loggedIn) {
    return next('/login')
  }
  next()
})

export default router
