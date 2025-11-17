<template>
  <div class="user-card-dark">
    <h3>{{ user.username }}</h3>
    <p>Szerepkör: <span class="role-text">{{ user.role }}</span></p>
    <p>Email: {{ user.email }}</p>
    <p>Regisztrálva: {{ user.created_at }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  user: Object
})
</script>

<style scoped>
.user-card-dark {
  background-color: #222831; /* Legsötétebb háttér, kontraszt a listaboxhoz */
  color: #DFD0B8; /* Világos szöveg */
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem 0;
  border: 1px solid #948979; /* Vékony kiemelő keret */
}

.user-card-dark h3 {
  color: #DFD0B8;
  margin-top: 0;
  border-bottom: 1px dashed #393E46; /* Finomabb elválasztóvonal */
  padding-bottom: 0.5rem;
  margin-bottom: 0.75rem;
}

.user-card-dark p {
  margin-bottom: 0.3rem;
}

.role-text {
  /* Kiemeljük a szerepkört */
  font-weight: bold; 
  color: #948979; 
}
</style>