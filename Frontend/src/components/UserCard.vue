<template>
  <div class="user-card">
    <h3>{{ user.username }}</h3>
    <p>Role: {{ user.role }}</p>
    <p>Email: {{ user.email }}</p>
    <p>Belépés: {{ user.created_at }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  user: Object
})
</script>

<style scoped>
.user-card {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  border-radius: 12px;
  margin: 0.5rem 0;
}
</style>
