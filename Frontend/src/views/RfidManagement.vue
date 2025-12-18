<template>
  <div class="page-container">
    <div class="page-content-box wide-box">
      <h1 class="page-title">RFID Kezelés / Felhasználók</h1>
      
      <div class="controls-section">
        <input 
          v-model="searchTerm" 
          placeholder="Keresés: Név, Email vagy Kártya ID..." 
          class="custom-input search-input"
        />
        
        <form class="add-form" @submit.prevent="addUser">
          <input v-model="newUser.username" placeholder="Felhasználónév" required class="custom-input" />
          <input v-model="newUser.email" placeholder="Email" type="email" required class="custom-input" />
          <input v-model="newUser.password" placeholder="Jelszó" type="password" required class="custom-input" />
          <select v-model="newUser.role" required class="custom-input select-role">
            <option disabled value="">Szerep</option>
            <option value="admin">Admin</option>
            <option value="leader">Csoportvezető</option>
            <option value="worker">Dolgozó</option>
          </select>
          <input v-model="newUser.card_id" placeholder="Kártya ID" required class="custom-input" />
          <button type="submit" class="btn custom-btn-primary add-btn">
            <i class="bi bi-plus-circle me-1"></i> Hozzáadás
          </button>
        </form>
      </div>
      
      <div class="table-responsive">
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
                <td><input v-model="editUser.username" class="custom-input table-input" /></td>
                <td><input v-model="editUser.email" type="email" class="custom-input table-input" /></td>
                <td>
                  <select v-model="editUser.role" class="custom-input table-input">
                    <option value="admin">Admin</option>
                    <option value="leader">Csoportvezető</option>
                    <option value="worker">Dolgozó</option>
                  </select>
                </td>
                <td><input v-model="editUser.card_id" class="custom-input table-input" /></td>
                <td class="action-cell">
                  <button class="btn btn-sm save-btn" @click="saveEdit(user.id)">
                    <i class="bi bi-save"></i>
                  </button>
                  <button class="btn btn-sm cancel-btn" @click="cancelEdit">
                    <i class="bi bi-x-circle"></i>
                  </button>
                </td>
              </template>
              <template v-else>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td><span class="badge role-badge">{{ user.role }}</span></td>
                <td><code>{{ user.card_id }}</code></td>
                <td class="action-cell">
                  <button class="btn btn-sm edit-btn" @click="startEdit(user)" title="Módosítás">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button class="btn btn-sm delete-btn" @click="deleteUser(user.id)" title="Törlés">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { users } from '../data'

const usersList = ref([...users])
const searchTerm = ref('')
const editingId = ref(null)
const editUser = ref({})

const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: '',
  card_id: ''
})

const filteredUsers = computed(() => {
  if (!searchTerm.value) return usersList.value
  const search = searchTerm.value.toLowerCase()
  return usersList.value.filter(u =>
    u.username.toLowerCase().includes(search) ||
    u.email.toLowerCase().includes(search) ||
    u.card_id.toLowerCase().includes(search)
  )
})

const addUser = () => {
  if (newUser.value.username && newUser.value.email && newUser.value.role && newUser.value.card_id) {
    const existingCard = usersList.value.some(u => u.card_id === newUser.value.card_id);
    if (existingCard) {
        alert("Ez a Kártya ID már hozzá van rendelve egy felhasználóhoz!");
        return; 
    }
    const id = usersList.value.length ? Math.max(...usersList.value.map(u => u.id)) + 1 : 1
    usersList.value.push({ id, ...newUser.value, created_at: new Date().toLocaleDateString() })
    newUser.value = { username: '', email: '', password: '', role: '', card_id: '' }
  }
}

const deleteUser = (id) => {
  if (confirm('Biztosan törölni szeretnéd ezt a felhasználót?')) {
    usersList.value = usersList.value.filter(u => u.id !== id)
  }
}

const startEdit = (user) => {
  editingId.value = user.id
  editUser.value = { ...user } 
}

const cancelEdit = () => {
  editingId.value = null
  editUser.value = {}
}

const saveEdit = (id) => {
  const index = usersList.value.findIndex(u => u.id === id)
  if (index !== -1) {
    usersList.value[index] = { ...editUser.value }
    cancelEdit()
  }
}
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

/* --- TÁBLÁZAT --- */
.table-responsive {
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.user-table th {
  padding: 1rem;
  background-color: var(--bg-inner);
  color: var(--text-main);
  border-bottom: 2px solid var(--accent);
  text-align: left;
}

.user-table td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid var(--border-color);
  vertical-align: middle;
}

.user-table tbody tr:nth-child(even) {
  background-color: rgba(var(--accent-rgb, 148, 137, 121), 0.03);
}

.user-table tbody tr:hover {
  background-color: rgba(var(--accent-rgb, 148, 137, 121), 0.08);
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
}

/* --- GOMBOK --- */
.custom-btn-primary {
  background-color: var(--accent);
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
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
}

.btn-sm:hover { transform: scale(1.1); color: white; }

.edit-btn { background-color: var(--accent); color: white; }
.delete-btn { background-color: #e74c3c; color: white; }
.save-btn { background-color: #2ecc71; color: white; }
.cancel-btn { background-color: #95a5a6; color: white; }

.table-input {
  padding: 0.3rem 0.5rem;
  font-size: 0.85rem;
}
</style>