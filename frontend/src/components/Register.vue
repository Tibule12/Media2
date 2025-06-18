<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div>
        <label>Username:</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Name:</label>
        <input v-model="first_name" required />
      </div>
      <div>
        <label>Surname:</label>
        <input v-model="last_name" required />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Birthday:</label>
        <input type="date" v-model="birthday" />
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
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      birthday: '',
      password: '',
      error: null,
    }
  },
  methods: {
    ...mapActions(['login']),
    async registerUser() {
      this.error = null
      try {
        await axios.post('/api/auth/register/', {
          username: this.username,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          birthday: this.birthday || null,
          password: this.password,
        })
        // Automatically login after registration
        await this.login({ username: this.username, password: this.password })
        this.$router.push('/')
        } catch (err) {
          if (err.response && err.response.data && err.response.data) {
            // Format and display detailed validation errors
            const errors = err.response.data
            this.error = Object.entries(errors).map(function([field, msgs]) {
              return field + ": " + (Array.isArray(msgs) ? msgs.join(", ") : msgs);
            }).join("; ")
          } else {
            this.error = 'Registration failed. Please try again.'
          }
        }
      },
  },
}
</script>
