<template>
  <div v-if="user.disposition === 'admin' || user.role === 'admin'" class="page-container">
    <div class="page-content-box">
      <h2 class="section-title">Felhasználók</h2>
      
      <div v-if="loading" class="text-center p-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else class="user-grid">
        <UserCard 
          v-for="u in users" 
          :key="u.card_id" 
          :user="u" 
          @refresh="fetchUsers" 
        />
      </div>

      <div v-if="!loading && users.length === 0" class="text-center p-5 text-muted">
        Nincsenek megjeleníthető felhasználók.
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
          <i class="bi bi-house-door me-2"></i>Vissza a főoldalra
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import UserCard from '../components/UserCard.vue'

// Reaktív változók
const users = ref([])
const loading = ref(true)
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const fetchUsers = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    loading.value = true
    // A korábbi getAllUser routeredet hívjuk meg
    const response = await axios.get('http://localhost:8000/user/all', {
      params: { token: token }
    })

    if (response.data.status === 1) {
      users.value = response.data.users
    } else {
      console.error("Hiba az adatok lekérésekor:", response.data.message)
    }
  } catch (error) {
    console.error("Hálózati hiba:", error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Csak akkor töltsük le az adatokat, ha admin
  if (user.value.role === 'admin' || user.value.disposition === 'admin') {
    fetchUsers()
  }
})
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