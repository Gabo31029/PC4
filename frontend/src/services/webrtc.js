class WebRTCService {
  constructor() {
    this.localStream = null
    this.remoteStreams = new Map()
    this.peerConnections = new Map()
    this.socketService = null
    this.onRemoteStream = null
  }

  setSocketService(socketService) {
    this.socketService = socketService
  }

  setOnRemoteStream(callback) {
    this.onRemoteStream = callback
  }

  async getLocalStream(video = true, audio = true) {
    try {
      this.localStream = await navigator.mediaDevices.getUserMedia({
        video,
        audio
      })
      return this.localStream
    } catch (error) {
      console.error('Error getting local stream:', error)
      throw error
    }
  }

  async getScreenStream() {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: true
      })
      return stream
    } catch (error) {
      console.error('Error getting screen stream:', error)
      throw error
    }
  }

  stopLocalStream() {
    if (this.localStream) {
      this.localStream.getTracks().forEach(track => track.stop())
      this.localStream = null
    }
  }

  createPeerConnection(userId, chatId) {
    const configuration = {
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' }
      ]
    }

    const pc = new RTCPeerConnection(configuration)

    // Add local stream tracks
    if (this.localStream) {
      this.localStream.getTracks().forEach(track => {
        pc.addTrack(track, this.localStream)
      })
    }

    // Handle remote stream
    pc.ontrack = (event) => {
      const [remoteStream] = event.streams
      this.remoteStreams.set(userId, remoteStream)
      if (this.onRemoteStream) {
        this.onRemoteStream(userId, remoteStream)
      }
    }

    // Handle ICE candidates
    pc.onicecandidate = (event) => {
      if (event.candidate && this.socketService) {
        const token = localStorage.getItem('token')
        this.socketService.emit('ice_candidate', {
          token,
          chat_id: chatId,
          target_id: userId,
          candidate: event.candidate
        })
      }
    }

    // Handle connection state
    pc.onconnectionstatechange = () => {
      console.log(`Peer connection state: ${pc.connectionState}`)
      if (pc.connectionState === 'failed' || pc.connectionState === 'disconnected') {
        this.closePeerConnection(userId)
      }
    }

    this.peerConnections.set(userId, pc)
    return pc
  }

  async createOffer(userId, chatId) {
    const pc = this.createPeerConnection(userId, chatId)
    const offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return offer
  }

  async handleOffer(offer, userId, chatId) {
    const pc = this.createPeerConnection(userId, chatId)
    await pc.setRemoteDescription(new RTCSessionDescription(offer))
    const answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return answer
  }

  async handleAnswer(answer, userId) {
    const pc = this.peerConnections.get(userId)
    if (pc) {
      await pc.setRemoteDescription(new RTCSessionDescription(answer))
    }
  }

  async handleIceCandidate(candidate, userId) {
    const pc = this.peerConnections.get(userId)
    if (pc) {
      await pc.addIceCandidate(new RTCIceCandidate(candidate))
    }
  }

  closePeerConnection(userId) {
    const pc = this.peerConnections.get(userId)
    if (pc) {
      pc.close()
      this.peerConnections.delete(userId)
    }
    this.remoteStreams.delete(userId)
  }

  closeAllConnections() {
    this.peerConnections.forEach((pc, userId) => {
      this.closePeerConnection(userId)
    })
    this.stopLocalStream()
  }

  replaceTrack(track) {
    // Replace video track in all peer connections
    this.peerConnections.forEach((pc) => {
      const sender = pc.getSenders().find(s => s.track && s.track.kind === 'video')
      if (sender) {
        sender.replaceTrack(track)
      }
    })
  }
}

export default new WebRTCService()

