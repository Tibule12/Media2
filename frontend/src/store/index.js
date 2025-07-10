import { createStore } from 'vuex'
import supabase from '../supabaseConfig'
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
        // Use Supabase signInWithPassword with email and password from credentials
        const { data, error } = await supabase.auth.signInWithPassword({
          email: credentials.email,
          password: credentials.password
        })
        if (error) throw error
        const token = data.session.access_token
        localStorage.setItem('token', token)
        commit('setToken', token)
        // Store user info from Supabase user object
        commit('setUser', {
          uid: data.user.id,
          email: data.user.email,
          displayName: data.user.user_metadata?.full_name || ''
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
      supabase.auth.signOut()
    }
  }
})

export default store
