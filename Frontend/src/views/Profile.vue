<template>
  <div class="auth-container">
    <Sidebar />
    <div class="auth-box">
      <h2>Profilom</h2>
      <p><strong>Felhasználónév:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Role:</strong> {{ user.role }}</p>
      <p><strong>Létrehozás ideje:</strong> {{ user.created_at }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue';

const user = ref(JSON.parse(localStorage.getItem('user')) || {})
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}

.auth-box {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  width: 350px;
}
</style>
