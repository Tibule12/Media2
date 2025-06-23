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
  margin: 30px auto;
  padding: 20px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.user-profile h2 {
  margin-bottom: 20px;
  font-weight: 700;
  font-size: 2rem;
  color: #ff6f61;
}

.user-profile form div {
  margin-bottom: 1.5em;
}

.user-profile label {
  font-weight: 700;
  display: block;
  margin-bottom: 6px;
  color: #555;
}

.user-profile input[type="text"],
.user-profile textarea {
  width: 100%;
  padding: 10px;
  font-size: 1.1rem;
  border: 2px solid #ff6f61;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.user-profile input[type="text"]:focus,
.user-profile textarea:focus {
  border-color: #ff3b2f;
  outline: none;
}

.user-profile input[disabled] {
  background-color: #f0f0f0;
  color: #999;
  cursor: not-allowed;
}

.user-profile textarea {
  resize: vertical;
  min-height: 100px;
}

.user-profile img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 12px;
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
}

.user-profile button[type="submit"] {
  background-color: #ff6f61;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-weight: 700;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.user-profile button[type="submit"]:hover {
  background-color: #ff3b2f;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
}

.user-profile p {
  margin-top: 15px;
  font-weight: 600;
}

.user-profile p[style*="color: red"] {
  color: #d9534f;
}

.follow-button {
  margin-top: 1em;
  background-color: #ff6f61;
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 25px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.5);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.follow-button:hover {
  background-color: #ff3b2f;
  box-shadow: 0 8px 30px rgba(255, 59, 47, 0.7);
}
</style>
