<template>
  <div class="log-container">
    <h2 class="table-title">Belépési logok</h2>
    <div class="table-responsive">
      <table class="log-data-table">
        <thead>
          <tr>
            <th>Felhasználó</th>
            <th>ID kártya</th>
            <th>Idő</th>
            <th>Be/Ki</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ getUserName(log.card_id) }}</td>
            <td>{{ log.card_id }}</td>
            <td>{{ log.time }}</td>
            <td>
              <span :class="log.log_IN ? 'entry-in' : 'entry-out'">
                {{ log.log_IN ? "Belépés" : "Kilépés" }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { logins, users } from '../data'

const logs = [...logins].reverse() // Eredeti tömb megőrzése mellett megfordítjuk

const getUserName = (card_id) => {
  const user = users.find(u => u.card_id === card_id)
  return user ? user.username : 'Ismeretlen'
}
</script>

<style scoped>
.log-container {
  background-color: var(--bg-card); 
  padding: 1.5rem;
  border-radius: 12px;
  margin: 1rem 0;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.table-title {
    color: var(--text-main);
    border-bottom: 2px solid var(--accent); 
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.table-responsive {
  overflow-x: auto; /* Mobilbarát nézet, ha túl széles a tábla */
}

.log-data-table {
  width: 100%;
  border-collapse: collapse;
}

/* Fejléc */
.log-data-table th {
  text-align: left;
  padding: 1rem 0.75rem;
  background-color: var(--bg-inner); 
  color: var(--text-main);
  font-weight: 600;
  border-bottom: 2px solid var(--border-color);
}

/* Sorok és Cellák */
.log-data-table td {
  text-align: left;
  padding: 0.85rem 0.75rem;
  border-bottom: 1px solid var(--border-color); 
  background-color: transparent; /* A szülő háttérszíne látszik */
  color: var(--text-main);
  transition: background-color 0.2s ease;
}

/* Páros sorok színezése - dinamikus átlátszósággal */
.log-data-table tr:nth-child(even) td {
    background-color: rgba(0, 0, 0, 0.03); 
}

/* Világos módban egy kicsit sötétebb csíkozás */
[data-theme="light"] .log-data-table tr:nth-child(even) td {
    background-color: rgba(0, 0, 0, 0.02);
}

/* Hover effektus a soron */
.log-data-table tr:hover td {
    background-color: rgba(148, 137, 121, 0.15); /* Az accent színünk (bézs) halvány verziója */
}

.log-data-table tr:last-child td {
  border-bottom: none;
}

/* Állapotjelzők (ezek maradhatnak fixek, mert jól mutatnak mindkét háttéren) */
.entry-in {
    font-weight: bold;
    color: #2ecc71; 
}
.entry-out {
    font-weight: bold;
    color: #e74c3c; 
}
</style>