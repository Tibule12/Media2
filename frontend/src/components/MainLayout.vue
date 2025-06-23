<template>
  <div>
    <nav class="navbar">
      <router-link to="/" class="nav-logo">Tibule Media</router-link>
      <ul class="nav-links">
        <li><router-link to="/feed">Feed</router-link></li>
        <li><router-link to="/profile">Profile</router-link></li>
        <li><router-link to="/notifications">Notifications</router-link></li>
        <li><router-link to="/chat">Chat</router-link></li>
        <li><router-link to="/search">Search</router-link></li>
      </ul>
      <button class="logout-button" @click="$emit('logout')">Logout</button>
    </nav>
<main>
  <router-view></router-view>
</main>
  </div>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: #ff6f61;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.6);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.nav-logo {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  text-decoration: none;
  letter-spacing: 1.5px;
  user-select: none;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 25px;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: white;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 1.1rem;
}

.nav-links li a:hover {
  color: #ff3b2f;
  text-shadow: 0 0 5px rgba(255, 59, 47, 0.7);
}

.logout-button {
  background-color: transparent;
  border: 2px solid white;
  color: white;
  padding: 8px 18px;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
  user-select: none;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.5);
}

.logout-button:hover {
  background-color: white;
  color: #ff6f61;
  box-shadow: 0 6px 20px rgba(255, 59, 47, 0.7);
}
main {
  margin-top: 70px;
}
</style>
