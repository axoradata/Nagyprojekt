<template>
  <div v-if="user.role === 'admin'" class="users-page-container">
    <div class="user-list-box">
      <h2 class="user-list-title">Felhasználók</h2>
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
.users-page-container {
  display: flex;
  justify-content: center;
  padding: 30px; /* margin helyett padding-et használunk, ha a main elem görget */
  min-height: 100%; /* Biztosítja, hogy kitöltse a main területét */
  background-color: #222831; /* Fő háttérszín */
}

.user-list-box {
  background-color: #393E46; /* Kártya/Konténer háttér (világosabb sötét) */
  color: #DFD0B8; /* Világos szöveg */
  padding: 2rem;
  border-radius: 16px;
  width: 400px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.user-list-title {
  color: #DFD0B8;
  border-bottom: 2px solid #948979; /* Kiemelő színű vonal */
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}
</style>