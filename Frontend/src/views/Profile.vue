<template>
  <div class="page-container">
    <div class="page-content-box">
      
      <h2 class="section-title">Felhasználói Profil</h2>
      
      <div class="profile-section mb-5">
        <h3 class="section-subtitle">Alap Információk</h3>
        <hr class="section-divider">

        <div class="data-row">
          <div class="data-label">Felhasználónév:</div>
          <div class="data-value">{{ user.username }}</div>
        </div>
        
        <div class="data-row">
          <div class="data-label">Email:</div>
          <div class="data-value">{{ user.email }}</div>
        </div>
        
        <div class="data-row">
          <div class="data-label">Szerepkör:</div>
          <div class="data-value role-value">{{ user.role }}</div>
        </div>
        
        <div class="data-row">
          <div class="data-label">Regisztrálva:</div>
          <div class="data-value">{{ user.created_at || 'Nincs adat' }}</div>
        </div>
      </div>

      <div class="profile-section">
        <h3 class="section-subtitle">Beállítások és Biztonság</h3>
        <hr class="section-divider">
        
        <div class="data-row mb-4">
          <div class="data-label">Megjelenítési mód:</div>
          <div class="data-value">
            <div class="d-flex align-items-center gap-2">              
              <select 
                v-model="selectedTheme" 
                @change="changeTheme" 
                class="form-select custom-input select-theme"
              >
                <option value="light">Világos</option>
                <option value="dark">Sötét</option>
                <option value="auto">Automatikus (Rendszer)</option>
              </select>
            </div>
          </div>
        </div>
        
        <button 
          class="btn custom-btn-primary w-100" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#passwordFormCollapse" 
        >
          <i class="bi bi-key-fill me-2"></i> Jelszó módosítása
        </button>
        
        <div class="collapse mt-3" id="passwordFormCollapse">
          <div class="card card-body custom-form-bg p-4">
            <h4 class="mb-3">Új jelszó beállítása</h4>
            <form @submit.prevent="updatePassword">
              <div class="mb-3">
                <label for="newPassword" class="form-label">Új jelszó</label>
                <input type="password" class="form-control custom-input" id="newPassword" required>
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Jelszó megerősítése</label>
                <input type="password" class="form-control custom-input" id="confirmPassword" required>
              </div>
              <button type="submit" class="btn custom-btn-primary w-100">Mentés és módosítás</button>
            </form>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')) || {})

// Aktuálisan kiválasztott téma (alapértelmezett az 'auto')
const selectedTheme = ref(localStorage.getItem('theme') || 'auto')

const changeTheme = () => {
  // Mentés localStorage-ba
  localStorage.setItem('theme', selectedTheme.value)
  
  // Azonnali alkalmazás (meghívjuk a globális logikát, ami az App.vue-ban is van)
  applyThemeLogic()
}

const applyThemeLogic = () => {
  if (selectedTheme.value === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light')
  } else {
    document.documentElement.setAttribute('data-theme', selectedTheme.value)
  }
}

const updatePassword = () => {
    alert("Jelszó módosítása funkció fut. Frissíteni kell a szerver oldalon!");
}

onMounted(() => {
    applyThemeLogic()
})
</script>

<style scoped>
.page-container {
  padding: 2rem; 
  min-height: 100vh; 
  width: 100%; 
  transition: all 0.3s ease;
  background-color: var(--bg-main);
}

.page-content-box {
  background-color: var(--bg-card); 
  color: var(--text-main); 
  padding: 2.5rem;
  border-radius: 16px;
  width: 100%;
  max-width: 900px; 
  margin: 0 auto;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.section-title {
  color: var(--text-main);
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.5rem;
  margin-bottom: 2.5rem;
  font-size: 1.8rem;
}

.section-subtitle {
  color: var(--text-main);
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
}

.section-divider {
  border-top: 1px solid var(--border-color);
  opacity: 0.5;
  margin-bottom: 1.5rem;
}

.profile-section {
  background-color: var(--bg-inner); 
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.data-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px dashed var(--border-color);
  align-items: center;
}

.profile-section .data-row:last-child {
  border-bottom: none;
}

.data-label {
  color: var(--text-main); 
  opacity: 0.8;
}

.data-value {
  font-weight: 600;
  color: var(--accent); 
}

.select-theme {
  min-width: 180px;
  cursor: pointer;
  background-color: var(--bg-card) !important;
  color: var(--text-main) !important;
  border: 1px solid var(--border-color) !important;
}

.role-value {
  text-transform: uppercase;
}

.custom-form-bg {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
}

.custom-input {
  background-color: var(--bg-inner);
  border-color: var(--border-color);
  color: var(--text-main);
}

.custom-btn-primary {
  background-color: var(--accent);
  border-color: var(--accent);
  color: white;
  font-weight: 600;
  transition: all 0.2s ease;
}

.custom-btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
</style>