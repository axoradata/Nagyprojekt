<template>
  <div class="login-page">
    <div class="auth-box">
      <h1>Belépés</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="label-text">Email:</label>
          <input type="email" v-model="email" required class="custom-input" />
        </div>
        <div class="form-group">
          <label class="label-text">Jelszó:</label>
          <input type="password" v-model="password" required class="custom-input" />
        </div>
        <button type="submit" class="btn-main custom-btn-primary">Bejelentkezés</button>
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

<style scoped>
/* A scoped stílus fontos, hogy ne zavarjon be más oldalaknak */

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  /* Változó a fő háttérnek */
  background-color: var(--bg-main); 
  transition: background-color 0.3s ease;
}

.auth-box {
  background-color: var(--bg-card); 
  padding: 3rem 3.5rem;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  /* Dinamikusabb árnyék */
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); 
  width: 400px;
  max-width: 90%;
  text-align: center;
  transition: all 0.3s ease;
}

h1 {
  margin-bottom: 1.8rem;
  color: var(--text-main) !important; 
  font-size: 2rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}

.label-text {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
  color: var(--accent); 
  font-weight: 500;
}

input.custom-input {
  width: 100%;
  padding: 0.7rem 0.9rem;
  background-color: var(--bg-inner);
  color: var(--text-main);
  border: 1px solid var(--border-color); 
  border-radius: 8px;
  outline: none;
  transition: all 0.2s;
}

input.custom-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(148, 137, 121, 0.2);
}

.custom-btn-primary {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  background-color: var(--accent);
  color: white; 
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: 0.3s;
  font-size: 1rem;
}

.custom-btn-primary:hover {
  filter: brightness(1.1);
}

.error {
  color: #d63031; 
  margin-top: 1rem;
  font-weight: 500;
}
</style>