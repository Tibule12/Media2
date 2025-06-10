<template>
  <div class="notifications">
    <h2>Notifications</h2>
    <ul>
      <li v-for="notification in notifications" :key="notification.id" :class="{ unread: !notification.read }">
        <p>{{ notification.message }}</p>
        <small>{{ new Date(notification.timestamp).toLocaleString() }}</small>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      notifications: [],
      error: null,
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/notifications/')
      this.notifications = response.data
    } catch (err) {
      this.error = 'Failed to load notifications.'
    }
  },
}
</script>

<style scoped>
.notifications {
  max-width: 600px;
  margin: 0 auto;
}
.notifications ul {
  list-style: none;
  padding: 0;
}
.notifications li {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}
.notifications li.unread {
  background-color: #eef;
  font-weight: bold;
}
</style>
