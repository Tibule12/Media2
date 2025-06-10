<template>
  <div class="welcome-page">
    <h1>Welcome to Tibule Media App</h1>
    <p>Please login or create an account to continue.</p>
    <router-link to="/login" class="btn">Login</router-link>
    <router-link to="/register" class="btn">Create Account</router-link>
  </div>
</template>

<script>
export default {
  name: 'Welcome',
}
</script>

<style scoped>
.welcome-page {
  max-width: 400px;
  margin: 100px auto;
  text-align: center;
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
}

.btn {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
