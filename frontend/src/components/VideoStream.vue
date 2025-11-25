<template>
  <div class="video-stream">
    <video 
      ref="videoElement"
      :muted="muted"
      autoplay
      playsinline
      class="video-element"
    ></video>
    <div class="video-label">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  stream: {
    type: MediaStream,
    default: null
  },
  muted: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  }
})

const videoElement = ref(null)

watch(() => props.stream, (newStream) => {
  if (videoElement.value && newStream) {
    videoElement.value.srcObject = newStream
  }
}, { immediate: true })

onMounted(() => {
  if (videoElement.value && props.stream) {
    videoElement.value.srcObject = props.stream
  }
})

onUnmounted(() => {
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }
})
</script>

<style scoped>
.video-stream {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-label {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: #e0e0e0;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
}
</style>

