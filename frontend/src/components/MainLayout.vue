<template>
  <div>
    <nav>
      <ul>
        <li><router-link to="/feed">Feed</router-link></li>
        <li><router-link to="/notifications">Notifications</router-link></li>
        <li><router-link to="/chat">Chat</router-link></li>
        <li><router-link to="/profile">Profile</router-link></li>
        <li><router-link to="/logout">Logout</router-link></li>
      </ul>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'MainLayout',
}
</script>

<style scoped>
nav {
  background-color: #333;
  padding: 1rem;
  position: relative;
  z-index: 1000;
}
nav ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
}
nav ul li {
}
nav ul li a {
  color: white;
  text-decoration: none;
  pointer-events: auto;
  cursor: pointer;
}
nav ul li a.router-link-exact-active {
  font-weight: bold;
  text-decoration: underline;
}
main {
  padding: 1rem;
  /* pointer-events: none; */
}
</style>
