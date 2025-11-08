<template>
  <div class="dashboard">
    <h1>Üdv, {{ user.name }}!</h1>
    <p>Szereped: {{ user.role }}</p>
    <button @click="logout">Kijelentkezés</button>
  </div>
</template>

<script>
export default {
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
.dashboard {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
}
button {
  padding: 8px 12px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
