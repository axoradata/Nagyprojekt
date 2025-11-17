<template>
  <div class="page-container-dark">
    <div class="page-content-box wide-box">
      <h1 class="page-title">RFID Kezelés / Felhasználók</h1>
      
      <div class="controls-section">
        <input 
          v-model="searchTerm" 
          placeholder="Keresés: Név, Email vagy Kártya ID..." 
          class="dark-input search-input"
        />
        
        <form class="add-form" @submit.prevent="addUser">
          <input v-model="newUser.username" placeholder="Felhasználónév" required class="dark-input" />
          <input v-model="newUser.email" placeholder="Email" type="email" required class="dark-input" />
          <input v-model="newUser.password" placeholder="Jelszó" type="password" required class="dark-input" />
          <select v-model="newUser.role" required class="dark-input select-role">
            <option disabled value="">Szerep</option>
            <option value="admin">Admin</option>
            <option value="leader">Csoportvezető</option>
            <option value="worker">Dolgozó</option>
          </select>
          <input v-model="newUser.card_id" placeholder="Kártya ID" required class="dark-input" />
          <button type="submit" class="btn custom-btn-primary add-btn"><i class="bi bi-plus-circle me-1"></i> Hozzáadás</button>
        </form>
      </div>
      
      <table class="data-table user-table">
        <thead>
          <tr>
            <th>Név</th>
            <th>Email</th>
            <th>Szerep</th>
            <th>Kártya ID</th>
            <th>Műveletek</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <template v-if="editingId === user.id">
              <td><input v-model="editUser.username" class="dark-input" /></td>
              <td><input v-model="editUser.email" type="email" class="dark-input" /></td>
              <td>
                <select v-model="editUser.role" class="dark-input">
                  <option value="admin">Admin</option>
                  <option value="leader">Csoportvezető</option>
                  <option value="worker">Dolgozó</option>
                </select>
              </td>
              <td><input v-model="editUser.card_id" class="dark-input" /></td>
              <td>
                <button class="btn btn-sm save-btn" @click="saveEdit(user.id)">
                  <i class="bi bi-save"></i> Mentés
                </button>
                <button class="btn btn-sm cancel-btn" @click="cancelEdit">
                  <i class="bi bi-x-circle"></i> Mégsem
                </button>
              </td>
            </template>
            <template v-else>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>{{ user.card_id }}</td>
              <td>
                <button class="btn btn-sm edit-btn" @click="startEdit(user)">
                  <i class="bi bi-pencil-square"></i> Módosítás
                </button>
                <button class="btn btn-sm delete-btn" @click="deleteUser(user.id)">
                  <i class="bi bi-trash"></i> Törlés
                </button>
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { users } from '../data'

// --- ÁLLAPOTOK ---
const user = JSON.parse(localStorage.getItem('user') || '{}')
const usersList = ref([...users]) // Reaktív felhasználó lista
const searchTerm = ref('') // Keresési feltétel
const editingId = ref(null) // Szerkesztés alatt lévő user ID-ja
const editUser = ref({}) // Szerkesztés alatt lévő user adatai

const newUser = ref({
  username: '',
  email: '',
  password: '', // Jelszó kezelése a háttérben történne, itt csak a mező van
  role: '',
  card_id: ''
})

// --- SZÁMÍTOTT TULAJDONSÁGOK (Keresés/Szűrés) ---
const filteredUsers = computed(() => {
  if (!searchTerm.value) {
    return usersList.value
  }
  const search = searchTerm.value.toLowerCase()
  return usersList.value.filter(u =>
    u.username.toLowerCase().includes(search) ||
    u.email.toLowerCase().includes(search) ||
    u.card_id.toLowerCase().includes(search)
  )
})

// --- CRUD FÜGGVÉNYEK ---
const addUser = () => {
  if (newUser.value.username && newUser.value.email && newUser.value.role && newUser.value.card_id) {
    const id = usersList.value.length ? Math.max(...usersList.value.map(u => u.id)) + 1 : 1
    const userToAdd = { id, ...newUser.value, created_at: new Date().toLocaleDateString() }
    
    // Először keressük meg, hogy a kártya ID létezik-e már
    const existingCard = usersList.value.some(u => u.card_id === newUser.value.card_id);
    if (existingCard) {
        alert("Ez a Kártya ID már hozzá van rendelve egy felhasználóhoz!");
        return; 
    }

    usersList.value.push(userToAdd)
    
    // Alapállapot visszaállítása
    newUser.value = { username: '', email: '', password: '', role: '', card_id: '' }
  } else {
      alert("Kérjük, töltse ki az összes mezőt!");
  }
}

