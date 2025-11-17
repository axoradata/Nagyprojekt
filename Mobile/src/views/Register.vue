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
              <ion-input v-model="card_id" type="text" placeholder="Kártya ID"></ion-input>
            </ion-item>

            <ion-item>
              <ion-input v-model="fullName" type="text" placeholder="Teljes név"></ion-input>
            </ion-item>

            <ion-item>
              <ion-input v-model="email" type="email" placeholder="Email"></ion-input>
            </ion-item>

            <ion-item>
              <ion-input v-model="password" type="password" placeholder="Jelszó"></ion-input>
            </ion-item>

            <ion-item>
              <ion-input v-model="authority" type="text" placeholder="AUTORITI"></ion-input>
            </ion-item>

            <ion-item>
              <ion-select v-if="mounted" v-model="role" placeholder="Válassz beosztást">
                <ion-select-option value="developer">Fejlesztő</ion-select-option>
                <ion-select-option value="designer">Designer</ion-select-option>
                <ion-select-option value="manager">Manager</ion-select-option>
                <ion-select-option value="other">Egyéb</ion-select-option>
              </ion-select>
            </ion-item>

            <ion-button expand="block" @click="register">
              Regisztráció
            </ion-button>

            <p class="ion-text-center ion-margin-top">
              Van már fiókod?
              <router-link to="/" class="no-underline">Bejelentkezés</router-link>
            </p>

          </ion-card-content>
        </ion-card>

      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import supabase from '@/supabase'
import bcrypt from 'bcryptjs'
import {
  IonPage, IonContent, IonItem, IonInput, IonSelect, IonSelectOption, IonButton, IonCard, IonCardContent
} from '@ionic/vue'

const card_id = ref('')
const fullName = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const authority = ref('')
const mounted = ref(false)
const router = useRouter()

onMounted(() => { mounted.value = true })

async function register() {
  if (!card_id.value || !fullName.value || !email.value || !password.value || !role.value || !authority.value) {
    alert('Tölts ki minden mezőt!')
    return
  }

  // Hash-eljük a jelszót
  const hashedPassword = bcrypt.hashSync(password.value, 10)

  const { error } = await supabase
    .from('users')
    .insert([{ 
      card_id: card_id.value,
      full_name: fullName.value, 
      email: email.value, 
      password_hash: hashedPassword, 
      role: role.value,
      authority: authority.value
    }])

  if (error) {
    alert(error.message)
  } else {
    alert('Sikeres regisztráció!')
    router.push('/')
  }
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

/* Select felugró lista világos/sötét módhoz */
body .sc-ion-select-md-h {
  --background: var(--ion-background-color);
  --color: var(--ion-text-color);
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
