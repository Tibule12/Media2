<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
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

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    }
  },
  methods: {
    async login() {
      try {
        // For simplicity, using session authentication
        await axios.post('/api/auth/login/', {
          username: this.username,
          password: this.password,
        })
        this.$router.push('/')
      } catch (err) {
        this.error = 'Login failed. Please check your credentials.'
      }
    },
  },
}
</script>
