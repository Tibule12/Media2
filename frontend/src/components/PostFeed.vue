<template>
  <div class="post-feed">
    <h2>Posts</h2>
    <router-link to="/create" class="create-post-button">Create New Post</router-link>

    <div class="filters" style="margin-bottom: 20px; display: flex; gap: 20px; align-items: center;">
      <label for="sort" style="font-weight: bold; color: #ff6f61;">Sort by:</label>
      <select id="sort" v-model="sortOrder" @change="fetchPosts" style="padding: 5px 10px; border-radius: 5px; border: 1px solid #ff6f61;">
        <option value="newest">Newest</option>
        <option value="oldest">Oldest</option>
        <option value="most_liked">Most Liked</option>
      </select>

      <label for="filter" style="font-weight: bold; color: #ff6f61;">Filter by author:</label>
      <input id="filter" v-model="authorFilter" @input="fetchPosts" placeholder="Author username" style="padding: 5px 10px; border-radius: 5px; border: 1px solid #ff6f61;" />
    </div>

    <div v-if="loading" class="loader-container">
      <div class="loader"></div>
      <p>Loading posts...</p>
    </div>

    <div v-else>
      <div v-if="posts.length === 0" class="no-posts">No posts yet.</div>
      <div v-for="post in posts" :key="post.id" class="post">
        <router-link :to="'/post/' + post.id" class="post-link">
          <h3>{{ post.author.username }}</h3>
          <p>{{ post.content }}</p>
          <div class="media-container">
            <template v-for="media in post.media" :key="media.id">
              <img v-if="media.media_type === 'image'" :src="getMediaUrl(media.file)" alt="Post image" class="post-image" loading="lazy" />
              <video v-else-if="media.media_type === 'video'" controls class="post-video" preload="metadata">
                <source :src="getMediaUrl(media.file)" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </template>
          </div>
        </router-link>
        <p>Likes: {{ post.likes ? post.likes.length : 0 }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig'

export default {
  data() {
    return {
      posts: [],
      sortOrder: 'newest',
      authorFilter: '',
      fetchTimeout: null,
      loading: false,
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
    },
    '$route'(to, from) {
      if (to.path === '/feed') {
        this.fetchPosts()
      }
    }
  },
  async created() {
    await this.fetchPosts()
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.fetchPosts()
      if (vm.$root.emitter) {
        vm.$root.emitter.on('postCreated', () => {
          setTimeout(() => {
            vm.fetchPosts()
          }, 500) // delay 500ms to allow backend to process
        })
      }
    })
  },
  methods: {
    getMediaUrl(file) {
      if (file.startsWith('http://') || file.startsWith('https://')) {
        return file
      }
      return `/media/${file}`
    },
    async fetchPosts() {
      this.loading = true
      try {
        const params = {}
        if (this.sortOrder) params.sort = this.sortOrder
        if (this.authorFilter) params.author = this.authorFilter
        const response = await axiosInstance.get('/api/posts/', { params })
        console.log('Fetched posts:', response.data)
        if (Array.isArray(response.data)) {
          this.posts = response.data
        } else if (response.data && response.data.results) {
          this.posts = response.data.results
        } else {
          this.posts = []
        }
      } catch (error) {
        console.error('Failed to load posts', error)
      } finally {
        this.loading = false
      }
    },
    async createPost(postData) {
      try {
        console.log('Creating post with data:', postData)
        const response = await axiosInstance.post('/api/posts/', postData)
        console.log('Post created:', response.data)
        this.$root.emitter.emit('postCreated')
      } catch (error) {
        console.error('Failed to create post', error)
      }
    }
  }
}
</script>

<style scoped>
.post {
  border: 1px solid #ff6f61;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 15px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  box-shadow: 0 6px 20px rgba(255, 105, 97, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 105, 97, 0.5);
}

.create-post-button {
  display: inline-block;
  margin-bottom: 20px;
  padding: 12px 30px;
  background-color: #ff6f61;
  color: white;
  border-radius: 30px;
  font-weight: 700;
  font-size: 1.2rem;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.create-post-button:hover {
  background-color: #ff3b2f;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
}

.media-container {
  margin-top: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.post-image, .post-video {
  border-radius: 12px;
  max-width: 100%;
  max-height: 300px;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
  transition: transform 0.3s ease;
}

.post-image:hover, .post-video:hover {
  transform: scale(1.05);
}
</style>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40px 0;
  color: #ff6f61;
  font-weight: 700;
  font-size: 1.2rem;
}

.loader {
  border: 6px solid #f3f3f3;
  border-top: 6px solid #ff6f61;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
