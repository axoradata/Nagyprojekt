<template>
  <div class="page-container">
    <div class="page-content-box wide-box">
      <h1 class="page-title">RFID kezelés</h1>
      
      <div class="controls-section">
        <input 
          v-model="searchTerm" 
          placeholder="Keresés: név, beosztás vagy kártya ID..." 
          class="custom-input search-input"
        />
        
        <form class="add-form" @submit.prevent="addUser">
          <input v-model="newUser.full_name" placeholder="Felhasználónév" required class="custom-input" />
          <input v-model="newUser.password" placeholder="Jelszó" type="password" required class="custom-input" />
          
          <select v-model="newUser.disposition" required class="custom-input select-role">
            <option disabled value="">Beosztás kiválasztása</option>
            <option value="admin">Admin</option>
            <option value="team_leader">Csoportvezető</option>
            <option value="employee">Dolgozó</option>
          </select>
          
          <input v-model="newUser.card_id" placeholder="Kártya ID" required class="custom-input" />
          
          <button type="submit" class="btn custom-btn-primary add-btn">
            <i class="bi bi-plus-circle me-1"></i> Hozzáadás
          </button>
        </form>
      </div>
      
      <div class="table-responsive">
        <table class="data-table user-table">
          <colgroup>
            <col style="width: 35%;"> <col style="width: 20%;"> <col style="width: 30%;"> <col style="width: 15%;"> </colgroup>
          <thead>
            <tr>
              <th>Név</th>
              <th>Beosztás</th>
              <th>Kártya ID</th>
              <th>Műveletek</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="4" class="text-center">Adatok betöltése...</td>
            </tr>
            
            <tr v-for="user in filteredUsers" :key="user.card_id">
              <td class="text-truncate">{{ user.full_name }}</td>
              <td><span class="badge role-badge">{{ user.disposition }}</span></td>
              <td><code>{{ user.card_id }}</code></td>
              <td class="action-cell">
                <button class="btn btn-sm delete-btn" @click="deleteUser(user.card_id)" title="Törlés">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>

            <tr v-if="!loading && filteredUsers.length === 0">
              <td colspan="4" class="text-center">Nincs megjeleníthető adat.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const usersList = ref([])
const searchTerm = ref('')
const loading = ref(true)

const newUser = ref({
  full_name: '',
  password: '',
  disposition: '',
  card_id: ''
})

const fetchUsers = async () => {
  loading.value = true
  const token = localStorage.getItem('token')
  
  try {
    const response = await axios.get('http://localhost:8000/user/all', { 
      params: { token: token } 
    })
    
    if (response.data.status === 1) {
      usersList.value = response.data.users 
    } else {
      console.warn("Hiba:", response.data.message)
      usersList.value = []
    }
  } catch (e) {
    console.error("Hálózati hiba:", e)
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  const search = searchTerm.value.toLowerCase()
  return usersList.value.filter(u =>
    (u.full_name?.toLowerCase().includes(search)) ||
    (u.card_id?.toLowerCase().includes(search)) ||
    (u.disposition?.toLowerCase().includes(search))
  )
})

const addUser = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.post('http://localhost:8000/user/register', null, {
      params: {
        card_id: newUser.value.card_id,
        disposition: newUser.value.disposition,
        full_name: newUser.value.full_name,
        password: newUser.value.password,
        token: token
      }
    })

    if (response.data.status === 1) {
      alert("Sikeres hozzáadás!")
      // Csak azokat ürítjük, amik az inputban voltak
      newUser.value = { full_name: '', password: '', disposition: '', card_id: '' }
      fetchUsers()
    } else {
      alert("Hiba: " + (response.data.message || "Sikertelen regisztráció"))
    }
  } catch (e) {
    alert("Szerverhiba! Ellenőrizd a Backend futását.")
  }
}

const deleteUser = async (card_id) => {
  if (!confirm("Biztosan törölni szeretnéd?")) return
  const token = localStorage.getItem('token')
  try {
    const response = await axios.delete('http://localhost:8000/user/delete', {
      params: { card_id, token }
    })
    if (response.data.status === 1) {
      fetchUsers()
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page-container {
  padding: 2rem;
  min-height: 100vh;
  width: 100%;
  transition: background-color 0.3s ease;
}

.page-content-box {
  background-color: var(--bg-card);
  color: var(--text-main);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  color: var(--text-main);
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.controls-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.search-input {
  max-width: 400px;
}

.add-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  background-color: var(--bg-inner);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.custom-input {
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  background-color: var(--bg-card);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.custom-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(148, 137, 121, 0.2);
  outline: none;
}

/* --- TÁBLÁZAT FIXÁLÁSA --- */
.table-responsive {
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  /* Megakadályozza az oszlopok ugrálását szűréskor */
  table-layout: fixed; 
}

.user-table th {
  padding: 1rem;
  background-color: var(--bg-inner);
  color: var(--text-main);
  border-bottom: 2px solid var(--accent);
  text-align: left;
  white-space: nowrap;
}

.user-table td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid var(--border-color);
  vertical-align: middle;
  /* Szöveg levágása, ha nem férne ki a fix szélességben */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-table tbody tr:nth-child(even) {
  background-color: rgba(148, 137, 121, 0.03);
}

.user-table tbody tr:hover {
  background-color: rgba(148, 137, 121, 0.08);
}

.role-badge {
  background-color: var(--accent);
  color: white;
  padding: 0.4rem 0.6rem;
  font-size: 0.75rem;
  text-transform: uppercase;
}

code {
  color: var(--accent);
  background-color: var(--bg-inner);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

/* --- GOMBOK --- */
.custom-btn-primary {
  background-color: var(--accent);
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 8px;
}

.action-cell {
  display: flex;
  gap: 0.4rem;
}

.btn-sm {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: transform 0.2s;
  border: none;
  cursor: pointer;
}

.btn-sm:hover { transform: scale(1.1); color: white; }

.delete-btn { background-color: #e74c3c; color: white; }
</style>