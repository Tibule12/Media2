<template>
  <div>
    <nav class="navbar">
      <router-link to="/" class="nav-logo">Tibule Media</router-link>
      <button class="mobile-menu-button" @click="toggleMobileMenu" aria-label="Toggle menu">
        <span :class="{ 'bar': true, 'bar1': true, 'change': mobileMenuOpen }"></span>
        <span :class="{ 'bar': true, 'bar2': true, 'change': mobileMenuOpen }"></span>
        <span :class="{ 'bar': true, 'bar3': true, 'change': mobileMenuOpen }"></span>
      </button>
      <ul :class="['nav-links', { 'mobile-open': mobileMenuOpen }]">
        <li><router-link to="/feed" @click.native="closeMobileMenu">Feed</router-link></li>
        <li><router-link to="/profile" @click.native="closeMobileMenu">Profile</router-link></li>
        <li><router-link to="/notifications" @click.native="closeMobileMenu">Notifications</router-link></li>
        <li><router-link to="/chat" @click.native="closeMobileMenu">Chat</router-link></li>
        <li><router-link to="/search" @click.native="closeMobileMenu">Search</router-link></li>
        <li><router-link to="/story/create" @click.native="closeMobileMenu">Create Story</router-link></li>
      </ul>
      <button class="theme-toggle-button" @click="toggleTheme" :aria-label="`Switch to ${isDark ? 'light' : 'dark'} mode`">
        <span v-if="isDark">🌞</span>
        <span v-else>🌙</span>
      </button>
      <button class="logout-button" @click="logout">Logout</button>
    </nav>
    <Stories />
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import Stories from './Stories.vue'

export default {
  components: {
    Stories
  },
  data() {
    return {
      mobileMenuOpen: false,
      isDark: false,
    }
  },
  mounted() {
    // Initialize theme from localStorage or system preference
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      this.isDark = savedTheme === 'dark'
    } else {
      this.isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    this.applyTheme()
  },
  methods: {
    logout() {
      this.$router.push('/logout')
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    toggleTheme() {
      this.isDark = !this.isDark
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')
      this.applyTheme()
    },
    applyTheme() {
      if (this.isDark) {
        document.documentElement.classList.add('dark-theme')
      } else {
        document.documentElement.classList.remove('dark-theme')
      }
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: var(--color-primary);
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 6px 20px var(--color-shadow);
  font-family: var(--font-family-base);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.navbar:hover {
  box-shadow: 0 8px 25px var(--color-shadow-hover);
}

.nav-logo {
  font-size: 2.2rem;
  font-weight: 900;
  color: var(--color-text-light);
  text-decoration: none;
  letter-spacing: 1.8px;
  user-select: none;
  transition: color 0.3s ease;
}

.nav-logo:hover {
  color: var(--color-primary-dark);
  text-shadow: 0 0 8px var(--color-primary-dark);
}

.mobile-menu-button {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 28px;
  height: 22px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-right: 15px;
  z-index: 1100;
  transition: transform 0.3s ease;
}

.mobile-menu-button:hover {
  transform: scale(1.1);
}

.bar {
  width: 100%;
  height: 3px;
  background-color: var(--color-text-light);
  transition: 0.4s;
  border-radius: 2px;
}

.change.bar1 {
  transform: rotate(-45deg) translate(-5px, 6px);
}

.change.bar2 {
  opacity: 0;
}

.change.bar3 {
  transform: rotate(45deg) translate(-5px, -6px);
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 25px;
  margin: 0;
  padding: 0;
}

.nav-links.mobile-open {
  display: block;
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  background-color: var(--color-primary);
  padding: 20px 0;
  border-radius: 0 0 20px 20px;
  box-shadow: 0 6px 20px var(--color-shadow);
  font-size: 1.2rem;
  z-index: 1000;
  animation: slideDown 0.4s ease forwards;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.nav-links.mobile-open li {
  margin: 15px 0;
  text-align: center;
}

.nav-links li a {
  color: var(--color-text-light);
  font-weight: 700;
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 1.1rem;
}

.nav-links li a:hover {
  color: var(--color-primary-dark);
  text-shadow: 0 0 5px var(--color-primary-dark);
}

.theme-toggle-button {
  background: transparent;
  border: 2px solid var(--color-text-light);
  color: var(--color-text-light);
  padding: 6px 12px;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  margin-left: 10px;
  user-select: none;
  box-shadow: 0 4px 15px var(--color-shadow);
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}

.theme-toggle-button:hover {
  background-color: var(--color-text-light);
  color: var(--color-primary);
  box-shadow: 0 6px 20px var(--color-shadow-hover);
  transform: scale(1.05);
}

.logout-button {
  background-color: transparent;
  border: 2px solid var(--color-text-light);
  color: var(--color-text-light);
  padding: 8px 18px;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
  user-select: none;
  box-shadow: 0 4px 15px var(--color-shadow);
}

.logout-button:hover {
  background-color: var(--color-text-light);
  color: var(--color-primary);
  box-shadow: 0 6px 20px var(--color-shadow-hover);
  transform: scale(1.05);
}

main {
  margin-top: 70px;
  transition: margin-top 0.3s ease;
}

@media (max-width: 768px) {
  .mobile-menu-button {
    display: flex;
  }
  .nav-links {
    display: none;
  }
}
</style>
