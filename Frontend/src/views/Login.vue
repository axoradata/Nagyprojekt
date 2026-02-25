<template>
  <div class="login-page">
  <button @click="testConnection" class="test-btn">Backend Teszt</button>
    <div class="auth-box">
      <h1>Belépés</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="label-text">Email:</label>
          <input type="text" v-model="email" required class="custom-input" />
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
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      testMessage: ''
    }
  },
  methods: {
    async testConnection() {
      try {
        const response = await axios.get('http://localhost:8000/');
        this.testMessage = `Backend mondja: ${response.data.Hello}`;
        console.log("Megjött a válasz:", response.data);
      } catch (error) {
        console.error("Hiba:", error);
      }
    },
    async handleLogin() {
      console.log("Gomb megnyomva!");
      try {
        const response = await axios.post('http://localhost:8000/user/login', null, {
          params: {
            username: this.email,
            password: this.password
          }
        });

        console.log("Válasz a backendtől:", response.data);

        if (response.data.status === 1) {
          console.log("Sikeres status! Token:", response.data.token);
          
          localStorage.setItem('token', response.data.token);
          
          // A konzolod szerint a válasz így néz ki: 
          // {status: 1, token: '...', card_id: '...', role: '...', name: '...'}
          // Tehát nem response.data.user-t kell menteni, hanem ezeket a mezőket:
          localStorage.setItem('user', JSON.stringify({
            full_name: response.data.name || 'Ismeretlen',
            card_id: response.data.card_id || '0000-0000-0000-0000',
            role: response.data.role || 'worker',
            disposition: response.data.role // Biztonság kedvéért mindkét néven elmentjük
          }));

          console.log("User adatok elmentve, irány a dashboard...");
          
          // Options API-ban (ebben a stílusban) így hivatkozunk a routerre:
          this.$router.push('/dashboard');
          
        } else {
          console.error("A backend status 0-át küldött!");
          this.errorMessage = "Hibás felhasználónév vagy jelszó!";
        }
      } catch (error) {
        console.error("Axios hívás hiba:", error);
        this.errorMessage = "Hálózati hiba történt!";
      }
    }
  }
}
</script>

<style scoped>
/* TESZTHEZ */
.test-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 15px;
  background: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  z-index: 100;
}

.test-message {
  margin-top: 15px;
  font-size: 0.85rem;
  color: #27ae60;
  font-weight: bold;
}
/*--------------------------*/

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