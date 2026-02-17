<script setup>
import {ref} from 'vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import ServiceList from './components/ServiceList.vue'
import {session} from "aprog";

const token = ref(session.get('access_token'))
const showRegister = ref(false)

const logout = () => {
  session.delete('access_token')
  token.value = null
  location.reload()
}
</script>

<template>
  <nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
      <span class="navbar-brand d-flex align-items-center">
        Pinger Pro
        <img src="/images/croco.png" alt="croco" style="height: 30px; margin-left: 10px;">
      </span>
      <button v-if="token" @click="logout" class="btn btn-outline-light btn-sm">Вийти</button>
    </div>
  </nav>

  <main class="container">
    <div v-if="!token">
      <Login v-if="!showRegister" />
      <Register v-else />
      <p class="text-center mt-3">
        <a href="#" @click.prevent="showRegister = !showRegister">
          {{ showRegister ? 'Вже є акаунт? Увійти' : 'Немає акаунту? Реєстрація' }}
        </a>
      </p>
    </div>
    <div v-else>
      <ServiceList />
    </div>
  </main>
</template>
