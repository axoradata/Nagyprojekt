<template>
  <div class="page-container-dark">
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
          <div class="data-label">Sötét téma:</div>
          <div class="data-value">
            <div class="form-check form-switch">
              <input class="form-check-input theme-switch" type="checkbox" role="switch" id="darkModeSwitch" checked> 
              <label class="form-check-label light-text" for="darkModeSwitch">Bekapcsolva</label>
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
          <div class="card card-body dark-form-bg p-4">
            <h4 class="light-text mb-3">Új jelszó beállítása</h4>
            <form @submit.prevent="updatePassword">
              <div class="mb-3">
                <label for="newPassword" class="form-label light-text">Új jelszó</label>
                <input type="password" class="form-control dark-input" id="newPassword" required>
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label light-text">Jelszó megerősítése</label>
                <input type="password" class="form-control dark-input" id="confirmPassword" required>
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
import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')) || {})

const updatePassword = () => {
    alert("Jelszó módosítása funkció fut. Frissíteni kell a szerver oldalon!");
}
</script>

<style scoped>
/* --- KÜLSŐ ELRENDEZÉS STÍLUSOK (Logs.vue alapján) --- */
.page-container-dark {
  background-color: #222831; 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100vh; 
  width: 100%; 
}

.page-content-box {
  background-color: #393E46; 
  color: #DFD0B8; 
  padding: 2.5rem; /* Kicsit több padding */
  border-radius: 16px;
  
  /* EGYSÉGES SZÉLESSÉG */
  width: 900px; 
  max-width: 95%; 
  
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  display: block; 
}

/* --- SZAKASZCÍMEK STÍLUSAI --- */
.section-title {
  color: #DFD0B8;
  border-bottom: 2px solid #948979;
  padding-bottom: 0.5rem;
  margin-bottom: 2.5rem;
  font-size: 1.8rem;
}

.section-subtitle {
  color: #DFD0B8;
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
}

.section-divider {
  border-top: 1px solid #222831;
  opacity: 1;
  margin-bottom: 1.5rem;
}

/* --- PROFIL ADATOK (List helyett blokk) --- */
.profile-section {
  background-color: #333940; /* Sötétebb háttér a szekcióknak */
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid #484f59;
}

.data-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px dashed #484f59; /* Finom elválasztó vonal */
  align-items: center;
}
.profile-section .data-row:last-child {
  border-bottom: none;
}

.data-label {
  font-weight: 400;
  color: #DFD0B8; 
}

.data-value {
  font-weight: 600;
  color: #948979; /* Kiemelő szín */
}

.role-value {
  text-transform: uppercase;
}

/* --- JELSZÓ ŰRLAP és GOMB STÍLUSOK --- */
.dark-form-bg {
  background-color: #222831 !important;
  border: 1px solid #484f59;
}

.form-control.dark-input {
  background-color: #393E46; 
  border-color: #484f59;
  color: #DFD0B8;
}
.form-control.dark-input:focus {
  border-color: #948979;
  box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.25); 
}

.light-text {
  color: #DFD0B8 !important;
}

.custom-btn-primary {
  background-color: #948979;
  border-color: #948979;
  color: white;
  font-weight: 600;
}
.custom-btn-primary:hover {
  background-color: #7d7264;
  border-color: #7d7264;
}

/* Téma kapcsoló */
.form-check-input.theme-switch:checked {
  background-color: #948979;
  border-color: #948979;
}
.form-check-input.theme-switch:focus {
  box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.5);
}
</style>