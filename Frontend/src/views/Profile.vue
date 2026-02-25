<template>
  <div class="page-container">
    <div class="page-content-box">
      
      <h2 class="section-title">Profil</h2>
      
      <div class="profile-section mb-5">
        <h3 class="section-subtitle">Információk</h3>
        <hr class="section-divider">

        <div class="data-row">
          <div class="data-label">Teljes név:</div>
          <div class="data-value">{{ user.full_name || 'Betöltés...' }}</div>
        </div>

        <!-- <div class="data-row">
          <div class="data-label">Felhasználónév:</div>
          <div class="data-value">{{ user.username }}</div>
        </div> -->
        
        <div class="data-row">
          <div class="data-label">Kártya azonosító (UID):</div>
          <div class="data-value code-font">{{ user.card_id || 'Nincs adat' }}</div>
        </div>
        
        <div class="data-row">
          <div class="data-label">Beosztás:</div>
          <div class="data-value role-value">{{ user.disposition || 'Nincs adat' }}</div>
        </div>

        <!-- <div class="data-row">
          <div class="data-label">Csoport:</div>
          <div class="data-value">{{ user.group || 'Nincs csoport' }}</div>
        </div> -->
      </div>

      <div class="profile-section">
        <h3 class="section-subtitle">Beállítások és biztonság</h3>
        <hr class="section-divider">
        
        <div class="data-row mb-4">
          <div class="data-label">Megjelenítési mód:</div>
          <div class="data-value">
            <select v-model="selectedTheme" @change="changeTheme" class="form-select custom-input select-theme">
              <option value="light">Világos</option>
              <option value="dark">Sötét</option>
              <option value="auto">Automatikus</option>
            </select>
          </div>
        </div>
        
        <button class="btn custom-btn-primary w-100" type="button" data-bs-toggle="collapse" data-bs-target="#passwordFormCollapse">
          <i class="bi bi-key-fill me-2"></i> Jelszó módosítása
        </button>
        
        <div class="collapse mt-3" id="passwordFormCollapse">
          <div class="card card-body custom-form-bg p-4">
            <h4 class="mb-3">Új jelszó beállítása</h4>
            <form @submit.prevent="updatePassword">
              <div class="mb-3">
                <label class="form-label">Új jelszó</label>
                <input 
                  v-model="passUpdate.new" 
                  type="password" 
                  class="form-control custom-input" 
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Jelszó megerősítése</label>
                <input 
                  v-model="passUpdate.confirm" 
                  type="password" 
                  class="form-control custom-input" 
                  required
                >
              </div>
              <button type="submit" class="btn custom-btn-primary w-100">
                <i class="bi bi-save me-2"></i>Mentés
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// LocalStorage-ból indulunk
const user = ref(JSON.parse(localStorage.getItem('user')) || {})
const selectedTheme = ref(localStorage.getItem('theme') || 'auto')

const applyThemeLogic = () => {
  const theme = selectedTheme.value === 'auto' 
    ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    : selectedTheme.value
  document.documentElement.setAttribute('data-theme', theme)
}

const changeTheme = () => {
  localStorage.setItem('theme', selectedTheme.value)
  applyThemeLogic()
}

const fetchUserInfo = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const response = await axios.get('http://localhost:8000/user/info', {
      params: { token: token }
    })

    if (response.data.status === 1) {
      user.value = {
        ...user.value,
        full_name: response.data.full_name,
        card_id: response.data.card_id,
        disposition: response.data.disposition,
        group: response.data.group
      }
      
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  } catch (error) {
    console.error("Hiba az adatok lekérésekor:", error)
  }
}


const passUpdate = ref({
  new: '',
  confirm: ''
})

const updatePassword = async () => {
  if (passUpdate.value.new !== passUpdate.value.confirm) {
    alert("A két jelszó nem egyezik meg!");
    return;
  }

  const token = localStorage.getItem('token')
  try {
    const response = await axios.post('http://localhost:8000/user/update', null, {
      params: {
        newPass: passUpdate.value.new, // Átírva newPass-ra!
        token: token
      }
    });

    if (response.data.status === 1) {
      alert("Jelszó sikeresen megváltoztatva!");
      passUpdate.value.new = '';
      passUpdate.value.confirm = '';
    } else {
      alert("Hiba: " + response.data.error);
    }
  } catch (e) {
    console.error("Szerverhiba:", e);
    alert("Szerverhiba (500). Nézd meg a Python terminált!");
  }
}

onMounted(() => {
  applyThemeLogic()
  fetchUserInfo()
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

.role-value {
  text-transform: uppercase;
  background: var(--accent);
  color: white !important;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.select-theme {
  min-width: 180px;
  cursor: pointer;
  background-color: var(--bg-card) !important;
  color: var(--text-main) !important;
  border: 1px solid var(--border-color) !important;
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