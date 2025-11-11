<template>
  <div class="log-table">
    <h2>Belépési logok</h2>
    <table>
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
          <td>{{ log.log_IN ? "Belépés" : "Kilépés" }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { logins, users } from '../data'

const logs = logins.reverse()

const getUserName = (card_id) => {
  const user = users.find(u => u.card_id === card_id)
  return user ? user.username : 'Ismeretlen'
}
</script>

<style scoped>
.log-table {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid #ccc;
}

th {
  background-color: #2c3e50;
  color: white;
}
</style>
