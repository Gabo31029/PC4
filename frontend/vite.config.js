import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: '0.0.0.0', // Permite acceso desde otras máquinas en la red
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true
      },
      '/socket.io': {
        target: process.env.VITE_SOCKET_URL || 'http://localhost:5000',
        ws: true
      }
    }
  }
})

