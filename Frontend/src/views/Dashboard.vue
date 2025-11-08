<template>
  <div class="layout">
    <Sidebar />
    <div class="dashboard">
      <h1>Üdv, {{ user.username }}!</h1>
      <p>Szereped: {{ user.role }}</p>
      <button @click="logout">Kijelentkezés</button>
    </div>
  </div>
</template>

<script>
import { roles } from '../data'
import Sidebar from '../components/Sidebar.vue'

export default {
  components: {
    Sidebar
  },

  name: 'Dashboard',
  data() {
    return {
      user: null
    }
  },
  created() {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      this.user = JSON.parse(storedUser)
      const role = roles.find(r => r.id === parseInt(this.user.role_id))
      if (role) {
        this.user.role = role.role  // hozzáadjuk a user objektumhoz a role nevet
      }
    } else {
      // ha nincs bejelentkezett user, visszairányít a loginra
      this.$router.push('/login')
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh; /* teljes képernyőmagasság */
}

.dashboard {
  flex-grow: 1; /* a dashboard kitölti a maradék helyet */
  padding: 40px;
  text-align: center;
  background: #f5f5f5;
  overflow-y: auto;
}

button {
  padding: 8px 12px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
