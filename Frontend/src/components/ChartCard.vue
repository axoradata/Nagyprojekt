<template>
  <div class="chart-card">
    <h2>Napi belépések</h2>
    <ul>
      <li v-for="log in logs" :key="log.id">
        {{ getUserName(log.card_id) }} - {{ log.time }} - {{ log.log_IN ? "Belépés" : "Kilépés" }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { logins, users } from '../data'

const logs = logins

const getUserName = (card_id) => {
  const user = users.find(u => u.card_id === card_id)
  return user ? user.username : 'Ismeretlen'
}
</script>

<style scoped>
.chart-card {
  background-color: #74b9ff;
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem 0;
  color: #2d3436;
}

h2 {
  margin-bottom: 0.5rem;
}
</style>
