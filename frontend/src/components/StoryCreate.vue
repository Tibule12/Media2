<template>
  <div class="story-create-container">
    <h1>Create Story</h1>
    <form @submit.prevent="submitStory" enctype="multipart/form-data">
      <div class="form-group">
        <label for="media">Upload Media (Image or Video)</label>
        <input id="media" type="file" @change="onFileChange" accept="image/*,video/*" required />
      </div>
      <div v-if="mediaPreview" class="media-preview">
        <video v-if="isVideo(mediaPreview)" controls autoplay muted loop>
          <source :src="mediaPreview" />
          Your browser does not support the video tag.
        </video>
        <img v-else :src="mediaPreview" alt="Media Preview" />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="!mediaFile">Post Story</button>
      <p v-if="message" class="success-message">{{ message }}</p>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
    <Stories />
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig'
import Stories from './Stories.vue'

export default {
  components: {
    Stories
  },
  data() {
    return {
      mediaFile: null,
      mediaPreview: null,
      message: '',
      error: '',
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.mediaFile = file
        this.mediaPreview = URL.createObjectURL(file)
      }
    },
    isVideo(url) {
      return url.endsWith('.mp4') || url.endsWith('.webm') || url.endsWith('.ogg')
    },
    async submitStory() {
      this.error = ''
      this.message = ''
      if (!this.mediaFile) {
        this.error = 'Please select a media file to upload.'
        return
      }
      try {
        const formData = new FormData()
        formData.append('media', this.mediaFile)
        // Set expires_at to 24 hours from now
        const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
        formData.append('expires_at', expiresAt)

        await axiosInstance.post('/api/stories/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.message = 'Story posted successfully.'
        this.mediaFile = null
        this.mediaPreview = null
      } catch (err) {
        this.error = 'Failed to post story. Please try again.'
      }
    },
  },
}
</script>

<style scoped>
.story-create-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: rgba(255, 111, 97, 0.85);
  border-radius: 15px;
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 900;
  font-size: 2.5rem;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 700;
}

input[type="file"] {
  color: #fff;
}

.media-preview {
  margin-top: 15px;
  text-align: center;
}

.media-preview img,
.media-preview video {
  max-width: 100%;
  max-height: 300px;
  border-radius: 10px;
}

button.btn-primary {
  width: 100%;
  padding: 15px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff6f61;
  background: #fff;
  border-radius: 50px;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
}

button.btn-primary:hover {
  background-color: #ff3b2f;
  color: #fff;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
}

.success-message {
  margin-top: 15px;
  color: #a6f0a6;
  font-weight: 700;
  text-align: center;
}

.error-message {
  margin-top: 15px;
  color: #ff3b2f;
  font-weight: 700;
  text-align: center;
}
</style>
