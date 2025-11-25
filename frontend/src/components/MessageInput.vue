<template>
  <div class="message-input-container">
    <div class="input-actions">
      <button @click="toggleFileInput" class="icon-btn" title="Subir archivo">
        📎
      </button>
      <button @click="toggleAudioRecorder" class="icon-btn" title="Grabar audio">
        🎤
      </button>
      <input 
        ref="fileInput"
        type="file" 
        style="display: none" 
        @change="handleFileSelect"
      />
    </div>
    <textarea
      v-model="message"
      @keydown.enter.exact.prevent="sendMessage"
      @keydown.enter.shift.exact="message += '\n'"
      placeholder="Escribe un mensaje..."
      rows="1"
      class="message-textarea"
    ></textarea>
    <button @click="sendMessage" class="send-btn" :disabled="!canSend">
      Enviar
    </button>
    
    <!-- Audio Recorder -->
    <div v-if="recording" class="audio-recorder">
      <div class="recording-indicator">
        <span class="pulse"></span>
        <span>Grabando...</span>
      </div>
      <button @click="stopRecording" class="stop-btn">Detener</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useChatStore } from '../stores/chat'
import api from '../services/api'

const props = defineProps({
  chatId: {
    type: Number,
    required: true
  }
})

const chatStore = useChatStore()

const message = ref('')
const fileInput = ref(null)
const recording = ref(false)
const mediaRecorder = ref(null)
const audioChunks = ref([])

const canSend = computed(() => {
  return message.value.trim().length > 0 || recording.value
})

function toggleFileInput() {
  fileInput.value?.click()
}

async function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    const filePath = response.data.file_path
    const messageType = file.type.startsWith('audio/') ? 'audio' : 'file'
    
    await chatStore.sendMessage(file.name, messageType, filePath)
    
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    alert('Error al subir el archivo')
  }
}

async function toggleAudioRecorder() {
  if (recording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    mediaRecorder.value.onstop = async () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
      await uploadAudio(audioBlob)
      
      // Stop all tracks
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.value.start()
    recording.value = true
  } catch (error) {
    console.error('Error starting recording:', error)
    alert('Error al iniciar la grabación')
  }
}

function stopRecording() {
  if (mediaRecorder.value && recording.value) {
    mediaRecorder.value.stop()
    recording.value = false
  }
}

async function uploadAudio(audioBlob) {
  try {
    const formData = new FormData()
    formData.append('file', audioBlob, 'audio.webm')
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    const filePath = response.data.file_path
    
    await chatStore.sendMessage('Audio', 'audio', filePath)
  } catch (error) {
    console.error('Error uploading audio:', error)
    alert('Error al subir el audio')
  }
}

async function sendMessage() {
  if (!canSend.value) return
  
  if (message.value.trim()) {
    await chatStore.sendMessage(message.value.trim(), 'text')
    message.value = ''
  }
}

onUnmounted(() => {
  if (recording.value) {
    stopRecording()
  }
})
</script>

<style scoped>
.message-input-container {
  padding: 15px 20px;
  border-top: 1px solid #3a3a3a;
  background-color: #2a2a2a;
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.input-actions {
  display: flex;
  gap: 5px;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
}

.icon-btn:hover {
  background-color: #3a3a3a;
}

.message-textarea {
  flex: 1;
  min-height: 40px;
  max-height: 120px;
  resize: none;
  font-family: inherit;
}

.send-btn {
  padding: 10px 20px;
  min-width: 80px;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.audio-recorder {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.recording-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #e0e0e0;
}

.pulse {
  width: 12px;
  height: 12px;
  background-color: #dc2626;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.stop-btn {
  padding: 8px 16px;
  background-color: #dc2626;
  border-color: #dc2626;
}
</style>

