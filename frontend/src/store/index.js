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
        const response = await axiosInstance.post('/api/auth/login/', credentials)
        const token = response.data.token
        localStorage.setItem('token', token)
        commit('setToken', token)
        // Optionally fetch user info here
        commit('setUser', response.data.user || null)
        axiosInstance.defaults.headers.common['Authorization'] = `Token ${token}`
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
