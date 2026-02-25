<template>
  <div class="main-content">
    <div class="stats-grid">
      <div class="stat-card">
        <p class="stat-value">{{ filteredLogs.length }}</p>
        <p class="stat-label">Összes esemény (szerepkör szerint)</p>
      </div>
      
      <div class="stat-card">
        <p class="stat-value accent-text">{{ usersInToday }}</p>
        <p class="stat-label">Aktuálisan bent lévők száma</p>
      </div>

      <div v-if="user.role === 'leader'" class="stat-card">
        <p class="stat-value accent-text">{{ supervisedUsersCount }}</p>
        <p class="stat-label">Felügyelt tagok Összesen</p>
      </div>

      <div v-if="user.role === 'worker'" class="stat-card">
        <p class="stat-value accent-text">{{ myWeeklyWorkHours }} h</p>
        <p class="stat-label">Saját ledolgozott órák a héten</p>
      </div>
    </div>

    <div class="card-custom chart-card">
        <h2>Napi ledolgozott munkaidő (hétfő-vasárnap)</h2>
        <div style="height: 100%; width: 100%; padding-bottom: 2rem;">
          <canvas id="weeklyLogChart"></canvas>
        </div>
    </div>

    <div class="card-custom log-preview">
      <h2>Legutóbbi események (top 5)</h2>
      <ul class="log-list">
        <li v-for="log in recentLogs" :key="log.id">
          <span :class="log.log_IN ? 'log-in' : 'log-out'">
              <i :class="log.log_IN ? 'bi bi-box-arrow-in-right' : 'bi bi-box-arrow-left'"></i>
          </span>
          <strong>{{ getUsername(log.card_id) }}</strong> - {{ log.time }}
        </li>
      </ul>
      <p v-if="recentLogs.length === 0" class="no-data">Nincs megjeleníthető esemény.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'; 

const user = ref(JSON.parse(localStorage.getItem('user') || '{}')) 
const logins = ref([])
let chartInstance = null; 

const fetchData = async () => {
    const token = localStorage.getItem('token')
    if (!token) return;
    
    try {
        const res = await axios.get('http://localhost:8000/user/info', { params: { token } })
        if (res.data.status === 1) {
            logins.value = (res.data.working_hours || []).map((timeStr, index) => ({
                id: index,
                card_id: res.data.card_id,
                time: timeStr,
                log_IN: index % 2 === 0 
            }))
            
            user.value.role = res.data.disposition || res.data.role;
            user.value.full_name = res.data.full_name;
        }
    } catch (e) {
        console.error("Hiba az adatok letöltésekor:", e)
    }
}

const parseLogTime = (logTimeString) => {
    if (!logTimeString) return null;
    const parsable = logTimeString.replace(/(\d{4})\. (\d{2})\. (\d{2})\./, '$1/$2/$3').trim();
    return new Date(parsable);
};

const startOfDay = (date) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d;
};

const calculateWorkDuration = (logData) => {
    let totalMinutes = 0;
    let clockInTime = null;
    const sortedLogs = [...logData].sort((a, b) => parseLogTime(a.time) - parseLogTime(b.time));
    
    sortedLogs.forEach(log => {
        const currentTime = parseLogTime(log.time);
        if (!currentTime) return;
        if (log.log_IN) { clockInTime = currentTime; } 
        else if (clockInTime) {
            const durationMs = currentTime - clockInTime;
            if (durationMs > 0) { totalMinutes += durationMs / (1000 * 60); }
            clockInTime = null; 
        }
    });
    return totalMinutes / 60;
};

const getUsername = () => {
  return user.value.full_name || 'Én';
}

const filteredLogs = computed(() => {
  const userCardId = user.value.card_id; 
  const userRole = user.value.role || user.value.disposition;
  
  return logins.value.filter(log => {
    if(userRole === 'admin') return true;
    return log.card_id == userCardId;
  });
})

const recentLogs = computed(() => [...filteredLogs.value].reverse().slice(0, 5));

