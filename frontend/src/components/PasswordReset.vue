<template>
  <div>
    <h2>Password Reset</h2>
    <form @submit.prevent="resetPassword">
      <div>
        <label>Email or Username:</label>
        <input v-model="identifier" required />
      </div>
      <button type="submit">Send Reset Link</button>
    </form>
    <p v-if="message" style="color:green">{{ message }}</p>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      identifier: '',
      message: null,
      error: null,
    }
  },
  methods: {
    async resetPassword() {
      this.message = null
      this.error = null
      try {
        await axios.post('/api/auth/password-reset/', {
          identifier: this.identifier,
        })
        this.message = 'If the account exists, a reset link has been sent.'
      } catch (err) {
        this.error = 'Failed to send reset link. Please try again.'
      }
    },
  },
}
</script>
