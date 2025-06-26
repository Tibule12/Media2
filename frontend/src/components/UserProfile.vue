<template>
  <div class="profile-page">
    <div class="cover-photo" v-if="coverPhoto" :style="{ backgroundImage: 'url(' + coverPhoto + ')' }"></div>
    <div class="profile-header">
      <img
        v-if="profilePicture"
        :src="profilePicture"
        alt="Profile Picture"
        class="profile-picture"
        @error="onImageError"
      />
      <img
        v-else
        :src="defaultProfileImage"
        alt="Default Profile Picture"
        class="profile-picture"
      />
      <div class="profile-info">
        <h2 class="profile-name">{{ fullName }}</h2>
        <button class="follow-button" @click="toggleFollow">
          {{ isFollowing ? 'Unfollow' : 'Follow' }}
        </button>
        <p class="profile-bio" v-if="bio">{{ bio }}</p>
        <div class="upload-profile-picture">
          <input type="file" @change="onProfilePictureChange" accept="image/*" />
          <button @click="uploadProfilePicture" :disabled="!newProfilePicture">Upload</button>
          <p v-if="uploadMessage" :class="{ success: uploadSuccess, error: !uploadSuccess }">{{ uploadMessage }}</p>
        </div>
        <div class="profile-stats">
          <div class="stat">
            <span class="stat-number">{{ photosCount }}</span>
            <span class="stat-label">Photos</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ followersCount }}</span>
            <span class="stat-label">Followers</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ followsCount }}</span>
            <span class="stat-label">Follows</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="storyHighlights && storyHighlights.length" class="story-highlights">
      <h3>Story Highlights</h3>
      <div class="highlights-list">
        <div v-for="story in storyHighlights" :key="story.id" class="highlight-item">
          <img :src="story.media" alt="Story Highlight" />
        </div>
      </div>
    </div>

    <div class="tabs">
      <button :class="{ active: activeTab === 'posts' }" @click="activeTab = 'posts'">Posts</button>
      <button :class="{ active: activeTab === 'videos' }" @click="activeTab = 'videos'">Videos</button>
      <button :class="{ active: activeTab === 'tagged' }" @click="activeTab = 'tagged'">Tagged</button>
    </div>

    <div v-if="activeTab === 'posts' && photos.length > 0" class="photo-grid">
      <div v-for="photo in photos" :key="photo.id" class="photo-item">
        <img :src="photo.file" alt="User Photo" />
      </div>
    </div>
    <div v-else-if="activeTab === 'videos'" class="video-grid" v-if="videos.length > 0">
      <div v-for="video in videos" :key="video.id" class="video-item">
        <video controls :src="video.file"></video>
      </div>
    </div>
    <div v-else-if="activeTab === 'tagged'" class="tagged-grid" v-if="tagged.length > 0">
      <div v-for="item in tagged" :key="item.id" class="tagged-item">
        <img :src="item.file" alt="Tagged Content" />
      </div>
    </div>
    <div v-else class="no-content-message">
      No content available.
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig'