const usersInToday = computed(() => {
    const statuses = {};
    filteredLogs.value.forEach(log => { statuses[log.card_id] = log.log_IN; });
    return Object.keys(statuses).filter(cardId => statuses[cardId] === true).length;
});

const myWeeklyWorkHours = computed(() => {
    const userRole = user.value.role || user.value.disposition;
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    const relevantLogs = filteredLogs.value.filter(log => {
        const logDate = parseLogTime(log.time);
        return logDate && logDate > oneWeekAgo && log.card_id == user.value.card_id;
    });
    return calculateWorkDuration(relevantLogs).toFixed(1);
});

const weeklyChartData = computed(() => {
    const currentUserId = user.value.card_id; 
    const today = startOfDay(new Date());
    const displayDayNamesShort = ['H', 'K', 'Sze', 'Cs', 'P', 'Szo', 'V']; 
    
    const currentDayOfWeek = today.getDay(); 
    const daysToMonday = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1; 
    const monday = new Date(today);
    monday.setDate(today.getDate() - daysToMonday);

    const dailyHours = [];
    for (let i = 0; i < 7; i++) {
        const targetDate = new Date(monday);
        targetDate.setDate(monday.getDate() + i); 
        const start = targetDate.getTime();
        const end = targetDate.getTime() + (24 * 60 * 60 * 1000);

        const dailyUserLogs = filteredLogs.value.filter(log => {
            const d = parseLogTime(log.time)?.getTime();
            return log.card_id == currentUserId && d >= start && d < end;
        });
        dailyHours.push(parseFloat(calculateWorkDuration(dailyUserLogs).toFixed(2)));
    }

    return {
        labels: displayDayNamesShort, 
        datasets: [{
            label: `Ledolgozott órák`, 
            data: dailyHours, 
            backgroundColor: '#948979',
            borderRadius: 5
        }]
    };
});

const initializeChart = () => {
    const canvas = document.getElementById('weeklyLogChart');
    if (!canvas) return;
    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(canvas.getContext('2d'), {
        type: 'bar', 
        data: weeklyChartData.value,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 12 } },
            plugins: { legend: { display: false } }
        }
    });
};

onMounted(async () => {
    await fetchData();
    initializeChart();
    
    const observer = new MutationObserver(() => initializeChart());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
});

watch(logins, () => {
    initializeChart();
});
</script>

<style scoped>
.main-content { 
    padding: 2rem; 
    transition: all 0.3s ease;
}

.page-title {
    color: var(--text-main);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.5rem;
    margin-bottom: 2rem;
}

.card-custom {
    background-color: var(--bg-card); 
    padding: 1.5rem; 
    border-radius: 12px; 
    border: 1px solid var(--border-color);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.card-custom h2 {
    color: var(--text-main);
    font-size: 1.3rem;
    margin-bottom: 1rem;
    border-bottom: 1px dashed var(--border-color);
    padding-bottom: 0.5rem;
}

.stats-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
    gap: 1.5rem; 
    margin-bottom: 2rem;
}

.stat-card { 
    background-color: var(--bg-card); 
    padding: 1.5rem; 
    border-radius: 12px; 
    border-left: 5px solid var(--accent);
    border-top: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: bold;
    color: var(--text-main);
    margin-bottom: 0.3rem;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--accent); 
    margin: 0;
}

.accent-text { color: var(--accent); }

.chart-card { height: 400px; padding: 2rem; }

.log-list { list-style: none; padding: 0; }
.log-list li { 
    padding: 0.75rem 0; 
    border-bottom: 1px solid var(--border-color); 
    display: flex; align-items: center; gap: 0.5rem;
    color: var(--text-main);
}
.log-list li:last-child { border-bottom: none; }

.log-in { color: #2ecc71; font-weight: bold; }
.log-out { color: #e74c3c; font-weight: bold; }
.no-data { color: var(--accent); font-style: italic; }
</style>