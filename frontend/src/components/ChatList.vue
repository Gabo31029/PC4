<template>
  <div class="chat-list">
    <div class="chat-list-header">
      <h2>Chats</h2>
      <button @click="showNewChatModal = true" class="new-chat-btn">+ Nuevo</button>
    </div>
    
    <div class="chat-search">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Buscar chats..."
      />
    </div>
    
    <div class="chats">
      <div 
        v-for="chat in filteredChats" 
        :key="chat.id"
        :class="['chat-item', { active: currentChat?.id === chat.id }]"
        @click="selectChat(chat)"
      >
        <div class="chat-info">
          <div class="chat-name">
            {{ getChatName(chat) }}
          </div>
          <div class="chat-preview">
            {{ getLastMessage(chat) }}
          </div>
        </div>
        <div class="chat-meta">
          <span v-if="isUserOnline(chat)" class="online-indicator"></span>
        </div>
      </div>
    </div>
    
    <!-- New Chat Modal -->
    <div v-if="showNewChatModal" class="modal-overlay" @click="showNewChatModal = false">
      <div class="modal" @click.stop>
        <h3>Nuevo Chat</h3>
        <div class="modal-content">
          <div class="form-group">
            <label>Tipo</label>
            <select v-model="newChatType">
              <option value="direct">Chat Directo</option>
              <option value="group">Grupo</option>
            </select>
          </div>
          <div v-if="newChatType === 'group'" class="form-group">
            <label>Nombre del Grupo</label>
            <input v-model="newChatName" type="text" placeholder="Nombre del grupo" />
          </div>
          <div class="form-group">
            <label>Buscar Usuarios</label>
            <input 
              v-model="userSearch" 
              type="text" 
              placeholder="Buscar usuarios..."
              @input="searchUsers"
            />
            <div v-if="searchResults.length > 0" class="user-results">
              <div 
                v-for="user in searchResults" 
                :key="user.id"
                class="user-result-item"
                @click="toggleUserSelection(user)"
              >
                <span>{{ user.username }}</span>
                <span v-if="selectedUsers.includes(user.id)" class="selected">✓</span>
              </div>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="showNewChatModal = false">Cancelar</button>
            <button @click="createChat" class="primary" :disabled="!canCreateChat">
              Crear
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const chatStore = useChatStore()
const authStore = useAuthStore()

const currentChat = computed(() => chatStore.currentChat)
const searchQuery = ref('')
const showNewChatModal = ref(false)
const newChatType = ref('direct')
const newChatName = ref('')
const userSearch = ref('')
const searchResults = ref([])
const selectedUsers = ref([])

const filteredChats = computed(() => {
  if (!searchQuery.value) return chatStore.chats
  const query = searchQuery.value.toLowerCase()
  return chatStore.chats.filter(chat => {
    const name = getChatName(chat).toLowerCase()
    return name.includes(query)
  })
})

const canCreateChat = computed(() => {
  if (newChatType.value === 'direct') {
    return selectedUsers.value.length === 1
  } else {
    return newChatName.value && selectedUsers.value.length > 0
  }
})

function getChatName(chat) {
  if (chat.type === 'group') {
    return chat.name || 'Grupo sin nombre'
  } else {
    return chat.other_user?.username || 'Usuario desconocido'
  }
}

function getLastMessage(chat) {
  // This would ideally come from the chat object
  return 'Último mensaje...'
}

function isUserOnline(chat) {
  if (chat.type === 'direct' && chat.other_user) {
    return chatStore.isUserOnline(chat.other_user.id)
  }
  return false
}

function selectChat(chat) {
  chatStore.setCurrentChat(chat)
}

async function searchUsers() {
  if (!userSearch.value) {
    searchResults.value = []
    return
  }
  
  try {
    const response = await api.get(`/users?search=${userSearch.value}`)
    searchResults.value = response.data.users.filter(u => u.id !== authStore.user?.id)
  } catch (error) {
    console.error('Error searching users:', error)
  }
}

function toggleUserSelection(user) {
  const index = selectedUsers.value.indexOf(user.id)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  } else {
    if (newChatType.value === 'direct') {
      selectedUsers.value = [user.id]
    } else {
      selectedUsers.value.push(user.id)
    }
  }
}

async function createChat() {
  const result = await chatStore.createChat(
    newChatType.value,
    newChatType.value === 'group' ? newChatName.value : null,
    selectedUsers.value
  )
  
  if (result.success) {
    showNewChatModal.value = false
    newChatName.value = ''
    userSearch.value = ''
    searchResults.value = []
    selectedUsers.value = []
    chatStore.setCurrentChat(result.chat)
  }
}

onMounted(() => {
  chatStore.loadChats()
})
</script>

<style scoped>
.chat-list {
  width: 300px;
  background-color: #2a2a2a;
  border-right: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-list-header {
  padding: 20px;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-list-header h2 {
  margin: 0;
  color: #e0e0e0;
  font-size: 20px;
}

.new-chat-btn {
  padding: 6px 12px;
  font-size: 12px;
}

.chat-search {
  padding: 15px;
  border-bottom: 1px solid #3a3a3a;
}

.chat-search input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
}

.chats {
  flex: 1;
  overflow-y: auto;
}

.chat-item {
  padding: 15px;
  border-bottom: 1px solid #3a3a3a;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
}

.chat-item:hover {
  background-color: #3a3a3a;
}

.chat-item.active {
  background-color: #2563eb;
}

.chat-info {
  flex: 1;
  min-width: 0;
}

.chat-name {
  font-weight: 500;
  color: #e0e0e0;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-preview {
  font-size: 12px;
  color: #b0b0b0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.online-indicator {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  display: inline-block;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
}

.modal h3 {
  margin: 0 0 20px 0;
  color: #e0e0e0;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.user-results {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #3a3a3a;
  border-radius: 4px;
  margin-top: 10px;
}

.user-result-item {
  padding: 10px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #3a3a3a;
}

.user-result-item:hover {
  background-color: #3a3a3a;
}

.user-result-item .selected {
  color: #2563eb;
}
</style>

