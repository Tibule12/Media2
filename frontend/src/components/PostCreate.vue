<template>
  <div>
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
      <textarea v-model="content" placeholder="What's on your mind?" required></textarea>
      <br />
      <button type="submit">Post</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      content: '',
      error: null,
    }
  },
  methods: {
    async createPost() {
      try {
        await axios.post('/api/posts/', { content: this.content })
        this.$router.push('/')
      } catch (err) {
        this.error = 'Failed to create post.'
      }
    },
  },
}
</script>
