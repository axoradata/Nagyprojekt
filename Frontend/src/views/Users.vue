<template>
  <div v-if="user.role === 'admin'" class="page-container">
    <div class="page-content-box">
      <h2 class="section-title">Felhasználók Kezelése</h2>
      
      <div class="user-grid">
        <UserCard v-for="u in users" :key="u.id" :user="u" />
      </div>
      
    </div>
  </div>
  
  <div v-else class="page-container">
    <div class="page-content-box access-denied-box">
      <div class="text-center p-5">
        <i class="bi bi-exclamation-octagon-fill display-1 text-danger mb-4"></i>
        <h2 class="section-title border-0">Hozzáférés megtagadva</h2>
        <p class="lead">Sajnáljuk, de csak rendszergazdák láthatják ezt az oldalt.</p>
        <router-link to="/dashboard" class="btn custom-btn-primary mt-3">
          Vissza a főoldalra
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { users } from '../data'
import UserCard from '../components/UserCard.vue'

const user = JSON.parse(localStorage.getItem('user') || '{}')
</script>

<style scoped>
.page-container {
  background-color: var(--bg-main); 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100vh;
  width: 100%; 
  transition: background-color 0.3s ease;
}

.page-content-box {
  background-color: var(--bg-card); 
  color: var(--text-main); 
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 1000px; /* Megnövelve a rács miatt */
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.section-title {
  color: var(--text-main);
  border-bottom: 2px solid var(--accent); 
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

/* --- RÁCS ELRENDEZÉS --- */
.user-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem; 
}

/* --- ACCESS DENIED EXTRA --- */
.access-denied-box {
    border-top: 5px solid #D63031;
}

.custom-btn-primary {
  background-color: var(--accent);
  border-color: var(--accent);
  color: white;
  padding: 0.6rem 1.5rem;
  font-weight: 600;
}

.custom-btn-primary:hover {
  filter: brightness(1.1);
}
</style>