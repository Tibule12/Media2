import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import mitt from 'mitt'
import './assets/styles.css'
import './axiosConfig'  // Import axios config to set baseURL

const emitter = mitt()

const app = createApp(App)
app.config.globalProperties.emitter = emitter
app.use(store)
app.use(router)
app.mount('#app')
