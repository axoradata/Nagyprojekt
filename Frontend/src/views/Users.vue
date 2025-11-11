<template>
  <div v-if="user.role === 'admin'" class="auth-container">
    <div class="auth-box">
      <h2>Felhasználók</h2>
      <UserCard v-for="u in users" :key="u.id" :user="u" />
    </div>
  </div>
</template>

<script setup>
import { users } from '../data'
import UserCard from '../components/UserCard.vue'

const user = JSON.parse(localStorage.getItem('user') || '{}')
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.auth-box {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  width: 400px;
}
</style>
