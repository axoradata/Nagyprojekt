import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Profile from '../views/Profile.vue'
import Users from '../views/Users.vue'
import Group from '../views/Group.vue'
import Logs from '../views/Logs.vue'
import RfidManagement from '../views/RfidManagement.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/users', name: 'Users', component: Users, meta: { requiresAuth: true } },
  { path: '/groups', name: 'Group', component: Group, meta: { requiresAuth: true } },
  { path: '/logs', name: 'Logs', component: Logs, meta: { requiresAuth: true } },
  { path: '/rfid', name: 'RfidManagement', component: RfidManagement, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (to.meta.requiresAuth && !user.role) next({ name: 'Login' })
  else next()
})

export default router
