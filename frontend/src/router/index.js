import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import PostFeed from '../components/PostFeed.vue'
import PostCreate from '../components/PostCreate.vue'
import PostDetail from '../components/PostDetail.vue'

const routes = [
  { path: '/', component: PostFeed },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/create', component: PostCreate },
  { path: '/post/:id', component: PostDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
