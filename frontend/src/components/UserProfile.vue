<template>
  <div class="user-profile">
    <h2>User Profile</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label>Username:</label>
        <input v-model="user.username" disabled />
      </div>
      <div>
        <label>Full Name:</label>
        <input v-model="user.fullName" />
      </div>
      <div>
        <label>Bio:</label>
        <textarea v-model="user.bio"></textarea>
      </div>
      <div>
        <label>Profile Picture:</label>
        <input type="file" @change="onFileChange" />
        <img v-if="previewImage" :src="previewImage" alt="Profile Preview" style="max-width: 200px; max-height: 200px;" />
      </div>
      <button type="submit">Save</button>
    </form>
    <p v-if="message" style="color:green">{{ message }}</p>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: {
        username: '',
        fullName: '',
        bio: '',
        profilePicture: null,
        isFollowing: false,
      },
      previewImage: null,
      message: null,
      error: null,
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/users/me/')
      this.user = response.data
      // Fetch follow status if viewing another user's profile
      if (this.$route.params.username && this.$route.params.username !== this.user.username) {
        const followResp = await axios.get(`/api/users/${this.$route.params.username}/follow-status/`)
        this.user.isFollowing = followResp.data.isFollowing
      }
    } catch (err) {
      this.error = 'Failed to load user profile.'
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      this.user.profilePicture = file
      this.previewImage = URL.createObjectURL(file)
    },
    async updateProfile() {
      this.message = null
      this.error = null
      try {
        const formData = new FormData()
        formData.append('fullName', this.user.fullName)
        formData.append('bio', this.user.bio)
        if (this.user.profilePicture) {
          formData.append('profilePicture', this.user.profilePicture)
        }
        await axios.put('/api/users/me/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.message = 'Profile updated successfully.'
      } catch (err) {
        this.error = 'Failed to update profile.'
      }
    },
    async toggleFollow() {
      try {
        if (this.user.isFollowing) {
          await axios.post(`/api/users/${this.user.username}/unfollow/`)
          this.user.isFollowing = false
        } else {
          await axios.post(`/api/users/${this.user.username}/follow/`)
          this.user.isFollowing = true
        }
      } catch (err) {
        this.error = 'Failed to update follow status.'
      }
    }
  },
}
</script>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;
}
.user-profile form div {
  margin-bottom: 1em;
}
.follow-button {
  margin-top: 1em;
}
</style>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;
}
.user-profile form div {
  margin-bottom: 1em;
}
</style>
