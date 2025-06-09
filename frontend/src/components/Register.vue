<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div>
        <label>Username:</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Register</button>
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
    async register() {
      try {
        await axios.post('/api/auth/register/', {
          username: this.username,
          password: this.password,
        })
        this.$router.push('/login')
      } catch (err) {
        this.error = 'Registration failed. Please try again.'
      }
    },
  },
}
</script>
