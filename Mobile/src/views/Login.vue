<template>
  <ion-page>
    <ion-content fullscreen>
      <div class="page-wrapper">

        <div class="logo-container">
          <img src="/axoradata_white.png" alt="App Logo" class="app-logo" />
        </div>

        <ion-card>
          <ion-card-content>
            <ion-item>
              <ion-input v-model="email" type="email" placeholder="Email"></ion-input>
            </ion-item>

            <ion-item>
              <ion-input v-model="password" type="password" placeholder="Jelszó"></ion-input>
            </ion-item>

            <ion-button expand="block" @click="login">
              Bejelentkezés
            </ion-button>

            <p class="ion-text-center ion-margin-top">
              Még nincs fiókod?
              <router-link to="/register" class="no-underline">Regisztráció</router-link>
            </p>
          </ion-card-content>
        </ion-card>

      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import supabase from '@/supabase'
import bcrypt from 'bcryptjs'
import { IonPage, IonContent, IonItem, IonInput, IonButton, IonCard, IonCardContent } from '@ionic/vue'

const email = ref('')
const password = ref('')
const router = useRouter()

async function login() {
  if (!email.value || !password.value) {
    alert('Kérlek, töltsd ki mindkét mezőt!')
    return
  }

  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('email', email.value)
    .single()

  if (data && bcrypt.compareSync(password.value, data.password_hash)) {
  localStorage.setItem('fullName', data.full_name)
  localStorage.setItem('role', data.role)
  localStorage.setItem('card_id', data.card_id)
  router.push('/home')
} else {
  alert('Hibás email vagy jelszó.')
}

  // Sikeres belépés
  localStorage.setItem('fullName', data.full_name)
  localStorage.setItem('role', data.role)
  localStorage.setItem('card_id', data.card_id)
  router.push('/home')
}
</script>


<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 60px;
}

/* Logo */
.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.app-logo {
  height: 150px;
  width: auto;
}

/* Card */
ion-card {
  width: 90%;
  max-width: 400px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin: 0 auto;
}

/* Input és Select világos/sötét módhoz */
ion-item, ion-input, ion-select {
  --background: transparent;
  --color: var(--ion-text-color);
  --placeholder-color: var(--ion-color-step-500);
}

/* Button */
ion-button {
  --border-radius: 12px;
  --background: var(--ion-color-primary);
  --color: var(--ion-color-light);
  font-weight: bold;
  padding: 12px 0;
}

/* Link */
.no-underline {
  color: var(--ion-color-primary);
  text-decoration: none;
  font-weight: bold;
}
</style>
