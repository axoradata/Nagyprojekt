<template>
  <div class="layout-dark">
    <main class="main-content-dark">
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

      <div class="card-dark chart-card">
          <h2>Napi Ledolgozott Munkaidő (Hétfő-Vasárnap)</h2>
          <div style="height: 100%; width: 100%;">
            <canvas id="weeklyLogChart"></canvas>
          </div>
      </div>


      <div class="card-dark log-preview">
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

    </main>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, nextTick, watch } from 'vue'
import { users, logins, groups } from '../data'
import Chart from 'chart.js/auto'; 

const user = ref(JSON.parse(localStorage.getItem('user') || '{}')) 
let chartInstance = null; 

// --- DÁTUM SEGÉDFÜGGVÉNYEK ---

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

        if (log.log_IN) {
            clockInTime = currentTime;
        } else if (clockInTime) {
            const durationMs = currentTime - clockInTime;
            if (durationMs > 0) {
                totalMinutes += durationMs / (1000 * 60); // ms -> perc
            }
            clockInTime = null; 
        }
    });

    return totalMinutes / 60; // Perc -> Óra
};


// --- EGYÉB SZÁMÍTÁSOK ---

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
    
    if(userRole === 'worker') {
      return log.card_id == userCardId
    }
    return false
  })
})

const recentLogs = computed(() => {
    return [...filteredLogs.value].reverse().slice(0, 5); 
});

const usersInToday = computed(() => {
    const statuses = {};
    filteredLogs.value.forEach(log => {
        statuses[log.card_id] = log.log_IN; 
    });
    return Object.keys(statuses).filter(cardId => statuses[cardId] === true).length;
});

const supervisedUsersCount = computed(() => {
    if (user.value.role !== 'leader') return 0;
    const members = groups
        .filter(g => g.leader_id === user.value.id)
        .flatMap(g => g.members);
    return new Set(members).size;
});

const myWeeklyWorkHours = computed(() => {
    if (user.value.role !== 'worker') return 0;
    
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const relevantLogs = filteredLogs.value.filter(log => {
        const logDate = parseLogTime(log.time);
        if (!logDate) return false;
        return logDate > oneWeekAgo; 
    });

    const ownLogs = relevantLogs.filter(log => log.card_id == user.value.card_id);
    const totalHours = calculateWorkDuration(ownLogs);

    return totalHours.toFixed(1);
});


// 6. Heti Munkaidő Összegzés Adatok
const weeklyChartData = computed(() => {
    
    const currentUserId = user.value.card_id; 
    
    if (!currentUserId) {
        return { labels: [], datasets: [] };
    }

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
        
        const jsDayIndex = day.getDay(); 
        const displayIndex = (jsDayIndex + 6) % 7; 
        
        const dayNameShort = displayDayNamesShort[displayIndex]; 
        
        dateLabels.push(dayNameShort);
        fullDateLabels.push(`${day.getMonth() + 1}/${day.getDate()}`); 
    }

    const dailyHours = fullDateLabels.map((dateStr, index) => {
        const targetDate = new Date(monday);
        targetDate.setDate(monday.getDate() + index); 
        
        const startOfTargetDay = new Date(targetDate);
        startOfTargetDay.setHours(0, 0, 0, 0);

        const endOfTargetDay = new Date(targetDate);
        endOfTargetDay.setDate(endOfTargetDay.getDate() + 1); 
        endOfTargetDay.setHours(0, 0, 0, 0);

        const dailyUserLogs = filteredLogs.value
            .filter(log => log.card_id == currentUserId)
            .filter(log => {
                const logDate = parseLogTime(log.time);
                if (!logDate) return false;
                return logDate >= startOfTargetDay && logDate < endOfTargetDay;
            });
            
        const totalHours = calculateWorkDuration(dailyUserLogs);
        
        return totalHours > 0 ? parseFloat(totalHours.toFixed(2)) : 0;
    });


    const primaryColor = '#948979'; 
    
    return {
        labels: dateLabels, 
        datasets: [{
            label: `Ledolgozott órák`, 
            data: dailyHours, 
            backgroundColor: primaryColor,
            borderColor: primaryColor,
            borderWidth: 1,
            borderRadius: 5,
            fullDateLabels: fullDateLabels 
        }]
    };
});


