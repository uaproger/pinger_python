<template>
  <div class="auth-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="auth-card card p-5 shadow border-0 rounded-4" style="width: 100%; max-width: 420px;">
      <div class="text-center mb-4">
        <div class="display-4 mb-2">
          <img src="/images/croco.png" alt="croco" style="max-height: 80px; width: auto;">
        </div>
        <h2 class="fw-bold">Вітаємо у Pinger</h2>
        <p class="text-secondary">Увійдіть, щоб розпочати моніторинг</p>
      </div>

      <div class="mb-3">
        <label class="form-label fw-medium">Логін</label>
        <input v-model="username" class="form-control form-control-lg rounded-3 border-light-subtle" placeholder="Ваш username" />
      </div>

      <div class="mb-4">
        <label class="form-label fw-medium">Пароль</label>
        <input v-model="password" type="password" class="form-control form-control-lg rounded-3 border-light-subtle" placeholder="••••••••" />
      </div>

      <button @click="login" class="btn btn-primary btn-lg w-100 rounded-3 fw-bold mb-3 shadow-sm">
        Увійти в систему
      </button>

      <p class="text-center text-muted small mb-0">
        У Вас виникли проблеми? Зверніться до адміністратора.
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-wrapper {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
.auth-card {
  transition: transform 0.3s ease;
}
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
  border-color: #0d6efd;
}
</style>

<script setup>
import {ref} from 'vue';
import axios from 'axios';
import {session, toast} from "aprog";

const username = ref('');
const password = ref('');

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/', {
      username: username.value,
      password: password.value
    });
    session.set('access_token', response.data.access);
    toast().success('Успішно залогінились!', {duration: 3000});
    location.reload();
  } catch (error) {
    toast().error('Помилка входу: перевірте дані', {duration: 5000});
  }
};
</script>
