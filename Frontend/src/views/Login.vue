<template>
  <div class="login-page">
    <div class="auth-box">
      <h1>Belépés</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="light-text">Email:</label>
          <input type="email" v-model="email" required class="dark-input" />
        </div>
        <div class="form-group">
          <label class="light-text">Jelszó:</label>
          <input type="password" v-model="password" required class="dark-input" />
        </div>
        <button type="submit" class="btn-main custom-btn-primary">Bejelentkezés</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
// A script rész változatlan marad
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
/* A globális stílusokat (html, body) átmásolhatod a main CSS fájlba,
   vagy meghagyhatod itt, de a többi stílus a Login.vue-ban lesz. */

/* Alapértelmezett margók eltávolítása globálisan */
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
  /* Fő háttér: Legsötétebb szín */
  background-color: #222831; 
}

.auth-box {
  /* Auth doboz háttér: Világosabb sötét szín */
  background-color: #393E46; 
  padding: 3rem 3.5rem;
  border-radius: 20px;
  /* Sötét árnyék a sötét háttéren */
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6); 
  width: 400px;
  max-width: 90%;
  text-align: center;
}

h1 {
  margin-bottom: 1.8rem;
  /* Szövegszín: Világos bézs */
  color: #DFD0B8 !important; 
  font-size: 2rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}

/* Label: Világos bézs a sötét háttéren */
label.light-text {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
  color: #DFD0B8; 
}

/* Input mezők sötét témához igazítva */
input.dark-input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  background-color: #222831; /* Legsötétebb háttér */
  color: #DFD0B8; /* Világos szöveg */
  border: 1px solid #393E46; 
  border-radius: 8px;
  outline: none;
  transition: 0.2s;
}

/* Fókusz színe a kiemelő színre állítva */
input.dark-input:focus {
  border-color: #948979; /* Kiemelő szín */
  box-shadow: 0 0 6px rgba(148, 137, 121, 0.6); /* Bézs árnyék */
}

/* A korábban használt custom-btn-primary stílusok alkalmazása */
.custom-btn-primary {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  background-color: #948979; /* Kiemelő szín */
  color: white; 
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: 0.3s;
  font-size: 1rem;
}

.custom-btn-primary:hover {
  background-color: #7d7264; /* Sötétebb kiemelő hover szín */
}

.error {
  color: #d63031; /* Hibaüzenet marad piros */
  margin-top: 1rem;
  font-weight: 500;
}
</style>