// --- CHART.JS INICIALIZÁLÁS ---
const initializeChart = () => {
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    const canvasElement = document.getElementById('weeklyLogChart');
    if (!canvasElement) {
        return; 
    }
    
    const ctx = canvasElement.getContext('2d');
    const data = weeklyChartData.value;

    chartInstance = new Chart(ctx, {
        type: 'bar', 
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            // EZ A RÉSZ GONDOSKODIK A HELYRŐL A FELIRATOKNAK
            layout: {
                 padding: {
                    bottom: 20 // Plusz hely alul a feliratoknak
                 }
            },
            scales: {
                y: {
                    min: 0,
                    max: 12, 
                    stacked: false, 
                    title: {
                        display: true,
                        text: 'Ledolgozott Órák',
                        color: '#DFD0B8'
                    },
                    grid: { color: 'rgba(223, 208, 184, 0.1)' },
                    ticks: { 
                        color: '#DFD0B8', 
                        stepSize: 1 
                    }
                },
                x: {
                    stacked: false, 
                    grid: { color: 'rgba(223, 208, 184, 0.1)' },
                    ticks: { color: '#DFD0B8' }
                }
            },
            plugins: {
                legend: { 
                    display: false, 
                    labels: { color: '#DFD0B8' } 
                }, 
                tooltip: { 
                    backgroundColor: '#222831', 
                    titleColor: '#DFD0B8', 
                    bodyColor: '#DFD0B8',
                    callbacks: {
                        title: function(context) {
                            if (context.length > 0) {
                                return context[0].dataset.fullDateLabels[context[0].dataIndex] + ' - ' + context[0].label; 
                            }
                            return '';
                        },
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y.toFixed(1); 
                            return `${label}: ${value} óra`;
                        }
                    }
                }
            }
        }
    });
};

onMounted(() => {
    watch(weeklyChartData, () => {
        initializeChart();
    }, { immediate: true }); 
    
    nextTick(() => {
        initializeChart();
    });
});
</script>

<style scoped>
/* --- FŐ ELRENDEZÉS STÍLUSOK (Változatlanul hagyva, kivéve a chart-card height-et) --- */
.layout-dark { 
    display: flex; 
    min-height: 100vh;
}

.main-content-dark { 
    flex: 1; 
    padding: 2rem; 
    background-color: #222831; 
    color: #DFD0B8; 
}

.page-title {
    color: #DFD0B8;
    border-bottom: 2px solid #948979;
    padding-bottom: 0.5rem;
    margin-bottom: 2rem;
    font-size: 1.8rem;
}

.card-dark {
    background-color: #393E46; 
    padding: 1.5rem; 
    border-radius: 12px; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
    margin-bottom: 1.5rem;
}

.card-dark h2 {
    color: #DFD0B8;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    border-bottom: 1px dashed #555;
    padding-bottom: 0.5rem;
}

.stats-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
    gap: 1.5rem; 
    margin-bottom: 2rem;
}

.stat-card { 
    background-color: #393E46; 
    padding: 1.5rem; 
    border-radius: 12px; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    border-left: 5px solid #948979; 
}

.stat-value {
    font-size: 2.2rem;
    font-weight: bold;
    color: #DFD0B8;
    margin-bottom: 0.3rem;
}

.stat-label {
    font-size: 0.9rem;
    color: #948979; 
    margin: 0;
}

.accent-text {
    color: #948979; 
}

/* MEGNYÚJTVA 450px-re, hogy legyen hely a feliratnak! */
.chart-card {
    height: 450px; 
    position: relative;
    padding: 2rem;
}

.log-list { 
    list-style: none; 
    padding: 0; 
    margin: 0;
}

.log-list li { 
    padding: 0.75rem 0; 
    border-bottom: 1px solid #484f59; 
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.log-list li:last-child {
    border-bottom: none;
}

.log-list strong {
    color: #DFD0B8;
}

.log-in {
    color: #85b066; 
    font-weight: bold;
}

.log-out {
    color: #d63031; 
    font-weight: bold;
}

.no-data {
    color: #948979;
    font-style: italic;
    padding-top: 1rem;
}
</style>