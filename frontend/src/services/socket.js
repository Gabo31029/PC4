import { io } from 'socket.io-client'
import { SOCKET_URL } from '../config'

class SocketService {
  constructor() {
    this.socket = null
    this.connected = false
  }

  connect(token) {
    if (this.socket?.connected) {
      return this.socket
    }

    this.socket = io(SOCKET_URL, {
      auth: { token },
      transports: ['websocket', 'polling']
    })

    this.socket.on('connect', () => {
      this.connected = true
      console.log('Socket connected to:', SOCKET_URL)
    })

    this.socket.on('disconnect', () => {
      this.connected = false
      console.log('Socket disconnected')
    })

    this.socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error)
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.connected = false
    }
  }

  emit(event, data) {
    if (this.socket && this.connected) {
      this.socket.emit(event, data)
    }
  }

  on(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback)
    }
  }

  off(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback)
    }
  }

  joinChat(chatId) {
    const token = localStorage.getItem('token')
    this.emit('join_chat', { token, chat_id: chatId })
  }

  leaveChat(chatId) {
    this.emit('leave_chat', { chat_id: chatId })
  }

  sendMessage(chatId, content, messageType = 'text', filePath = null) {
    const token = localStorage.getItem('token')
    this.emit('send_message', {
      token,
      chat_id: chatId,
      content,
      message_type: messageType,
      file_path: filePath
    })
  }
}

export default new SocketService()

