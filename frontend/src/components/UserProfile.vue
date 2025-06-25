<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    <p v-if="!profile.fullName && !profile.bio && !profilePicturePreview" class="loading-message">Loading profile...</p>
    <form @submit.prevent="updateProfile" enctype="multipart/form-data">
      <div class="form-group">
        <label for="fullName">Full Name</label>
        <input id="fullName" v-model="profile.fullName" type="text" placeholder="Full Name" />
      </div>
      <div class="form-group">
        <label for="bio">Bio</label>
        <textarea id="bio" v-model="profile.bio" placeholder="Tell us about yourself"></textarea>
      </div>
      <div class="form-group">
        <label for="profilePicture">Profile Picture</label>
        <input id="profilePicture" type="file" @change="onFileChange" />
        <div v-if="profilePicturePreview" class="preview">
          <img :src="profilePicturePreview" alt="Profile Picture Preview" />
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Save Profile</button>
      <p v-if="message" class="success-message">{{ message }}</p>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig'

export default {
  data() {
    return {
      profile: {
        fullName: '',
        bio: '',
        profilePicture: null,
      },
      profilePicturePreview: null,
      message: '',
      error: '',
    }
  },
  async created() {
    await this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      this.error = ''
      try {
        const response = await axiosInstance.get('/api/users/me/')
        this.profile.fullName = response.data.profile?.fullName || ''
        this.profile.bio = response.data.profile?.bio || ''
        this.profilePicturePreview = response.data.profile?.profilePicture || null
      } catch (err) {
        this.error = 'Failed to load profile. Please login again.'
      }
    },
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.profile.profilePicture = file
        this.profilePicturePreview = URL.createObjectURL(file)
      }
    },
    async updateProfile() {
      this.error = ''
      this.message = ''
      try {
        const formData = new FormData()
        formData.append('fullName', this.profile.fullName)
        formData.append('bio', this.profile.bio)
        if (this.profile.profilePicture instanceof File) {
          formData.append('profilePicture', this.profile.profilePicture)
        }
        const response = await axiosInstance.put('/api/users/me/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.message = 'Profile updated successfully.'
        this.profilePicturePreview = response.data.profile?.profilePicture || this.profilePicturePreview
      } catch (err) {
        this.error = 'Failed to update profile.'
      }
    },
  },
}
</script>

<style scoped>
.profile-container {
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

input[type="text"],
textarea {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: none;
  font-size: 1rem;
  resize: vertical;
}

textarea {
  min-height: 100px;
}

input[type="file"] {
  color: #fff;
}

.preview img {
  margin-top: 10px;
  max-width: 150px;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.6);
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
