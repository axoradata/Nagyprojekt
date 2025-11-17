<template>
  <div class="container py-5 d-flex justify-content-center custom-bg">
    
    <div class="card profile-card" style="width: 30rem;">
      
      <div class="profile-header text-center"> 
        <i class="bi bi-person-circle me-2 fs-4"></i>
        <h2 class="h4 mb-0">Felhasználói Profil</h2>
      </div>
      
      <div class="card-body">
        
        <h5 class="mb-3 profile-title">Alap Információk</h5>
        <ul class="list-group list-group-flush mb-4">
          
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <strong>Felhasználónév:</strong>
            <span class="profile-badge">{{ user.username }}</span>
          </li>
          
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <strong>Email:</strong>
            <span class="profile-badge">{{ user.email }}</span>
          </li>
          
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <strong>Szerepkör:</strong>
            <span class="profile-badge">
              {{ user.role }}
            </span>
          </li>
          
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <strong>Regisztrálva:</strong>
            <span class="profile-badge">{{ user.created_at || 'Nincs adat' }}</span>
          </li>
          
        </ul>

        <h5 class="mb-3 profile-title">Beállítások és Biztonság</h5>
        <ul class="list-group list-group-flush mb-4">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <strong>Sötét téma:</strong>
            <div class="form-check form-switch">
              <input class="form-check-input theme-switch" type="checkbox" role="switch" id="darkModeSwitch" checked> 
              <label class="form-check-label light-text" for="darkModeSwitch">Bekapcsolva</label>
            </div>
          </li>
        </ul>
        
        <button 
          class="btn custom-btn-primary w-100" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#passwordFormCollapse" 
        >
          Jelszó módosítása
        </button>
        
        <div class="collapse mt-3" id="passwordFormCollapse">
          <div class="card card-body dark-form-bg">
            <form @submit.prevent="updatePassword">
              <div class="mb-3">
                <label for="newPassword" class="form-label light-text">Új jelszó</label>
                <input type="password" class="form-control dark-input" id="newPassword" required>
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label light-text">Jelszó megerősítése</label>
                <input type="password" class="form-control dark-input" id="confirmPassword" required>
              </div>
              <button type="submit" class="btn custom-btn-primary w-100">Mentés</button>
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

// Jelszómódosítás funkció (csak szimuláció, a háttér logikát kellene megvalósítani)
const updatePassword = () => {
    alert("Jelszó módosítása funkció fut. Frissíteni kell a szerver oldalon!");
}
</script>

<style scoped>
/* --- SZÍNEK ---
#222831: Legsötétebb (Háttér)
#393E46: Sötétszürke (Kártya)
#948979: Sötét Bézs (Kiemelés, Gomb)
#DFD0B8: Világos Bézs (Szöveg)
*/

.custom-bg {
    background-color: #222831;
    min-height: 100vh;
    width: 100%;
    padding-bottom: 50px; 
}

/* --- PROFILKÁRTYA STÍLUSOK --- */
.profile-card {
    background-color: #393E46;
    border: none;
    border-radius: 12px;
    
    /* FINOMÍTOTT SÖTÉT ÁRNYÉK */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(148, 137, 121, 0.1); 
}

.profile-header {
    background-color: #222831;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding: 1.5rem 0;
}
.profile-header h2,
.profile-header i {
    color: #DFD0B8 !important;
}

/* --- LISTA STÍLUSOK --- */
.list-group-item {
    background-color: #393E46;
    border-bottom: 1px solid #222831; 
    padding-left: 0;
}
.list-group-flush > .list-group-item:last-child {
    border-bottom-width: 0;
}

.profile-title {
    color: #DFD0B8 !important;
    border-bottom: 1px solid #948979; 
    padding-bottom: 0.2rem;
}

.list-group-item strong {
    color: #DFD0B8 !important;
}

.profile-badge {
    color: #948979 !important; 
    background-color: transparent !important;
    font-weight: 600;
    padding: 0;
}

/* --- FORMUJELENÍTÉSI STÍLUSOK (Jelszó űrlap) --- */
.dark-form-bg {
    background-color: #222831 !important;
    border-radius: 8px;
    border: 1px solid #484f59; /* Keret a belső kártyának */
}

/* Input és Select mezők */
.form-control.dark-input {
    background-color: #393E46; 
    border-color: #484f59;
    color: #DFD0B8;
    box-shadow: none;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control.dark-input:focus {
    border-color: #948979;
    box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.25); 
    background-color: #393E46; 
}

.light-text {
    color: #DFD0B8 !important;
}

/* --- GOMB ÉS KAPCSOLÓ STÍLUSOK --- */
.custom-btn-primary {
    background-color: #948979;
    border-color: #948979;
    color: white;
    font-weight: 600;
    box-shadow: none;
    transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
}
.custom-btn-primary:hover {
    background-color: #7d7264;
    border-color: #7d7264;
}
.custom-btn-primary:focus {
    box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.5); 
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