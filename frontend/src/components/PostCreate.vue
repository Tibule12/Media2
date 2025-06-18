<template>
  <div>
    <h2>Create Post</h2>
    <form @submit.prevent="createPost" enctype="multipart/form-data">
      <textarea v-model="content" placeholder="What's on your mind?" required></textarea>
      <br />
      <input type="file" @change="onFileChange" multiple />
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
      files: [],
      error: null,
    }
  },
  methods: {
    onFileChange(event) {
      this.files = Array.from(event.target.files)
    },
    async createPost() {
      try {
        const formData = new FormData()
        formData.append('content', this.content)
        this.files.forEach((file, index) => {
          formData.append(`media_${index}`, file)
        })
        const token = localStorage.getItem('token')
        await axios.post('/api/posts/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${token}`,
          },
        })
        this.$router.push('/feed')
      } catch (err) {
        console.error('Create post error:', err)
        this.error = 'Failed to create post.'
      }
    },
  },
}
</script>
