<template>
  <div class="log-table-dark">
    <h2 class="table-title">Belépési logok</h2>
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
.log-table-dark {
  /* Megtartjuk a színt, amit a szülő (LogBox) már megadott, 
     vagy ha önálló, akkor ez a #393E46 */
  background-color: #393E46; 
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem 0;
  color: #DFD0B8; /* Alapértelmezett szövegszín */
}

.table-title {
    color: #DFD0B8;
    border-bottom: 2px solid #948979; /* Kiemelő színű aláhúzás */
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.log-data-table {
  width: 100%;
  border-collapse: collapse;
}

/* Fejléc */
.log-data-table th {
  text-align: left;
  padding: 0.75rem 0.5rem;
  
  /* Legsötétebb szín a kiemeléshez */
  background-color: #222831; 
  color: #DFD0B8;
  
  /* Keret eltávolítása, hogy ne legyen dupla vonal */
  border-bottom: none; 
}

/* Sorok és Cellák */
.log-data-table td {
  text-align: left;
  padding: 0.75rem 0.5rem;
  
  /* Finom elválasztóvonal */
  border-bottom: 1px solid #393E46; 
  background-color: #393E46; /* Megegyezik a dobozzal */
  color: #DFD0B8;
}

.log-data-table tr:nth-child(even) td {
    /* Színváltás a páros soroknál a jobb olvashatóság érdekében */
    background-color: #333940; 
}

.log-data-table tr:hover td {
    /* Hover effektus a soron */
    background-color: #484f59;
}

.log-data-table tr:last-child td {
  border-bottom: none;
}

/* Belépés/Kilépés állapot kiemelése (Opcionális) */
.entry-in {
    font-weight: bold;
    color: #85b066; /* Zöldes árnyalat belépésre */
}
.entry-out {
    font-weight: bold;
    color: #d63031; /* Pirosas árnyalat kilépésre */
}
</style>