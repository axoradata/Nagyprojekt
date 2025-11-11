<template>
  <aside class="sidebar">
    <h2>Belépve: {{ user.username }}</h2>
    <nav>
      <ul>
        <li><router-link to="/dashboard">Dashboard</router-link></li>
        <li><router-link to="/profile">Profil</router-link></li>
        <li v-if="user.role === 'admin'"><router-link to="/users">Felhasználók</router-link></li>
        <li v-if="user.role === 'admin' || user.role === 'leader'"><router-link to="/groups">Csoportok</router-link></li>
        <li v-if="user.role === 'admin'"><router-link to="/logs">Események</router-link></li>
        <li v-if="user.role === 'admin'"><router-link to="/rfid">RFID kezelés</router-link></li>

        <li><button class="btn-logout" @click="logout">Kijelentkezés</button></li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 2rem 0 0 0;
}

nav li {
  margin: 1rem 0;
}

nav a {
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

.btn-logout {
  background-color: #5a7fa4;
  border: none;
  border-radius: 8px;
  padding: 0.7rem;
  color: white;
  cursor: pointer;
  width: 100%;
  font-weight: bold;
}

.btn-logout:hover {
  background-color: #ff7675;
}
</style>
