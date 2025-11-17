<template>
  <div class="layout-dark">
    <main class="main-content-dark">
      <h1 class="page-title">Üdv, {{ user.username }}! 👋</h1>

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
          <h2>Heti Munkaidő Eloszlás (Gantt-szerű)</h2>
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
import { onMounted, computed, ref, nextTick } from 'vue'
import { users, logins, groups } from '../data'
import Chart from 'chart.js/auto'; 

const user = JSON.parse(localStorage.getItem('user') || '{}')
let chartInstance = null; 

// --- DÁTUM SEGÉDFÜGGVÉNYEK ---

// A mock adatok dátumformátumának parsolása.
const parseLogTime = (logTimeString) => {
    if (!logTimeString) return null;
    const parsable = logTimeString.replace(/(\d{4})\. (\d{2})\. (\d{2})\./, '$1/$2/$3').trim();
    return new Date(parsable);
};

// Visszaadja a nap 0:00:00 időpontját
const startOfDay = (date) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d;
};

// Órává konvertálja az időpontot (0-24 skálán)
const hoursFromStartOfDay = (date) => {
    if (!date) return 0;
    const sod = startOfDay(date);
    return (date.getTime() - sod.getTime()) / (1000 * 60 * 60); // ms -> óra
};

// --- MUNKAIDŐ SZÁMÍTÁSOK ---

