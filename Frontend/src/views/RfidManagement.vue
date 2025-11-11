<template>
  <div class="layout">
    <Sidebar />
    <main class="main-content">
      <h1>RFID Kezelés / Felhasználók</h1>

      <form class="add-form" @submit.prevent="addUser">
        <input v-model="newUser.username" placeholder="Felhasználónév" required />
        <input v-model="newUser.email" placeholder="Email" type="email" required />
        <input v-model="newUser.password" placeholder="Jelszó" type="password" required />
        <select v-model="newUser.role" required>
          <option disabled value="">Szerep</option>
          <option value="admin">Admin</option>
          <option value="leader">Csoportvezető</option>
          <option value="worker">Dolgozó</option>
        </select>
        <input v-model="newUser.card_id" placeholder="Kártya ID" required />
        <button type="submit">Hozzáadás</button>
      </form>

      <table class="user-table">
        <thead>
          <tr>
            <th>Név</th>
            <th>Email</th>
            <th>Szerep</th>
            <th>Kártya ID</th>
            <th>Művelet</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in usersList" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.card_id }}</td>
            <td>
              <button class="delete-btn" @click="deleteUser(user.id)">🗑 Törlés</button>
            </td>
          </tr>
        </tbody>
      </table>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { users } from '../data'

const user = JSON.parse(localStorage.getItem('user') || '{}')

// Felhasználók listája (reaktív másolat)
const usersList = ref([...users])

const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: '',
  card_id: ''
})

// Új felhasználó hozzáadása
const addUser = () => {
  const id = usersList.value.length ? Math.max(...usersList.value.map(u => u.id)) + 1 : 1
  const userToAdd = { id, ...newUser.value }
  usersList.value.push(userToAdd)

  // Alapállapot visszaállítása
  newUser.value = { username: '', email: '', password: '', role: '', card_id: '' }
}

const deleteUser = (id) => {
  usersList.value = usersList.value.filter(u => u.id !== id)
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background: #f1f2f6;
  color: #2d3436;
}

.add-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.add-form input,
.add-form select {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #b2bec3;
}

.add-form button {
  background: #2d3436;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s;
}

.add-form button:hover {
  background: #74b9ff;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dfe6e9;
}

th {
  background: #2c3e50;
  color: white;
}

.delete-btn {
  background: #5a7fa4;
  color: white;
  border: none;
  padding: 0.4rem 0.7rem;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.delete-btn:hover {
  background: #ff7675;
}

</style>
