import { createStore } from 'vuex'
import axiosInstance from '../axiosConfig'

const store = createStore({
  state() {
    return {
      token: localStorage.getItem('token') || '',
      user: null,
    }
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token
    },
    getUser(state) {
      return state.user
    }
  },
  mutations: {
    setToken(state, token) {
      state.token = token
    },
    setUser(state, user) {
      state.user = user
    },
    clearAuth(state) {
      state.token = ''
      state.user = null
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        // credentials contains idToken from Firebase client SDK
        const response = await axiosInstance.post('/api/auth/login/', { idToken: credentials.idToken })
        const uid = response.data.uid
        const token = response.data.token || credentials.idToken // fallback to idToken if no token returned
        localStorage.setItem('token', token)
        commit('setToken', token)
        // Store user info from response
        commit('setUser', {
          uid: uid,
          email: response.data.email,
          displayName: response.data.displayName
        })
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`
        return true
      } catch (error) {
        commit('clearAuth')
        localStorage.removeItem('token')
        throw error
      }
    },
    logout({ commit }) {
      commit('clearAuth')
      localStorage.removeItem('token')
      delete axiosInstance.defaults.headers.common['Authorization']
    }
  }
})

export default store
