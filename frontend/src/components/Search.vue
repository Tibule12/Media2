<template>
  <div class="search-page">
    <h2>Search</h2>
    <input v-model="query" @input="performSearch" placeholder="Search users or posts..." />
    <div v-if="loading">Loading...</div>
    <div v-if="error" style="color:red">{{ error }}</div>
    <div v-if="results.length === 0 && query">No results found.</div>
    <ul>
      <li v-for="item in results" :key="item.id">
        <template v-if="item.type === 'user'">
          <router-link :to="`/profile/${item.username}`">User: {{ item.username }}</router-link>
        </template>
        <template v-else-if="item.type === 'post'">
          <router-link :to="`/post/${item.id}`">Post: {{ item.title }}</router-link>
        </template>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import debounce from 'lodash/debounce'

export default {
  data() {
    return {
      query: '',
      results: [],
      loading: false,
      error: null,
    }
  },
  methods: {
    performSearch: debounce(async function () {
      if (!this.query.trim()) {
        this.results = []
        return
      }
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/search/', {
          params: { q: this.query }
        })
        this.results = response.data
      } catch (err) {
        this.error = 'Search failed. Please try again.'
      } finally {
        this.loading = false
      }
    }, 300),
  },
}
</script>

<style scoped>
.search-page {
  max-width: 600px;
  margin: 0 auto;
}
.search-page input {
  width: 100%;
  padding: 8px;
  margin-bottom: 1em;
}
</style>
