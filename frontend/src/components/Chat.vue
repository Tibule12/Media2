<template>
  <div class="chat-container">
    <h2>Direct Messages</h2>
    <div class="conversations">
      <ul>
        <li v-for="conv in conversations" :key="conv.id" @click="selectConversation(conv)">
          {{ conv.participantName }}
        </li>
      </ul>
    </div>
    <div class="messages" v-if="selectedConversation">
      <ul>
        <li v-for="msg in messages" :key="msg.id">
          <strong>{{ msg.senderName }}:</strong> {{ msg.text }}
        </li>
      </ul>
      <form @submit.prevent="sendMessage">
        <input v-model="newMessage" placeholder="Type a message..." />
        <button type="submit">Send</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      conversations: [],
      selectedConversation: null,
      messages: [],
      newMessage: '',
      error: null,
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/chat/conversations/')
      this.conversations = response.data
    } catch (err) {
      this.error = 'Failed to load conversations.'
    }
  },
  methods: {
    async selectConversation(conv) {
      this.selectedConversation = conv
      try {
        const response = await axios.get(`/api/chat/conversations/${conv.id}/messages/`)
        this.messages = response.data
      } catch (err) {
        this.error = 'Failed to load messages.'
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim()) return
      try {
        const response = await axios.post(`/api/chat/conversations/${this.selectedConversation.id}/messages/`, {
          text: this.newMessage,
        })
        this.messages.push(response.data)
        this.newMessage = ''
      } catch (err) {
        this.error = 'Failed to send message.'
      }
    },
  },
}
</script>

<style scoped>
.chat-container {
  display: flex;
  max-width: 800px;
  margin: 0 auto;
}
.conversations {
  width: 30%;
  border-right: 1px solid #ccc;
}
.conversations ul {
  list-style: none;
  padding: 0;
}
.conversations li {
  padding: 10px;
  cursor: pointer;
}
.conversations li:hover {
  background-color: #eee;
}
.messages {
  width: 70%;
  padding: 10px;
}
.messages ul {
  list-style: none;
  padding: 0;
  max-height: 400px;
  overflow-y: auto;
}
.messages li {
  margin-bottom: 10px;
}
form {
  display: flex;
}
input {
  flex-grow: 1;
  padding: 5px;
}
button {
  padding: 5px 10px;
}
</style>
