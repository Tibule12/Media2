<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1>Welcome to Tibule Media</h1>
      <p>Your ultimate social media platform to connect, share, and explore.</p>
      <router-link to="/register" class="btn btn-primary">Get Started</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Welcome'
}
</script>

<style scoped>
.welcome-container {
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

.welcome-content {
  max-width: 600px;
  background: rgba(255, 111, 97, 0.85);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
  animation: fadeInScale 1s ease forwards;
}

h1 {
  font-size: 3.5rem;
  margin-bottom: 20px;
  font-weight: 900;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

p {
  font-size: 1.5rem;
  margin-bottom: 30px;
  font-weight: 600;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.btn {
  display: inline-block;
  padding: 15px 40px;
  font-size: 1.3rem;
  font-weight: 700;
  color: #ff6f61;
  background: #fff;
  border-radius: 50px;
  text-decoration: none;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
}

.btn:hover {
  background-color: #ff3b2f;
  color: #fff;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
  cursor: pointer;
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
</style>