export default {
  data() {
    return {
      fullName: '',
      profilePicture: '',
      coverPhoto: '',
      bio: '',
      photosCount: 0,
      followersCount: 0,
      followsCount: 0,
      photos: [],
      videos: [],
      tagged: [],
      storyHighlights: [],
      activeTab: 'posts',
      isFollowing: false,
      loadingProfile: true,
      loadingContent: true,
      errorProfile: null,
      errorContent: null,
      defaultProfileImage: '/default-profile.png',
    }
  },
  async created() {
    await this.fetchUserProfile()
    await this.fetchUserContent()
  },
  data() {
    return {
      newProfilePicture: null,
      uploadMessage: '',
      uploadSuccess: false,
    }
  },
  methods: {
    async fetchUserProfile() {
      this.loadingProfile = true
      this.errorProfile = null
      try {
        const response = await axiosInstance.get('/api/users/me/')
        const profile = response.data.profile || {}
        this.fullName = profile.fullName || response.data.first_name + ' ' + response.data.last_name
        this.profilePicture = profile.profilePicture || ''
        this.coverPhoto = profile.coverPhoto || ''
        this.bio = profile.bio || ''
        this.photosCount = response.data.photos_count || 0
        this.followersCount = response.data.followers_count || 0
        this.followsCount = response.data.follows_count || 0
        this.isFollowing = response.data.is_following || false
        this.storyHighlights = response.data.story_highlights || []
      } catch (error) {
        this.errorProfile = 'Failed to fetch user profile.'
        console.error('Failed to fetch user profile:', error)
      } finally {
        this.loadingProfile = false
      }
    },
    async fetchUserContent() {
      this.loadingContent = true
      this.errorContent = null
      try {
        // Fetch posts
        const postsResponse = await axiosInstance.get('/api/posts/?author=' + this.$route.params.username)
        this.photos = postsResponse.data.filter(post => post.media.length > 0 && post.media[0].media_type === 'image').map(post => post.media[0])
        this.videos = postsResponse.data.filter(post => post.media.length > 0 && post.media[0].media_type === 'video').map(post => post.media[0])
        // Fetch tagged content - placeholder, implement as needed
        this.tagged = []
      } catch (error) {
        this.errorContent = 'Failed to fetch user content.'
        console.error('Failed to fetch user content:', error)
      } finally {
        this.loadingContent = false
      }
    },
    toggleFollow() {
      this.isFollowing = !this.isFollowing
      // Implement follow/unfollow API call here
    },
    onImageError(event) {
      event.target.src = '/default-profile.png'
    },
    onProfilePictureChange(event) {
      console.log('File selected')
      const file = event.target.files[0]
      if (file) {
        this.newProfilePicture = file
      }
    },
    async uploadProfilePicture() {
      console.log('Upload button clicked')
      if (!this.newProfilePicture) {
        this.uploadMessage = 'Please select a profile picture to upload.'
        this.uploadSuccess = false
        return
      }
      const formData = new FormData()
      formData.append('profilePicture', this.newProfilePicture)
      try {
        const response = await axiosInstance.put('/api/users/me/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.profilePicture = response.data.profile.profilePicture
        this.uploadMessage = 'Profile picture updated successfully.'
        this.uploadSuccess = true
        this.newProfilePicture = null
      } catch (error) {
        this.uploadMessage = 'Failed to upload profile picture.'
        this.uploadSuccess = false
        console.error('Profile picture upload error:', error)
      }
    },
  },
}
</script>

<style scoped>
.profile-page {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.cover-photo {
  width: 100%;
  height: 200px;
  background-size: cover;
  background-position: center;
  border-radius: 20px 20px 0 0;
  margin-bottom: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ff6f61;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.6);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-weight: 900;
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.follow-button {
  background-color: #ff6f61;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}

.follow-button:hover {
  background-color: #ff3b2f;
}

.profile-bio {
  font-size: 1rem;
  color: #666;
  margin-bottom: 20px;
}

.profile-stats {
  display: flex;
  gap: 30px;
}

.stat {
  text-align: center;
}

.stat-number {
  font-weight: 700;
  font-size: 1.4rem;
  color: #ff6f61;
}

.stat-label {
  font-size: 0.9rem;
  color: #999;
}

.story-highlights {
  margin-bottom: 20px;
}

.highlights-list {
  display: flex;
  gap: 15px;
}

.highlight-item img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ff6f61;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.highlight-item img:hover {
  transform: scale(1.1);
}

.tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.tabs button {
  background: none;
  border: none;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  padding-bottom: 5px;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: color 0.3s ease, border-color 0.3s ease;
}

.tabs button.active {
  color: #ff6f61;
  border-color: #ff6f61;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.photo-item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.3);
  transition: transform 0.3s ease;
}

.photo-item img:hover {
  transform: scale(1.05);
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.video-item video {
  width: 100%;
  height: 100px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.3);
  transition: transform 0.3s ease;
}

.video-item video:hover {
  transform: scale(1.05);
}

.tagged-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.tagged-item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.3);
  transition: transform 0.3s ease;
}

.tagged-item img:hover {
  transform: scale(1.05);
}

.no-content-message {
  text-align: center;
  color: #999;
  font-weight: 700;
  font-size: 1.2rem;
}

@media (max-width: 600px) {
  .profile-page {
    max-width: 90%;
    margin: 20px auto;
    padding: 15px;
  }
  .photo-item img,
  .video-item video,
  .tagged-item img {
    height: 80px;
  }
}
</style>
