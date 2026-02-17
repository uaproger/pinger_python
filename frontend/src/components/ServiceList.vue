<template>
  <div class="container mt-5 pb-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Мої сервіси <span class="badge bg-primary rounded-pill">{{ services.length }}</span></h2>
      <div class="text-muted small d-flex align-items-center">
        Автоматичний моніторинг активовано
        <img src="/images/croco.png" alt="croco" style="height: 24px; margin-left: 8px;">
      </div>
    </div>

    <div class="card border-0 shadow-sm mb-5 bg-light">
      <div class="card-body p-4">
        <h5 class="card-title mb-3 fw-bold">Додати новий ресурс</h5>
        <div class="row g-3">
          <div class="col-md-5">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0"><i class="bi bi-tag"></i></span>
              <input v-model="newName" class="form-control border-start-0 ps-0" placeholder="Назва (напр. Мій Сайт)" />
            </div>
          </div>
          <div class="col-md-5">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0"><i class="bi bi-link-45deg"></i></span>
              <input v-model="newUrl" class="form-control border-start-0 ps-0" placeholder="URL (https://example.com)" />
            </div>
          </div>
          <div class="col-md-2">
            <button @click="addService" class="btn btn-primary w-100 fw-bold">
              <i class="bi bi-plus-lg me-1"></i> Додати
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div v-for="service in services" :key="service.id" class="col-md-4">
        <div class="card h-100 border-0 shadow-sm service-card transition-all">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title fw-bold mb-0 text-truncate" style="max-width: 80%;">{{ service.name }}</h5>
              <div :class="service.is_online ? 'status-dot online' : 'status-dot offline'"></div>
            </div>
            <p class="card-text text-muted small text-truncate mb-3">{{ service.url }}</p>

            <div class="d-flex align-items-center mb-3">
              <span :class="service.is_online ? 'badge bg-success-subtle text-success border border-success' : 'badge bg-danger-subtle text-danger border border-danger'" class="px-3 py-2 rounded-pill fw-bold">
                {{ service.is_online ? 'Online' : 'Offline' }} ({{ service.status_code || '---' }})
              </span>
            </div>

            <div class="text-secondary smaller mt-auto">
              <i class="bi bi-clock me-1"></i> Останній запит:
              <span class="fw-medium">{{ service.last_check ? new Date(service.last_check).toLocaleTimeString() : '---' }}</span>
            </div>
          </div>
          <div class="card-footer bg-transparent border-top-0 p-4 pt-0 d-flex gap-2">
            <button @click="pingService(service.id)" class="btn btn-sm btn-outline-primary flex-grow-1 rounded-3">
              Перевірити
            </button>
            <button @click="deleteService(service.id)" class="btn btn-sm btn-outline-danger rounded-3">
              Видалити
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="services.length === 0" class="text-center py-5">
      <div class="display-1 text-muted mb-3 opacity-25">
        <img src="/images/croco.png" alt="croco" style="max-height: 80px; width: auto;">
      </div>
      <h4 class="text-muted">Тут поки порожньо</h4>
      <p class="text-secondary">Ваші сервіси з'являться тут після додавання</p>
    </div>
  </div>
</template>

<style scoped>
.service-card {
  transition: transform 0.2s ease, shadow 0.2s ease;
}
.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 5px;
}
.online { background-color: #198754; box-shadow: 0 0 8px rgba(25, 135, 84, 0.5); }
.offline { background-color: #dc3545; box-shadow: 0 0 8px rgba(220, 53, 69, 0.5); }
.smaller { font-size: 0.75rem; }
</style>

<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import {session, toast} from "aprog";

const services = ref([]);
const newName = ref('');
const newUrl = ref('');
const emit = defineEmits(['logout-event']);

const getAuthHeaders = () => {
  const token = session.get('access_token');
  return { headers: { Authorization: `Bearer ${token}` } };
};

const fetchServices = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/services/', getAuthHeaders());
    services.value = response.data;
  } catch (error) {
    toast().error('Помилка завантаження або потрібна авторизація');
    emit('logout-event');
  }
};

const addService = async () => {
  if (!newName.value || !newUrl.value) {
    toast().warning('Будь ласка, заповніть обидва поля');
    return;
  }
  try {
    await axios.post('http://localhost:8000/api/services/', {
      name: newName.value,
      url: newUrl.value
    }, getAuthHeaders());

    newName.value = '';
    newUrl.value = '';
    await fetchServices();
  } catch (error) {
    toast().error('Помилка при додаванні. Перевірте формат URL.');
  }
};

const deleteService = async (id) => {
  if (!confirm('Ви впевнені, що хочете видалити цей сервіс?')) return;

  try {
    await axios.delete(`http://localhost:8000/api/services/${id}/`, getAuthHeaders());
    await fetchServices();
  } catch (error) {
    toast().error('Не вдалося видалити сервіс');
  }
};

const pingService = async (id) => {
  try {
    await axios.post(`http://localhost:8000/api/services/${id}/ping/`, {}, getAuthHeaders());
    await fetchServices();
  } catch (error) {
    toast().error('Помилка при перевірці статусу');
  }
};

onMounted(fetchServices);
</script>
