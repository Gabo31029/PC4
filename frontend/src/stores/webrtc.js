import { defineStore } from 'pinia'
import { ref } from 'vue'
import webrtcService from '../services/webrtc'
import socketService from '../services/socket'

export const useWebRTCStore = defineStore('webrtc', () => {
  const inCall = ref(false)
  const isCaller = ref(false)
  const localStream = ref(null)
  const remoteStreams = ref(new Map())
  const currentChatId = ref(null)
  const videoEnabled = ref(true)
  const audioEnabled = ref(true)
  const screenSharing = ref(false)

  webrtcService.setSocketService(socketService)
  webrtcService.setOnRemoteStream((userId, stream) => {
    addRemoteStream(userId, stream)
  })

  async function startCall(chatId, isInitiator = true) {
    try {
      isCaller.value = isInitiator
      currentChatId.value = chatId
      
      // Get local stream
      localStream.value = await webrtcService.getLocalStream(videoEnabled.value, audioEnabled.value)
      
      if (isInitiator) {
        // Create offer for all participants
        const offer = await webrtcService.createOffer(null, chatId)
        const token = localStorage.getItem('token')
        socketService.emit('call_offer', {
          token,
          chat_id: chatId,
          offer
        })
      }
      
      inCall.value = true
      return { success: true }
    } catch (error) {
      console.error('Error starting call:', error)
      return { success: false, error: error.message }
    }
  }

  async function answerCall(chatId, callerId, offer) {
    try {
      currentChatId.value = chatId
      isCaller.value = false
      
      // Get local stream
      localStream.value = await webrtcService.getLocalStream(videoEnabled.value, audioEnabled.value)
      
      // Handle offer and create answer
      const answer = await webrtcService.handleOffer(offer, callerId, chatId)
      
      const token = localStorage.getItem('token')
      socketService.emit('call_answer', {
        token,
        chat_id: chatId,
        caller_id: callerId,
        answer
      })
      
      inCall.value = true
      return { success: true }
    } catch (error) {
      console.error('Error answering call:', error)
      return { success: false, error: error.message }
    }
  }

  async function endCall() {
    const chatId = currentChatId.value
    
    webrtcService.closeAllConnections()
    localStream.value = null
    remoteStreams.value.clear()
    inCall.value = false
    isCaller.value = false
    screenSharing.value = false
    
    if (chatId) {
      const token = localStorage.getItem('token')
      socketService.emit('call_end', {
        token,
        chat_id: chatId
      })
    }
    
    currentChatId.value = null
  }

  async function toggleVideo() {
    if (localStream.value) {
      const videoTrack = localStream.value.getVideoTracks()[0]
      if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled
        videoEnabled.value = videoTrack.enabled
      }
    }
  }

  async function toggleAudio() {
    if (localStream.value) {
      const audioTrack = localStream.value.getAudioTracks()[0]
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled
        audioEnabled.value = audioTrack.enabled
      }
    }
  }

  async function toggleScreenShare() {
    try {
      if (screenSharing.value) {
        // Stop screen share and resume camera
        const stream = await webrtcService.getLocalStream(true, audioEnabled.value)
        localStream.value = stream
        webrtcService.replaceTrack(stream.getVideoTracks()[0])
        screenSharing.value = false
      } else {
        // Start screen share
        const screenStream = await webrtcService.getScreenStream()
        const videoTrack = screenStream.getVideoTracks()[0]
        
        // Keep audio from original stream
        if (localStream.value) {
          const audioTrack = localStream.value.getAudioTracks()[0]
          if (audioTrack) {
            screenStream.addTrack(audioTrack)
          }
        }
        
        localStream.value = screenStream
        webrtcService.replaceTrack(videoTrack)
        screenSharing.value = true
        
        // Handle screen share end
        videoTrack.onended = () => {
          toggleScreenShare()
        }
      }
    } catch (error) {
      console.error('Error toggling screen share:', error)
    }
  }

  function addRemoteStream(userId, stream) {
    remoteStreams.value.set(userId, stream)
  }

  function removeRemoteStream(userId) {
    remoteStreams.value.delete(userId)
  }

  // Setup socket listeners
  function setupSocketListeners() {
    socketService.on('call_offer', async (data) => {
      const { chat_id, caller_id, offer } = data
      // Show call notification (you can emit an event or use a notification system)
      // For now, we'll auto-answer (you might want to add a UI for this)
      await answerCall(chat_id, caller_id, offer)
    })

    socketService.on('call_answer', async (data) => {
      const { answerer_id, answer } = data
      await webrtcService.handleAnswer(answer, answerer_id)
      // The remote stream will be added via webrtcService's ontrack handler
    })

    socketService.on('ice_candidate', async (data) => {
      const { sender_id, candidate } = data
      await webrtcService.handleIceCandidate(candidate, sender_id)
    })

    socketService.on('call_end', () => {
      endCall()
    })
  }

  return {
    inCall,
    isCaller,
    localStream,
    remoteStreams,
    currentChatId,
    videoEnabled,
    audioEnabled,
    screenSharing,
    startCall,
    answerCall,
    endCall,
    toggleVideo,
    toggleAudio,
    toggleScreenShare,
    addRemoteStream,
    removeRemoteStream,
    setupSocketListeners
  }
})