// Kiszámítja a ledolgozott időt órában
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
            clockInTime = null; // Páros lezárva
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
  const userCardId = user.card_id;

  return logins.filter(log => {
    if(user.role === 'admin') return true
    
    if(user.role === 'leader') {
      const supervisedMembersCardIds = groups
        .filter(g => g.leader_id === user.id)
        .flatMap(g => g.members)
        .map(memberId => users.find(u => u.id === memberId)?.card_id)
        .filter(id => id);
      
      return supervisedMembersCardIds.includes(log.card_id) || log.card_id == userCardId;
    }
    
    if(user.role === 'worker') {
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
    if (user.role !== 'leader') return 0;
    const members = groups
        .filter(g => g.leader_id === user.id)
        .flatMap(g => g.members);
    return new Set(members).size;
});

const myWeeklyWorkHours = computed(() => {
    if (user.role !== 'worker') return 0;
    
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const relevantLogs = filteredLogs.value.filter(log => {
        const logDate = parseLogTime(log.time);
        if (!logDate) return false;
        return logDate > oneWeekAgo; 
    });

    const ownLogs = relevantLogs.filter(log => log.card_id == user.card_id);
    const totalHours = calculateWorkDuration(ownLogs);

    return totalHours.toFixed(1);
});


// 6. Heti Munkaidő Eloszlás Adatok (Range Bar Chart)
const weeklyChartData = computed(() => {
    const dayMap = {}; // Nap/dátum -> logok listája

    // 1. Csoportosítás nap szerint (utolsó 7 nap)
    const today = startOfDay(new Date());
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(today.getDate() - 6);

    filteredLogs.value.forEach(log => {
        const logDate = parseLogTime(log.time);
        if (!logDate || logDate < sevenDaysAgo) return;

        const dateKey = startOfDay(logDate).toISOString().slice(0, 10); 
        
        if (!dayMap[dateKey]) {
            dayMap[dateKey] = [];
        }
        dayMap[dateKey].push(log);
    });

    // 2. Kiszámoljuk minden napra a munkaidő blokkokat (Range-eket)
    const allWorkRanges = []; // Minden egyes munkaidő blokk egy [start, end] tömb lesz
    const daysLabels = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap'];
    
    const todayDayIndex = today.getDay(); // 0=V, 1=H, ...
    // Kiszámítjuk a Hétfő offsetet (ha ma Hétfő (1), akkor offset 0, ha Kedd (2), akkor 1, ha Vasárnap (0), akkor 6)
    const mondayOffset = todayDayIndex === 0 ? 6 : todayDayIndex - 1; 

    for(let i = 0; i < 7; i++) {
        const day = new Date(today);
        // Beállítjuk az aktuális napot a 7 napos ciklusban (i=0 -> Hétfő)
        day.setDate(today.getDate() - mondayOffset + i); 
        const dateKey = day.toISOString().slice(0, 10);
        
        const dayLogs = dayMap[dateKey] || [];
        
        const sortedLogs = [...dayLogs].sort((a, b) => parseLogTime(a.time) - parseLogTime(b.time));
        
        let clockInTime = null;

        // Iterálunk a logokon és keressük a párokat
        sortedLogs.forEach(log => {
            const currentTime = parseLogTime(log.time);
            if (!currentTime) return;

            if (log.log_IN) {
                clockInTime = currentTime;
            } else if (clockInTime) {
                // Kilépés, van előző belépés -> Range Bar adatpont generálása
                const startHour = hoursFromStartOfDay(clockInTime);
                const endHour = hoursFromStartOfDay(currentTime);
                
                if (endHour > startHour) {
                    allWorkRanges.push({
                        x: daysLabels[i], // X tengelyen a nap neve
                        y: [startHour, endHour] // Y tengelyen az időtartomány [kezdőóra, végóra]
                    });
                }
                clockInTime = null;
            }
        });
    }

    // A Range Bar chart egyetlen dataset-et használ, ahol minden adatpont egy tartomány.
    return { 
        labels: daysLabels, // Az X tengelyen lévő kategóriák (Napok)
        datasets: [
            {
                label: 'Munkaidő Blokkok',
                data: allWorkRanges,
                backgroundColor: '#948979',
                borderColor: '#DFD0B8',
                borderWidth: 1,
                borderRadius: 5,
            }
        ]
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
        type: 'bar', // Bar chart típus
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x', // X tengelyen a napok (oszlopdiagram, ami vertikálisan mutatja az időt)
            scales: {
                // Y tengely: A nap 24 órája (0:00-tól 24:00-ig)
                y: {
                    min: 0,
                    max: 24,
                    title: {
                        display: true,
                        text: 'A Nap Órái',
                        color: '#DFD0B8'
                    },
                    // Az idő tengely fordított, hogy 0:00 legyen felül (mint az órarendeken)
                    reverse: true,
                    grid: { color: 'rgba(223, 208, 184, 0.1)' },
                    ticks: { 
                        color: '#DFD0B8', 
                        stepSize: 1, // Óránkénti jelölés
                        callback: function(value) {
                             // Óra + :00 formátum
                            return `${Math.floor(value).toString().padStart(2, '0')}:00`; 
                        }
                    }
                },
                // X tengely: A napok kategóriái
                x: {
                    grid: { color: 'rgba(223, 208, 184, 0.1)' },
                    ticks: { color: '#DFD0B8' }
                }
            },
            plugins: {
                legend: { display: false }, // Nincs szükség jelmagyarázatra, csak 1 adatsor van
                tooltip: { 
                    backgroundColor: '#222831', 
                    titleColor: '#DFD0B8', 
                    bodyColor: '#DFD0B8',
                    callbacks: {
                        // Tooltip testreszabása: Munkaidő blokk [kezdőóra:végóra]
                        label: function(context) {
                            const range = context.parsed._custom; // A range bar értéke [start, end]
                            if (range && Array.isArray(range) && range.length === 2) {
                                const startH = Math.floor(range[0]).toString().padStart(2, '0');
                                const startM = Math.round((range[0] % 1) * 60).toString().padStart(2, '0');
                                
                                const endH = Math.floor(range[1]).toString().padStart(2, '0');
                                const endM = Math.round((range[1] % 1) * 60).toString().padStart(2, '0');

                                return `Munkaidő: ${startH}:${startM} - ${endH}:${endM}`;
                            }
                            return 'Nincs adat';
                        }
                    }
                }
            }
        }
    });
};

onMounted(() => {
    nextTick(() => {
        initializeChart();
    });
});
</script>

<style scoped>
/* A CSS stílusok változatlanok maradnak */
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

.chart-card {
    height: 400px; 
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