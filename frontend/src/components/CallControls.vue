<template>
  <div class="call-controls">
    <button 
      @click="$emit('toggle-audio')"
      :class="['control-btn', { active: audioEnabled }]"
      :title="audioEnabled ? 'Silenciar' : 'Activar audio'"
    >
      {{ audioEnabled ? '🔊' : '🔇' }}
    </button>
    
    <button 
      @click="$emit('toggle-video')"
      :class="['control-btn', { active: videoEnabled }]"
      :title="videoEnabled ? 'Apagar video' : 'Activar video'"
    >
      {{ videoEnabled ? '📹' : '📵' }}
    </button>
    
    <button 
      @click="$emit('toggle-screen')"
      :class="['control-btn', { active: screenSharing }]"
      title="Compartir pantalla"
    >
      🖥️
    </button>
    
    <button 
      @click="$emit('end-call')"
      class="control-btn danger"
      title="Finalizar llamada"
    >
      📞
    </button>
  </div>
</template>

<script setup>
defineProps({
  videoEnabled: {
    type: Boolean,
    default: true
  },
  audioEnabled: {
    type: Boolean,
    default: true
  },
  screenSharing: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-video', 'toggle-audio', 'toggle-screen', 'end-call'])
</script>

<style scoped>
.call-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background-color: #1a1a1a;
}

.control-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #4a4a4a;
  background-color: #2a2a2a;
  transition: all 0.2s;
}

.control-btn:hover {
  background-color: #3a3a3a;
  transform: scale(1.1);
}

.control-btn.active {
  background-color: #2563eb;
  border-color: #2563eb;
}

.control-btn.danger {
  background-color: #dc2626;
  border-color: #dc2626;
}

.control-btn.danger:hover {
  background-color: #b91c1c;
}
</style>

