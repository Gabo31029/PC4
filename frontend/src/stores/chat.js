import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'
import socketService from '../services/socket'

export const useChatStore = defineStore('chat', () => {
  const chats = ref([])
  const currentChat = ref(null)
  const messages = ref([])
  const onlineUsers = ref(new Set())

  function setChats(newChats) {
    chats.value = newChats
  }

  function addChat(chat) {
    const exists = chats.value.find(c => c.id === chat.id)
    if (!exists) {
      chats.value.push(chat)
    }
  }

  function setCurrentChat(chat) {
    currentChat.value = chat
    if (chat) {
      socketService.joinChat(chat.id)
      loadMessages(chat.id)
    }
  }

  function addMessage(message) {
    if (message.chat_id === currentChat.value?.id) {
      messages.value.push(message)
    }
  }

  function setMessages(newMessages) {
    messages.value = newMessages
  }

  async function loadChats() {
    try {
      const response = await api.get('/chats')
      chats.value = response.data.chats
    } catch (error) {
      console.error('Error loading chats:', error)
    }
  }

  async function loadMessages(chatId) {
    try {
      const response = await api.get(`/chats/${chatId}/messages`)
      messages.value = response.data.messages
    } catch (error) {
      console.error('Error loading messages:', error)
    }
  }

  async function createChat(type, name = null, participantIds = []) {
    try {
      const response = await api.post('/chats', {
        type,
        name,
        participant_ids: participantIds
      })
      addChat(response.data.chat)
      return { success: true, chat: response.data.chat }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Failed to create chat' 
      }
    }
  }

  async function sendMessage(content, messageType = 'text', filePath = null) {
    if (!currentChat.value) return { success: false, error: 'No chat selected' }
    
    try {
      socketService.sendMessage(
        currentChat.value.id,
        content,
        messageType,
        filePath
      )
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Failed to send message' 
      }
    }
  }

  function setOnlineUsers(userIds) {
    onlineUsers.value = new Set(userIds)
  }

  function addOnlineUser(userId) {
    onlineUsers.value.add(userId)
  }

  function removeOnlineUser(userId) {
    onlineUsers.value.delete(userId)
  }

  function isUserOnline(userId) {
    return onlineUsers.value.has(userId)
  }

  // Setup socket listeners
  function setupSocketListeners() {
    socketService.on('new_message', (message) => {
      addMessage(message)
    })

    socketService.on('user_online', (data) => {
      addOnlineUser(data.user_id)
    })

    socketService.on('user_offline', (data) => {
      removeOnlineUser(data.user_id)
    })

    socketService.on('online_users', (data) => {
      setOnlineUsers(data.user_ids)
    })
  }

  return {
    chats,
    currentChat,
    messages,
    onlineUsers,
    setChats,
    addChat,
    setCurrentChat,
    addMessage,
    setMessages,
    loadChats,
    loadMessages,
    createChat,
    sendMessage,
    setOnlineUsers,
    addOnlineUser,
    removeOnlineUser,
    isUserOnline,
    setupSocketListeners
  }
})

