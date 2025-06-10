<template>
  <div>
    <h2>Post Detail</h2>
    <div v-if="post">
      <h3>{{ post.author.username }}</h3>
      <p>{{ post.content }}</p>

      <div v-if="post.media && post.media.length">
        <h4>Media</h4>
        <div v-for="mediaItem in post.media" :key="mediaItem.id" class="media-item">
          <img v-if="mediaItem.type.startsWith('image/')" :src="mediaItem.url" alt="Post media" style="max-width: 100%; max-height: 400px;" />
          <video v-else-if="mediaItem.type.startsWith('video/')" controls style="max-width: 100%; max-height: 400px;">
            <source :src="mediaItem.url" :type="mediaItem.type" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>

      <p>Likes: {{ post.likes.length }}</p>
      <button @click="toggleLike">{{ liked ? 'Unlike' : 'Like' }}</button>

      <h4>Comments</h4>
      <div v-for="comment in post.comments" :key="comment.id" class="comment">
        <p><strong>{{ comment.author.username }}:</strong> {{ comment.content }}</p>
      </div>

      <form @submit.prevent="addComment">
        <input v-model="newComment" placeholder="Add a comment" required />
        <button type="submit">Comment</button>
      </form>
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['id'],
  data() {
    return {
      post: null,
      newComment: '',
      liked: false,
    }
  },
  async created() {
    await this.fetchPost()
  },
  methods: {
    async fetchPost() {
      try {
        const response = await axios.get(`/api/posts/${this.id}/`)
        this.post = response.data
        this.liked = this.post.likes.some(like => like.user.username === this.$root.$data.username)
      } catch (error) {
        console.error('Failed to load post', error)
      }
    },
    async toggleLike() {
      try {
        const response = await axios.post(`/api/posts/${this.id}/like/`)
        this.liked = !this.liked
        await this.fetchPost()
      } catch (error) {
        console.error('Failed to toggle like', error)
      }
    },
    async addComment() {
      try {
        await axios.post('/api/comments/', {
          post: this.id,
          content: this.newComment,
        })
        this.newComment = ''
        await this.fetchPost()
      } catch (error) {
        console.error('Failed to add comment', error)
      }
    },
  },
}
</script>

<style>
.comment {
  border-top: 1px solid #ccc;
  padding: 5px 0;
}
</style>
