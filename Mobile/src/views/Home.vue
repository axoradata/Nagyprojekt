<template>
  <ion-page>
    <ion-content fullscreen>
      <div class="home-wrapper">

        <!-- Logó -->
        <div class="logo-container">
          <img src="\axoradata_white.png" alt="App Logo" class="app-logo" />
        </div>

        <ion-card>
          <ion-card-content class="text-center">
            <h2>Üdv, {{ fullName }}!</h2>
            <p>ID: {{ card_id }}</p>
            <p>A te beosztásod: <strong>{{ role }}</strong></p>
          </ion-card-content>
        </ion-card>

        <ion-button expand="block" class="ion-margin-top" @click="logout">
          Kijelentkezés
        </ion-button>

      </div>
    </ion-content>
  </ion-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { IonPage, IonContent, IonButton } from '@ionic/vue'

export default {
  name: 'HomePage',
  components: { IonPage, IonContent, IonButton },
  setup() {
    const router = useRouter()
    const fullName = ref('')
    const card_id = ref('')
    const role = ref('')

    onMounted(() => {
      fullName.value = localStorage.getItem('fullName') || 'Felhasználó'
      role.value = localStorage.getItem('role') || 'Ismeretlen'
      card_id.value = localStorage.getItem('card_id') || 'N/A'
    })

    function logout() {
      localStorage.removeItem('user')
      localStorage.removeItem('fullName')
      localStorage.removeItem('role')
      router.push('/')
    }

    return { fullName, role, logout }
  }
}
</script>

<style scoped>
.home-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
  padding: 0 20px;
}

.logo-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.app-logo {
  height: 200px;
  width: auto;
}

h2 {
  font-size: 22px;
  margin-bottom: 5px;
}

p {
  font-size: 18px;
}

ion-card {
  width: 90%;
  max-width: 400px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

ion-button {
  --border-radius: 12px;
  --background: #387eff;
  --color: #fff;
}
</style>
