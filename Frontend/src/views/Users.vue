<template>
  <div v-if="user.role === 'admin'" class="page-container-dark">
    <div class="page-content-box">
      <h2 class="section-title">Felhasználók</h2>
      
      <div class="user-grid">
        <UserCard v-for="u in users" :key="u.id" :user="u" />
      </div>
      
    </div>
  </div>
  <div v-else class="page-container-dark">
    <div class="page-content-box">
      <h2 class="section-title text-center" style="color: #D63031;">Hozzáférés megtagadva</h2>
      <p class="text-center">Csak rendszergazdák láthatják ezt az oldalt.</p>
    </div>
  </div>
</template>

<script setup>
import { users } from '../data'
import UserCard from '../components/UserCard.vue'

const user = JSON.parse(localStorage.getItem('user') || '{}')
</script>

<style scoped>
/* --- FŐ ELRENDEZÉS STÍLUSOK (Logs.vue alapján, 900px) --- */
.page-container-dark {
  background-color: #222831; 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100vh;
  width: 100%; 
}

.page-content-box {
  background-color: #393E46; 
  color: #DFD0B8; 
  padding: 2rem;
  border-radius: 16px;
  
  /* EGYSÉGES SZÉLESSÉG */
  width: 900px;
  max-width: 95%; 
  
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.section-title {
  color: #DFD0B8;
  border-bottom: 2px solid #948979; 
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

/* --- RÁCS ELRENDEZÉS a kártyákhoz --- */
.user-grid {
    display: grid;
    /* Automatikus tördelés: minimum 250px széles oszlopok */
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem; 
}
</style>