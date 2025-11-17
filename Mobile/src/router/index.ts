import { createRouter, createWebHistory } from '@ionic/vue-router'
import LoginPage from '../views/Login.vue'
import RegisterPage from '../views/Register.vue'
import HomePage from '../views/Home.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/home', name: 'Home', component: HomePage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
