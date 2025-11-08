<template>
  <aside class="sidebar">
    <h2>MyApp</h2>
    <ul>
      <li><router-link to="/dashboard">Dashboard</router-link></li>
      <li v-if="user && user.role === 'admin'"><router-link to="/admin">Admin Panel</router-link></li>
      <li v-if="user && user.role === 'leader'"><router-link to="/leader">Csoportvezetői Panel</router-link></li>
      <li v-if="user"><button @click="logout">Kijelentkezés</button></li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      user: null
    }
  },
  created() {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      this.user = JSON.parse(storedUser)
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
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  background-color: #2c3e50;
  padding: 20px;
  color: white;
}

.sidebar h2 {
  margin-bottom: 30px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 15px;
}

.sidebar a {
  color: white;
  text-decoration: none;
}

.sidebar a:hover {
  text-decoration: underline;
}

.sidebar button {
  background: none;
  border: 1px solid white;
  color: white;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
