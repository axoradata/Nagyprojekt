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

<!-- <style>
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
</style> -->

<style>
:root {
  /* VILÁGOS MÓD - A kép menta és fehér erezete alapján */
  --bg-body: #d9e7e0;        /* Világos mentazöld (a kép alapszíne) */
  --bg-card: rgba(255, 255, 255, 0.8); /* "Frosted glass" üveghatás */
  --bg-inner: #f1f7f4;       /* Extra világos menta az inputoknak */
  --text-main: #2a3b32;      /* Sötét smaragd szöveg */
  --accent: #5e8c76;         /* Közép-menta gombok (a kép sötétebb erei) */
  --accent-hover: #4a6f5d;
  --border-color: rgba(255, 255, 255, 0.4);
  
  /* Formák */
  --radius-xl: 40px;
  --radius-md: 15px;
}

[data-theme="dark"] {
  /* SÖTÉT MÓD - A kép legsötétebb smaragd árnyalatai alapján */
  --bg-body: #16241d;        /* Mély, majdnem fekete smaragdzöld */
  --bg-card: rgba(28, 43, 35, 0.9); 
  --bg-inner: #1f3329;
  --text-main: #d1e2d8;      /* Világos menta szöveg */
  --accent: #76a58f;         /* Világosabb menta gombok sötétben */
  --accent-hover: #8fc2ab;
  --border-color: rgba(255, 255, 255, 0.1);
}

/* Alapbeállítások a kép alkalmazásához */
.main-bg {
  position: relative;
  background-color: var(--bg-body);
  color: var(--text-main);
  /* IDE TEDD A KÉPEDET: */
  background-repeat: repeat;
  background-image: url('./assets/zold-arany-selyem2.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  z-index: 1;
}

/* Árnyékoló réteg, hogy a szöveg mindig olvasható legyen a képen */
.main-bg::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  /* Lágy átmenet, hogy a kép ne legyen túl zavaró a szöveg alatt */
  background: radial-gradient(circle at center, transparent 0%, var(--bg-body) 100%);
  opacity: 0.4;
  z-index: -1;
  pointer-events: none;
}

/* Alkalmazzuk a színeket a komponensekre */
.auth-box {
  background-color: var(--bg-card) !important;
  backdrop-filter: blur(15px); /* Ez teszi "üvegessé" a dobozt */
  border-radius: var(--radius-xl) !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1) !important;
}

.custom-input {
  background-color: var(--bg-inner) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-main) !important;
}

.custom-btn-primary {
  background-color: var(--accent) !important;
  color: white !important;
  border-radius: var(--radius-md) !important;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 10px 20px rgba(94, 140, 118, 0.2);
}

.custom-btn-primary:hover {
  background-color: var(--accent-hover) !important;
  transform: translateY(-1px);
}
</style>

<style scoped>
.ms-sidebar {
    margin-left: 240px;
    height: 100vh; 
    overflow-y: auto;
}
</style>