<template>
  <div class="main-content">
    <h1 class="page-title">Üdv, {{ user.username }}!</h1>

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
        <p class="stat-label">Felügyelt Tagok Összesen</p>
      </div>

      <div v-if="user.role === 'worker'" class="stat-card">
        <p class="stat-value accent-text">{{ myWeeklyWorkHours }} h</p>
        <p class="stat-label">Saját ledolgozott órák a héten</p>
      </div>
    </div>

    <div class="card-custom chart-card">
        <h2>Napi Ledolgozott Munkaidő (Hétfő-Vasárnap)</h2>
        <div style="height: 100%; width: 100%;">
          <canvas id="weeklyLogChart"></canvas>
        </div>
    </div>

    <div class="card-custom log-preview">
      <h2>Legutóbbi események (Top 5)</h2>
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
import { onMounted, computed, ref, nextTick, watch } from 'vue'
import { users, logins, groups } from '../data'
import Chart from 'chart.js/auto'; 

const user = ref(JSON.parse(localStorage.getItem('user') || '{}')) 
let chartInstance = null; 

// --- DÁTUM SEGÉDFÜGGVÉNYEK ÉS LOGIKA (Változatlan) ---
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

const getUsername = (card_id) => {
  const u = users.find(u => u.card_id == card_id)
  return u ? u.username : 'Ismeretlen'
}

const filteredLogs = computed(() => {
  const userCardId = user.value.card_id; 
  const userRole = user.value.role;
  return logins.filter(log => {
    if(userRole === 'admin') return true
    if(userRole === 'leader') {
      const supervisedMembersCardIds = groups
        .filter(g => g.leader_id === user.value.id)
        .flatMap(g => g.members)
        .map(memberId => users.find(u => u.id === memberId)?.card_id)
        .filter(id => id);
      return supervisedMembersCardIds.includes(log.card_id) || log.card_id == userCardId;
    }
    return userRole === 'worker' ? log.card_id == userCardId : false
  })
})

const recentLogs = computed(() => [...filteredLogs.value].reverse().slice(0, 5));
const usersInToday = computed(() => {
    const statuses = {};
    filteredLogs.value.forEach(log => { statuses[log.card_id] = log.log_IN; });
    return Object.keys(statuses).filter(cardId => statuses[cardId] === true).length;
});
const supervisedUsersCount = computed(() => {
    if (user.value.role !== 'leader') return 0;
    const members = groups.filter(g => g.leader_id === user.value.id).flatMap(g => g.members);
    return new Set(members).size;
});
const myWeeklyWorkHours = computed(() => {
    if (user.value.role !== 'worker') return 0;
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
    if (!currentUserId) return { labels: [], datasets: [] };

    const today = startOfDay(new Date());
    const displayDayNamesShort = ['H', 'K', 'Sze', 'Cs', 'P', 'Szo', 'V']; 
    const dateLabels = []; 
    const fullDateLabels = []; 

    const currentDayOfWeek = today.getDay(); 
    const daysToMonday = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1; 
    const monday = new Date(today);
    monday.setDate(today.getDate() - daysToMonday);

    for (let i = 0; i < 7; i++) {
        const day = new Date(monday);
        day.setDate(monday.getDate() + i);
        dateLabels.push(displayDayNamesShort[i]);
        fullDateLabels.push(`${day.getMonth() + 1}/${day.getDate()}`); 
    }

    const dailyHours = fullDateLabels.map((_, index) => {
        const targetDate = new Date(monday);
        targetDate.setDate(monday.getDate() + index); 
        const start = new Date(targetDate).setHours(0,0,0,0);
        const end = new Date(targetDate).setDate(targetDate.getDate() + 1);
        const dailyUserLogs = filteredLogs.value.filter(log => {
            const d = parseLogTime(log.time);
            return log.card_id == currentUserId && d >= start && d < end;
        });
        return parseFloat(calculateWorkDuration(dailyUserLogs).toFixed(2));
    });

    return {
        labels: dateLabels, 
        datasets: [{
            label: `Ledolgozott órák`, 
            data: dailyHours, 
            backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#948979',
            borderRadius: 5,
            fullDateLabels: fullDateLabels 
        }]
    };
});

// --- DINAMIKUS CHART.JS SZÍNEK ---
const getChartColors = () => {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    return {
        text: isLight ? '#2d3436' : '#DFD0B8',
        grid: isLight ? 'rgba(0,0,0,0.05)' : 'rgba(223, 208, 184, 0.1)',
        tooltipBg: isLight ? '#ffffff' : '#222831'
    };
};

const initializeChart = () => {
    if (chartInstance) chartInstance.destroy();
    const canvas = document.getElementById('weeklyLogChart');
    if (!canvas) return;

    const colors = getChartColors();
    const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();

    chartInstance = new Chart(canvas.getContext('2d'), {
        type: 'bar', 
        data: weeklyChartData.value,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
            padding: {
                bottom: 20, // Extra helyet csinál alul a betűknek
                top: 10
                }
            },
            scales: {
                y: { 
                    beginAtZero: true, max: 12,
                    ticks: { color: colors.text },
                    grid: { color: colors.grid },
                    title: { display: true, text: 'Órák', color: colors.text }
                },
                x: { 
                    ticks: { color: colors.text },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: colors.tooltipBg,
                    titleColor: accentColor,
                    bodyColor: colors.text,
                    borderColor: accentColor,
                    borderWidth: 1
                }
            }
        }
    });
};

onMounted(() => {
    initializeChart();
    // Figyeljük, ha a téma változik, rajzoljuk újra a chartot
    const observer = new MutationObserver(() => initializeChart());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
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