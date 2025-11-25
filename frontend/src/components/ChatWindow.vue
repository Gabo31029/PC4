<template>
  <div class="chat-window">
    <div v-if="!currentChat" class="no-chat">
      <p>Selecciona un chat para comenzar</p>
    </div>
    
    <div v-else class="chat-container">
      <div class="chat-header">
        <div class="chat-title">
          <h3>{{ getChatName(currentChat) }}</h3>
          <span v-if="isUserOnline(currentChat)" class="online-badge">En línea</span>
        </div>
        <button @click="startCall" class="call-btn">📞</button>
      </div>
      
      <div class="messages-container" ref="messagesContainer">
        <div 
          v-for="message in messages" 
          :key="message.id"
          :class="['message', { own: message.user_id === authStore.user?.id }]"
        >
          <div class="message-header">
            <span class="message-username">{{ message.username }}</span>
            <span class="message-time">{{ formatTime(message.created_at) }}</span>
          </div>
          <div class="message-content">
            <div v-if="message.message_type === 'text'">{{ message.content }}</div>
            <div v-else-if="message.message_type === 'audio'">
              <audio controls :src="getFileUrl(message.file_path)"></audio>
            </div>
            <div v-else-if="message.message_type === 'file'">
              <a :href="getFileUrl(message.file_path)" target="_blank" class="file-link">
                📎 {{ message.content || 'Archivo' }}
              </a>
            </div>
          </div>
        </div>
      </div>
      
      <MessageInput :chat-id="currentChat.id" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { useWebRTCStore } from '../stores/webrtc'
import MessageInput from './MessageInput.vue'

const chatStore = useChatStore()
const authStore = useAuthStore()
const webrtcStore = useWebRTCStore()

const messagesContainer = ref(null)

const currentChat = computed(() => chatStore.currentChat)
const messages = computed(() => chatStore.messages)

function getChatName(chat) {
  if (chat.type === 'group') {
    return chat.name || 'Grupo sin nombre'
  } else {
    return chat.other_user?.username || 'Usuario desconocido'
  }
}

function isUserOnline(chat) {
  if (chat.type === 'direct' && chat.other_user) {
    return chatStore.isUserOnline(chat.other_user.id)
  }
  return false
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

function getFileUrl(filePath) {
  if (!filePath) return ''
  return `/api/files/${filePath}`
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function startCall() {
  if (currentChat.value) {
    webrtcStore.startCall(currentChat.value.id, true)
  }
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

watch(currentChat, () => {
  scrollToBottom()
})

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #1a1a1a;
}

.no-chat {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #b0b0b0;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2a2a2a;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-title h3 {
  margin: 0;
  color: #e0e0e0;
  font-size: 18px;
}

.online-badge {
  font-size: 12px;
  color: #10b981;
}

.call-btn {
  padding: 8px 16px;
  font-size: 16px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  max-width: 70%;
  padding: 10px 15px;
  background-color: #2a2a2a;
  border-radius: 8px;
  align-self: flex-start;
}

.message.own {
  align-self: flex-end;
  background-color: #2563eb;
}

.message-header {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
  font-size: 12px;
}

.message-username {
  font-weight: 500;
  color: #b0b0b0;
}

.message.own .message-username {
  color: #e0e0e0;
}

.message-time {
  color: #808080;
}

.message-content {
  color: #e0e0e0;
  word-wrap: break-word;
}

.file-link {
  color: #e0e0e0;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.file-link:hover {
  text-decoration: underline;
}

audio {
  width: 100%;
  max-width: 300px;
}
</style>

