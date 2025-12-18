<template>
  <div class="chart-card">
    <h2 class="section-title">Napi belépések</h2>
    <ul class="log-list">
      <li v-for="log in logs" :key="log.id" class="log-item">
        <span class="user-name">{{ getUserName(log.card_id) }}</span> 
        <span class="log-time">{{ log.time }}</span> 
        <span :class="log.log_IN ? 'status-in' : 'status-out'">
          {{ log.log_IN ? "Belépés" : "Kilépés" }}
        </span>
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
  background-color: var(--bg-card); 
  color: var(--text-main);
  /* A 1.5rem helyett adjunk nagyobb értéket az aljának: */
  padding: 1.5rem 1.5rem 2.5rem 1.5rem; 
  border-radius: 12px;
  margin: 1rem 0;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  /* Ez biztosítja, hogy a tartalom ne lógjon ki semmiképp: */
  overflow: hidden; 
}
.chart-container {
  position: relative;
  /* Adjunk neki egy kis extra helyet az alján a feliratoknak */
  margin-bottom: 10px; 
  width: 100%;
}

.section-title {
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  font-size: 1.4rem;
}

.log-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.log-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-item:last-child {
  border-bottom: none;
}

.user-name {
  font-weight: 600;
  flex: 1;
}

.log-time {
  color: var(--accent); /* A kiemelő szín (bézs vagy sötétszürke) */
  margin: 0 1rem;
  font-size: 0.9rem;
}

/* Ezek fix színek maradhatnak, mert sötéten és világoson is jól látszanak */
.status-in {
  color: #2ecc71; /* Zöld */
  font-weight: bold;
}

.status-out {
  color: #e74c3c; /* Piros */
  font-weight: bold;
}
</style>