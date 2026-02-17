<template>
  <div class="auth-wrapper d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="auth-card card p-5 shadow border-0 rounded-4" style="width: 100%; max-width: 420px;">
      <div class="text-center mb-4">
        <div class="display-4 mb-2">
          <img src="/images/croco.png" alt="croco" style="max-height: 80px; width: auto;">
        </div>
        <h2 class="fw-bold">Створити акаунт</h2>
        <p class="text-secondary">Приєднуйтесь до системи моніторингу</p>
      </div>

      <div class="mb-3">
        <label class="form-label fw-medium">Логін</label>
        <div class="input-group">
          <span class="input-group-text bg-white border-light-subtle"><i class="bi bi-person"></i></span>
          <input v-model="username" class="form-control form-control-lg rounded-end-3 border-light-subtle" placeholder="Вигадайте логін" />
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label fw-medium">Електронна пошта</label>
        <div class="input-group">
          <span class="input-group-text bg-white border-light-subtle"><i class="bi bi-envelope"></i></span>
          <input v-model="email" type="email" class="form-control form-control-lg rounded-end-3 border-light-subtle" placeholder="example@mail.com" />
        </div>
      </div>

      <div class="mb-4">
        <label class="form-label fw-medium">Пароль</label>
        <div class="input-group">
          <span class="input-group-text bg-white border-light-subtle"><i class="bi bi-lock"></i></span>
          <input v-model="password" type="password" class="form-control form-control-lg rounded-end-3 border-light-subtle" placeholder="••••••••" />
        </div>
      </div>

      <button @click="register" class="btn btn-success btn-lg w-100 rounded-3 fw-bold mb-3 shadow-sm">
        Зареєструватися
      </button>

      <p class="text-center text-muted small mb-0">
        Вже є акаунт?
        <a href="#" @click.prevent="$emit('switch-to-login')" class="text-primary text-decoration-none fw-bold">Увійти</a>
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
.auth-card:hover {
  transform: translateY(-5px);
}
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.1);
  border-color: #198754;
}
.input-group-text {
  color: #6c757d;
}
</style>

<script setup>
import {ref, defineEmits} from 'vue';
import axios from 'axios';
import {toast} from "aprog";

const emit = defineEmits(['registered', 'switch-to-login']);

const username = ref('');
const email = ref('');
const password = ref('');

const register = async () => {
  if (!username.value || !password.value) {
    toast().warning('Логін та пароль є обов\'язковими');
    return;
  }

  try {
    await axios.post('http://localhost:8000/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    });

    toast().success('Реєстрація успішна! Тепер увійдіть.');
    emit('registered');
  } catch (e) {
    toast().error('Помилка реєстрації. Можливо, такий логін вже існує.');
  }
};
</script>
