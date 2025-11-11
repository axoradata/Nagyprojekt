<template>
  <div class="layout">
    <Sidebar />
    <main class="main-content">
      <h1>Üdv, {{ user.username }}!</h1>

      <div class="stats">
        <p>Összes belépés/kilépés, amit láthatsz: {{ filteredLogs.length }}</p>
      </div>

      <div class="log-preview">
        <h2>Legutóbbi események</h2>
        <ul>
          <li v-for="log in recentLogs" :key="log.id">
            {{ getUsername(log.card_id) }} - {{ log.time }} - {{ log.log_IN ? 'Belépés' : 'Kilépés' }}
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
import { users, logins, groups } from '../data'

const user = JSON.parse(localStorage.getItem('user') || '{}')

// card_id -> username segédfüggvény
const getUsername = (card_id) => {
  const u = users.find(u => u.card_id === card_id)
  return u ? u.username : 'Ismeretlen'
}

// filterezés role alapján
const filteredLogs = logins.filter(log => {
  if(user.role === 'admin') return true
  if(user.role === 'leader') {
    const groupMembers = groups
      .filter(g => g.leader_id === user.id)
      .flatMap(g => g.members)
    return groupMembers.includes(log.card_id)
  }
  if(user.role === 'worker') {
    return log.card_id === user.card_id
  }
  return false
})

// legutóbbi 5 esemény
const recentLogs = filteredLogs.slice(-5).reverse()
</script>

<style scoped>
.layout { 
  display: flex; min-height: 100vh;
}

.main-content { flex: 1; padding: 2rem; background: #f1f2f6; color: #2c3e50}
.stats { margin-bottom: 2rem; background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.log-preview { background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
ul { list-style: none; padding: 0; }
li { padding: 0.5rem 0; border-bottom: 1px solid #ccc; }
</style>
