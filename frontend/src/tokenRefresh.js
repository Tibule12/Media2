import supabase from './supabaseConfig'
import store from './store'

// Listen for auth state changes and update token in localStorage and Vuex store
supabase.auth.onAuthStateChange((event, session) => {
  if (session && session.access_token) {
    localStorage.setItem('token', session.access_token)
    store.commit('setToken', session.access_token)
  } else {
    localStorage.removeItem('token')
    store.commit('clearAuth')
  }
})

// Optionally, refresh token periodically every 45 minutes
setInterval(async () => {
  const session = supabase.auth.session()
  if (session) {
    const { data, error } = await supabase.auth.refreshSession()
    if (!error && data && data.access_token) {
      localStorage.setItem('token', data.access_token)
      store.commit('setToken', data.access_token)
    }
  }
}, 45 * 60 * 1000) // 45 minutes

export default null