const deleteUser = (id) => {
  if (confirm('Biztosan törölni szeretnéd ezt a felhasználót?')) {
    usersList.value = usersList.value.filter(u => u.id !== id)
  }
}

// --- MÓDOSÍTÁS FÜGGVÉNYEK ---
const startEdit = (user) => {
  editingId.value = user.id
  // Mély másolat készítése a szerkesztéshez
  editUser.value = { ...user } 
}

const cancelEdit = () => {
  editingId.value = null
  editUser.value = {}
}

const saveEdit = (id) => {
  const index = usersList.value.findIndex(u => u.id === id)
  if (index !== -1) {
    // Frissítés
    usersList.value[index] = { ...editUser.value }
    cancelEdit() // Szerkesztés befejezése
  }
}
</script>

<style scoped>
/* --- FŐ ELRENDEZÉS ÉS HÁTTÉR --- */
.page-container-dark {
  background-color: #222831; 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100%; 
  width: 100%; 
}

.page-content-box {
  background-color: #393E46; 
  color: #DFD0B8; 
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  /* Táblázat miatt szélesebb konténer */
  width: 1200px; 
  max-width: 100%; 
}

.page-title {
    color: #DFD0B8;
    border-bottom: 2px solid #948979;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
}

/* --- VEZÉRLŐ ELEMEK (KERESÉS ÉS HOZZÁADÁS) --- */
.controls-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.search-input {
    width: 100%;
    max-width: 400px;
    padding: 0.7rem;
    font-size: 1rem;
}

.add-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  /* Kényszerítjük, hogy a gomb a végére kerüljön */
  align-items: center; 
}

/* --- INPUT/SELECT ÁLTALÁNOS STÍLUSOK (SÖTÉT TÉMÁHOZ) --- */
.dark-input {
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  background-color: #222831; /* Legsötétebb háttér */
  color: #DFD0B8; /* Világos szöveg */
  border: 1px solid #393E46; 
  transition: 0.2s;
}

.dark-input:focus {
  border-color: #948979; /* Kiemelő szín fókuszban */
  box-shadow: 0 0 6px rgba(148, 137, 121, 0.4);
}

.add-form input,
.add-form select {
    flex-grow: 1; /* Kitöltik a helyet */
}

.select-role {
    min-width: 150px;
}

/* --- TÁBLÁZAT STÍLUSOK --- */
.user-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #393E46; 
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.user-table th {
  padding: 0.8rem 1rem;
  text-align: left;
  background-color: #222831; /* Legsötétebb fejléchez */
  color: #DFD0B8;
  border-bottom: 2px solid #948979; /* Kiemelő színű elválasztó */
}

.user-table td {
  padding: 0.7rem 1rem;
  text-align: left;
  border-bottom: 1px solid #484f59; /* Sötétebb szürke vonal */
  color: #DFD0B8;
  vertical-align: middle;
}

/* Páros sorok háttérszíne */
.user-table tbody tr:nth-child(even) {
    background-color: #333940; 
}

/* Hover effektus */
.user-table tbody tr:hover {
    background-color: #484f59;
}

/* --- GOMB STÍLUSOK --- */
.custom-btn-primary {
  background-color: #948979;
  border: none;
  color: white;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s;
}
.custom-btn-primary:hover {
  background-color: #7d7264;
}

/* Műveleti gombok (Edit, Delete, Save, Cancel) */
.btn-sm {
    padding: 0.3rem 0.6rem;
    font-size: 0.9rem;
    margin-left: 0.5rem;
}

.edit-btn {
    background-color: #948979;
    color: white;
}
.edit-btn:hover {
    background-color: #7d7264;
}

.delete-btn {
    background-color: #d63031; /* Piros */
    color: white;
}
.delete-btn:hover {
    background-color: #a82425;
}

.save-btn {
    background-color: #4CAF50; /* Zöld */
    color: white;
    margin-left: 0; /* Ne legyen dupla margó */
}
.save-btn:hover {
    background-color: #388E3C;
}

.cancel-btn {
    background-color: #7f8c8d; /* Szürke */
    color: white;
}
.cancel-btn:hover {
    background-color: #616a6b;
}

/* Inputok a szerkesztési módban */
.user-table td input,
.user-table td select {
    padding: 0.3rem 0.5rem;
    font-size: 0.9rem;
    width: 100%;
    box-sizing: border-box;
}

</style>