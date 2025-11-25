<template>
  <div class="home-container">
    <ChatList />
    <ChatWindow />
    <CallWindow />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { useWebRTCStore } from '../stores/webrtc'
import socketService from '../services/socket'
import ChatList from '../components/ChatList.vue'
import ChatWindow from '../components/ChatWindow.vue'
import CallWindow from '../components/CallWindow.vue'

const authStore = useAuthStore()
const chatStore = useChatStore()
const webrtcStore = useWebRTCStore()

onMounted(() => {
  // Connect socket if authenticated
  if (authStore.isAuthenticated && authStore.token) {
    socketService.connect(authStore.token)
    
    // Setup store listeners
    chatStore.setupSocketListeners()
    webrtcStore.setupSocketListeners()
    
    // Load initial data
    chatStore.loadChats()
    
    // Get online users
    const token = localStorage.getItem('token')
    socketService.emit('get_online_users', { token })
  }
})

onUnmounted(() => {
  socketService.disconnect()
})
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
  width: 100%;
}
</style>

