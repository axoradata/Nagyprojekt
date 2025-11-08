<template>
  <div class="login-page">
    <h1>Belépés</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Jelszó:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Bejelentkezés</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import { users } from '../data'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    handleLogin() {
      const user = users.find(u => u.email === this.email && u.password === this.password)
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/dashboard')
      } else {
        this.errorMessage = 'Hibás email vagy jelszó'
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  max-width: 400px;
  margin: 80px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.login-page div {
  margin-bottom: 15px;
}
button {
  padding: 8px 12px;
  cursor: pointer;
}
.error {
  color: red;
}
</style>
