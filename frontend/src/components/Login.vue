<template>
  <div>
    <h2>Login</h2>
<form @submit.prevent="loginUser">
      <div>
        <label>Username:</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    }
  },
  methods: {
    ...mapActions(['login']),
    async loginUser() {
      console.log('loginUser method triggered')
      this.error = null
      try {
        const response = await axios.post('/api/auth/login/', {
          username: this.username,
          password: this.password,
        })
        const token = response.data.token
        localStorage.setItem('authToken', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        this.$router.push('/feed')
      } catch (err) {
        console.error('Login error:', err)
        this.error = 'Login failed. Please check your credentials.'
      }
    },
  },
}
</script>
