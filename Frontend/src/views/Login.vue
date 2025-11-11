<template>
  <div class="login-page">
    <div class="auth-box">
      <h1>Belépés</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label>Jelszó:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit" class="btn-main">Bejelentkezés</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
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

<style>
/* 🧩 Alapértelmezett margók eltávolítása globálisan */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: #2c3e50;
}

.auth-box {
  background: #fff;
  padding: 3rem 3.5rem;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  width: 400px;
  max-width: 90%;
  text-align: center;
}

h1 {
  margin-bottom: 1.8rem;
  color: #2d3436;
  font-size: 2rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}

label {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
  color: #636e72;
}

input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid #b2bec3;
  border-radius: 8px;
  outline: none;
  transition: 0.2s;
}

input:focus {
  border-color: #2c3e50;
  box-shadow: 0 0 6px rgba(9,132,227,0.3);
}

.btn-main {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  background-color: #2c3e50;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: 0.3s;
  font-size: 1rem;
}

.btn-main:hover {
  background-color: #74b9ff;
}

.error {
  color: #d63031;
  margin-top: 1rem;
  font-weight: 500;
}
</style>
