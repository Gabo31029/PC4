import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import socketService from '../services/socket'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    try {
      const response = await api.post('/login', { username, password })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', token.value)
      
      // Connect socket
      socketService.connect(token.value)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  async function register(username, email, password) {
    try {
      const response = await api.post('/register', { username, email, password })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', token.value)
      
      // Connect socket
      socketService.connect(token.value)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed' 
      }
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    socketService.disconnect()
  }

  async function loadUser() {
    if (!token.value) return
    
    try {
      // User info is already in token, but we can fetch if needed
      // For now, we'll get it from login/register response
    } catch (error) {
      console.error('Error loading user:', error)
      logout()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    loadUser
  }
})

