<template>
  <div class="log-container">
    <h2 class="table-title">Belépési logok</h2>
    
    <div v-if="loading" class="text-center p-4">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
    
    <div v-else class="table-responsive">
      <table class="log-data-table">
        <thead>
          <tr>
            <th>Felhasználó</th>
            <th>Kártya ID</th>
            <th>Időpont</th>
            <th>Esemény</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(log, index) in formattedLogs" :key="index">
            <td>{{ userData.name }}</td>
            <td class="font-monospace text-accent">{{ userData.cardId }}</td>
            <td class="font-monospace">{{ log.time }}</td>
            <td>
              <span :class="log.isEntry ? 'entry-in' : 'entry-out'">
                <i :class="log.isEntry ? 'bi bi-box-arrow-in-right' : 'bi bi-box-arrow-left'"></i>
                {{ log.isEntry ? " Belépés" : " Kilépés" }}
              </span>
            </td>
          </tr>
          <tr v-if="formattedLogs.length === 0">
            <td colspan="4" class="text-center p-4">Nincsenek rögzített adatok.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const rawHours = ref([])
const userData = ref({ name: '', cardId: '' })
const loading = ref(true)

const fetchLogs = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.get('http://localhost:8000/user/info', { params: { token } })
    console.log("LogTable válasz:", response.data) // Ellenőrzéshez a konzolon
    
    if (response.data.status === 1) {
      rawHours.value = response.data.working_hours || []
      userData.value.name = response.data.full_name
      userData.value.cardId = response.data.card_id
    }
  } catch (e) {
    console.error("Hiba a logok betöltésekor:", e)
  } finally {
    loading.value = false
  }
}

const formattedLogs = computed(() => {
  return rawHours.value.map((item, index) => {
    let timeStr = String(item);
    
    if (timeStr.includes('T') || timeStr.includes('-')) {
      timeStr = timeStr
        .replace('T', ' ')         
        .replace(/-/g, '.') + '.';
    }
    
    timeStr = timeStr.replace(/\s+/g, ' ').trim();

    return {
      time: timeStr,
      isEntry: index % 2 === 0 
    }
  }).reverse()
})
onMounted(fetchLogs)
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