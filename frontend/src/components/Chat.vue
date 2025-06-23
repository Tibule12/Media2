<template>
  <div class="chat-container">
    <h2>Direct Messages</h2>
    <div class="conversations">
      <ul>
        <li v-for="conv in conversations" :key="conv.id" @click="selectConversation(conv)" :class="{ selected: selectedConversation && selectedConversation.id === conv.id }">
          {{ conv.participantName }}
          <span v-if="hasUnread(conv.id)" class="unread-indicator">•</span>
        </li>
      </ul>
    </div>
    <div class="messages" v-if="selectedConversation">
      <ul>
        <li v-for="msg in messages" :key="msg.id" :class="{ 'my-message': msg.sender === currentUserId }">
          <strong>{{ msg.senderName }}:</strong> {{ msg.content }}
          <span v-if="msg.read" class="read-receipt">✓</span>
        </li>
      </ul>
      <form @submit.prevent="sendMessage">
        <input v-model="newMessage" placeholder="Type a message..." @input="notifyTyping" />
        <button type="submit">Send</button>
      </form>
      <div v-if="typingIndicator" class="typing-indicator">{{ typingIndicator }}</div>
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
      currentUserId: null,
      typingIndicator: '',
      typingTimeout: null,
      unreadMessages: {}, // { conversationId: boolean }
    }
  },
  async created() {
    try {
      const userResponse = await axios.get('/api/users/me/')
      this.currentUserId = userResponse.data.id
      const response = await axios.get('/api/chat/conversations/')
      this.conversations = response.data
      // Initialize unread messages state
      this.conversations.forEach(conv => {
        this.unreadMessages[conv.id] = false
      })
    } catch (err) {
      this.error = 'Failed to load conversations.'
    }
  },
  methods: {
    async selectConversation(conv) {
      this.selectedConversation = conv
      this.unreadMessages[conv.id] = false
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
          content: this.newMessage,
        })
        this.messages.push(response.data)
        this.newMessage = ''
      } catch (err) {
        this.error = 'Failed to send message.'
      }
    },
    hasUnread(conversationId) {
      return this.unreadMessages[conversationId]
    },
    notifyTyping() {
      this.typingIndicator = 'Typing...'
      clearTimeout(this.typingTimeout)
      this.typingTimeout = setTimeout(() => {
        this.typingIndicator = ''
      }, 2000)
    }
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
  position: relative;
}
.conversations li.selected {
  background-color: #ff6f61;
  color: white;
}
.unread-indicator {
  color: #ff3b2f;
  font-size: 1.5rem;
  position: absolute;
  right: 10px;
  top: 8px;
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
.messages li.my-message {
  text-align: right;
  font-weight: 700;
}
.read-receipt {
  margin-left: 10px;
  color: #4caf50;
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
.typing-indicator {
  font-style: italic;
  color: #999;
  margin-top: 5px;
}
</style>
