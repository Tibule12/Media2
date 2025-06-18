<template>
  <div class="post-feed">
    <h2>Posts</h2>
    <router-link to="/create" class="create-post-button">Create New Post</router-link>

    <div class="filters">
      <label for="sort">Sort by:</label>
      <select id="sort" v-model="sortOrder" @change="fetchPosts">
        <option value="newest">Newest</option>
        <option value="oldest">Oldest</option>
        <option value="most_liked">Most Liked</option>
      </select>

      <label for="filter">Filter by author:</label>
      <input id="filter" v-model="authorFilter" @input="fetchPosts" placeholder="Author username" />
    </div>

    <div v-if="posts.length === 0" class="no-posts">No posts yet.</div>
    <div v-for="post in posts" :key="post.id" class="post">
      <router-link :to="'/post/' + post.id" class="post-link">
        <h3>{{ post.author.username }}</h3>
        <p>{{ post.content }}</p>
        <div class="media-container">
          <template v-for="media in post.media" :key="media.id">
            <img v-if="media.media_type === 'image'" :src="media.file" alt="Post image" class="post-image" />
            <video v-else-if="media.media_type === 'video'" controls class="post-video">
              <source :src="media.file" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </template>
        </div>
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
      sortOrder: 'newest',
      authorFilter: '',
      fetchTimeout: null,
    }
  },
  watch: {
    sortOrder() {
      this.fetchPosts()
    },
    authorFilter() {
      if (this.fetchTimeout) clearTimeout(this.fetchTimeout)
      this.fetchTimeout = setTimeout(() => {
        this.fetchPosts()
      }, 300)
    }
  },
  async created() {
    await this.fetchPosts()
  },
  methods: {
    async fetchPosts() {
      try {
        const params = {}
        if (this.sortOrder) params.sort = this.sortOrder
        if (this.authorFilter) params.author = this.authorFilter
        const response = await axios.get('/api/posts/', { params })
        this.posts = response.data
      } catch (error) {
        console.error('Failed to load posts', error)
      }
    }
  }
}
</script>

<style>
.post {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
