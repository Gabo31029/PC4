<template>
  <div v-if="inCall" class="call-window">
    <div class="call-container">
      <div class="video-grid">
        <VideoStream 
          :stream="localStream" 
          :muted="true"
          label="Tú"
          class="local-video"
        />
        <VideoStream 
          v-for="[userId, stream] in remoteStreams" 
          :key="userId"
          :stream="stream"
          :muted="false"
          :label="`Usuario ${userId}`"
          class="remote-video"
        />
      </div>
      
      <CallControls 
        :video-enabled="videoEnabled"
        :audio-enabled="audioEnabled"
        :screen-sharing="screenSharing"
        @toggle-video="toggleVideo"
        @toggle-audio="toggleAudio"
        @toggle-screen="toggleScreenShare"
        @end-call="endCall"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useWebRTCStore } from '../stores/webrtc'
import VideoStream from './VideoStream.vue'
import CallControls from './CallControls.vue'

const webrtcStore = useWebRTCStore()

const inCall = computed(() => webrtcStore.inCall)
const localStream = computed(() => webrtcStore.localStream)
const remoteStreams = computed(() => webrtcStore.remoteStreams)
const videoEnabled = computed(() => webrtcStore.videoEnabled)
const audioEnabled = computed(() => webrtcStore.audioEnabled)
const screenSharing = computed(() => webrtcStore.screenSharing)

function toggleVideo() {
  webrtcStore.toggleVideo()
}

function toggleAudio() {
  webrtcStore.toggleAudio()
}

function toggleScreenShare() {
  webrtcStore.toggleScreenShare()
}

function endCall() {
  webrtcStore.endCall()
}
</script>

<style scoped>
.call-window {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #000;
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.call-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.video-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;
  padding: 10px;
  overflow: auto;
}

.local-video {
  position: relative;
  min-height: 200px;
}

.remote-video {
  position: relative;
  min-height: 200px;
}
</style>

