ord<template>
  <div class="auth-container">
    <div class="auth-content">
      <h1>Login</h1>
      <form @submit.prevent="loginUser">
        <input v-model="email" type="email" placeholder="Email" required autocomplete="email" />
        <input v-model="password" type="password" placeholder="Password" required autocomplete="current-password" />
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <div style="margin-top: 20px; display: flex; justify-content: center; gap: 15px;">
        <button class="btn btn-secondary" @click="$router.push('/register')">Signup</button>
        <button class="btn btn-secondary" @click="$router.push('/password-reset')">Forgot Password</button>
      </div>
      <p v-if="error" class="error-message">{{ formattedError }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
    }
  },
  computed: {
    formattedError() {
      if (!this.error) return ''
      if (typeof this.error === 'string') return this.error
      try {
        return JSON.stringify(this.error)
      } catch {
        return String(this.error)
      }
    }
  },
  watch: {
    error(newVal) {
      console.log('Error value changed:', newVal)
    }
  },
  methods: {
    ...mapActions(['login']),
    async loginUser() {
      this.error = null
      try {
        await this.login({ email: this.email.trim(), password: this.password })
        this.$router.push('/')
      } catch (err) {
        if (err.response && err.response.data) {
          console.log('Login error response:', err.response.data);
          const errors = err.response.data
          this.error = Object.entries(errors).map(function([field, msgs]) {
            return field + ": " + (Array.isArray(msgs) ? msgs.join(", ") : msgs);
          }).join("; ")
        } else {
          this.error = 'Login failed. Please try again.'
        }
      }
    },
  },
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  color: #fff;
  padding: 20px;
}

.auth-content {
  max-width: 400px;
  background: rgba(255, 111, 97, 0.85);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
  animation: fadeInScale 1s ease forwards;
}

h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 900;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

input {
  width: 100%;
  padding: 12px 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  border: none;
  font-size: 1rem;
}

button.btn {
  width: 100%;
  padding: 15px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff6f61;
  background: #fff;
  border-radius: 50px;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

button.btn:hover {
  background-color: #ff3b2f;
  color: #fff;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
  cursor: pointer;
}

button.btn-secondary {
  width: 100%;
  padding: 14px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ff6f61;
  background: transparent;
  border: 2px solid #ff6f61;
  border-radius: 50px;
  box-shadow: none;
  transition: background-color 0.3s ease, color 0.3s ease;
  cursor: pointer;
  margin-top: 12px;
}

button.btn-secondary:hover {
  background-color: #ff6f61;
  color: #fff;
}

.error-message {
  color: #ff3b2f;
  margin-top: 10px;
  font-weight: 700;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.auth-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.auth-buttons .btn {
  width: 48%;
  padding: 10px;
  font-size: 1rem;
  font-weight: 600;
  color: #ff6f61;
  background: #fff;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.auth-buttons .btn:hover {
  background-color: #ff3b2f;
  color: #fff;
}
</style>
