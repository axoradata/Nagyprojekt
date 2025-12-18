<template>
  <div id="app" class="d-flex min-vh-100 main-bg">
    
    <Sidebar v-if="$route.name !== 'Login'" />

    <main 
      class="flex-grow-1"
      :class="{ 'ms-sidebar': $route.name !== 'Login' }"
    >
      <router-view />
    </main>

  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: { Sidebar },
  methods: {
    // Külön metódusba tesszük, hogy több helyről is meghívhassuk
    applyTheme() {
      const savedTheme = localStorage.getItem('theme') || 'auto';
      
      if (savedTheme === 'auto') {
        // Megnézzük a rendszerszintű beállítást
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      } else {
        // Alkalmazzuk a mentett 'light' vagy 'dark' értéket
        document.documentElement.setAttribute('data-theme', savedTheme);
      }
    }
  },
  mounted() {
    // 1. Első indításkor téma beállítása
    this.applyTheme();

    // 2. Figyeljük, ha a Windows/macOS témát vált, miközben nyitva az oldal
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      // Csak akkor váltunk automatikusan, ha a felhasználó 'auto' módban van
      if (localStorage.getItem('theme') === 'auto' || !localStorage.getItem('theme')) {
        this.applyTheme();
      }
    });

    // 3. Figyeljük a localStorage változásait (opcionális, de hasznos)
    // Ha pl. a Profil oldalon átállítod a témát, ez segít, hogy minden ablak frissüljön
    window.addEventListener('storage', (e) => {
      if (e.key === 'theme') {
        this.applyTheme();
      }
    });
  }
}
</script>

<style>
:root {
  /* SÖTÉT TÉMA (Alapértelmezett) */
  --bg-body: #222831;
  --bg-card: #393E46;
  --bg-inner: #222831;
  --text-main: #DFD0B8;
  --accent: #948979;
  --accent-hover: #7d7264;
  --border-color: #484f59;
  --input-bg: #393E46;
}

[data-theme="light"] {
  /* VILÁGOS TÉMA */
  --bg-body: #f0f2f5;
  --bg-card: #ffffff;
  --bg-inner: #f8f9fa;
  --text-main: #2d3436;
  --accent: #636e72;
  --accent-hover: #2d3436;
  --border-color: #dcdde1;
  --input-bg: #ffffff;
}

/* Általános alapbeállítások minden oldalra */
body {
  margin: 0;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.main-bg {
  background-color: var(--bg-body);
  color: var(--text-main);
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>

<style scoped>
.ms-sidebar {
    margin-left: 240px;
    height: 100vh; 
    overflow-y: auto;
}
</style>