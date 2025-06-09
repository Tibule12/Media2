<template>
  <div>
    <h2>Posts</h2>
    <router-link to="/create">Create New Post</router-link>
    <div v-if="posts.length === 0">No posts yet.</div>
    <div v-for="post in posts" :key="post.id" class="post">
      <router-link :to="'/post/' + post.id">
        <h3>{{ post.author.username }}</h3>
        <p>{{ post.content }}</p>
      </router-link>
      <p>Likes: {{ post.likes.length }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      posts: [],
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/posts/')
      this.posts = response.data
    } catch (error) {
      console.error('Failed to load posts', error)
    }
  },
}
</script>

<style>
.post {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
