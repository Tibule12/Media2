<template>
  <div class="search">
    <input type="text" v-model="query" @input="onInput" placeholder="Search users, posts, hashtags, mentions..." />
    <ul v-if="results.length > 0" class="results-list">
      <li v-for="result in results" :key="result.type + '-' + result.id" @click="selectResult(result)">
        <span v-if="result.type === 'user'">User: {{ result.username }}</span>
        <span v-else-if="result.type === 'post'">Post: {{ result.title }}</span>
        <span v-else-if="result.type === 'hashtag'">Hashtag: {{ result.tag }}</span>
        <span v-else-if="result.type === 'mention'">Mention: {{ result.username }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      query: '',
      results: [],
    }
  },
  methods: {
    async onInput() {
      if (this.query.length < 3) {
        this.results = []
        return
      }
      try {
        const response = await axios.get('/api/search/', { params: { q: this.query } })
        this.results = response.data
      } catch (error) {
        console.error('Search failed', error)
      }
    },
    selectResult(result) {
      if (result.type === 'user') {
        this.$router.push(`/profile/${result.username}`)
      } else if (result.type === 'post') {
        this.$router.push(`/post/${result.id}`)
      } else if (result.type === 'hashtag') {
        this.$router.push(`/search?tag=${result.tag}`)
      } else if (result.type === 'mention') {
        this.$router.push(`/profile/${result.username}`)
      }
    }
  }
}
</script>

<style scoped>
.search {
  max-width: 600px;
  margin: 20px auto;
}
.search input {
  width: 100%;
  padding: 10px;
  font-size: 1.1rem;
  border: 2px solid #ff6f61;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}
.search input:focus {
  border-color: #ff3b2f;
  outline: none;
}
.results-list {
  list-style: none;
  padding: 0;
  margin-top: 10px;
  border: 1px solid #ff6f61;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
}
.results-list li {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.results-list li:hover {
  background-color: #ff6f61;
  color: white;
}
</style>
