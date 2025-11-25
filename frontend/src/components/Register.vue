<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Registro</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Usuario</label>
          <input 
            v-model="username" 
            type="text" 
            required 
            placeholder="Elige un usuario"
          />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="email" 
            type="email" 
            required 
            placeholder="tu@email.com"
          />
        </div>
        <div class="form-group">
          <label>Contraseña</label>
          <input 
            v-model="password" 
            type="password" 
            required 
            placeholder="Mínimo 6 caracteres"
            minlength="6"
          />
        </div>
        <div class="form-group">
          <label>Confirmar Contraseña</label>
          <input 
            v-model="confirmPassword" 
            type="password" 
            required 
            placeholder="Confirma tu contraseña"
          />
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <button type="submit" class="primary" :disabled="loading">
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>
        <p class="login-link">
          ¿Ya tienes cuenta? 
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  if (password.value !== confirmPassword.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }
  
  if (password.value.length < 6) {
    error.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }
  
  loading.value = true
  error.value = ''
  
  const result = await authStore.register(username.value, email.value, password.value)
  
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error
  }
  
  loading.value = false
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #1a1a1a;
}

.register-card {
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #e0e0e0;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #b0b0b0;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 12px;
  background-color: #1a1a1a;
  border: 1px solid #4a4a4a;
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #2563eb;
}

button {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
}

.error-message {
  background-color: #dc2626;
  color: white;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #b0b0b0;
  font-size: 14px;
}

.login-link a {
  color: #2563eb;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>

