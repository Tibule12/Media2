<template>
  <div class="stories">
    <h2>Stories</h2>
    <div v-if="stories.length === 0">No stories available.</div>
    <div class="story-list">
      <div v-for="story in stories" :key="story.id" class="story" @click="viewStory(story)">
        <img :src="story.media" alt="Story media" class="story-thumbnail" />
        <p>{{ story.author.username }}</p>
      </div>
    </div>
    <div v-if="activeStory" class="story-viewer" @click="closeStory">
      <video v-if="isVideo(activeStory.media)" controls autoplay>
        <source :src="activeStory.media" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <img v-else :src="activeStory.media" alt="Story media" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      stories: [],
      activeStory: null,
    }
  },
  async created() {
    await this.fetchStories()
  },
  methods: {
    async fetchStories() {
      try {
        const response = await axios.get('/api/stories/')
        // Filter out expired stories
        const now = new Date()
        this.stories = response.data.filter(story => new Date(story.expires_at) > now)
      } catch (error) {
        console.error('Failed to load stories', error)
      }
    },
    viewStory(story) {
      this.activeStory = story
    },
    closeStory() {
      this.activeStory = null
    },
    isVideo(mediaUrl) {
      return mediaUrl.endsWith('.mp4') || mediaUrl.endsWith('.webm') || mediaUrl.endsWith('.ogg')
    }
  }
}
</script>

<style>
.stories {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 20px;
}
.story-list {
  display: flex;
  gap: 10px;
}
.story {
  cursor: pointer;
  text-align: center;
}
.story-thumbnail {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
}
.story-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}
.story-viewer img,
.story-viewer video {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}
</style>
