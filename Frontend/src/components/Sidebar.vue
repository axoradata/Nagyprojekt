<template>
  <!-- Sidebar (desktop fix + mobile offcanvas) -->
  <nav
    id="sidebarMenu"
    class="d-lg-block bg-dark text-white sidebar collapse"
  >
    <div class="position-sticky pt-3 sidebar-sticky">
      <div class="canvas-header">
        <h5 class="canvas-title text-center" id="sidebarMenuLabel"><img src="../assets/Axora.png" style="height:150px;"></img></h5>
      </div>

      <div class="fotartalom d-flex flex-column h-100">
        <h5 class="px-3 mb-4 mt-4">
          Belépve: <span class="fw-bold">{{ user.username }}</span>
        </h5>

        <ul class="nav flex-column">

          <li class="nav-item">
            <router-link 
              to="/dashboard"
              class="nav-link text-white"
              :class="{ active: isActive('/dashboard') }"
            >
              <i class="bi bi-speedometer2 me-2"></i>
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link 
              to="/profile"
              class="nav-link text-white"
              :class="{ active: isActive('/profile') }"
            >
              <i class="bi bi-person-circle me-2"></i>
              Profil
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/users"
              class="nav-link text-white"
              :class="{ active: isActive('/users') }"
            >
              <i class="bi bi-people-fill me-2"></i>
              Felhasználók
            </router-link>
          </li>

          <li v-if="user.role === 'admin' || user.role === 'leader'" class="nav-item">
            <router-link
              to="/groups"
              class="nav-link text-white"
              :class="{ active: isActive('/groups') }"
            >
              <i class="bi bi-diagram-3-fill me-2"></i>
              Csoportok
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/logs"
              class="nav-link text-white"
              :class="{ active: isActive('/logs') }"
            >
              <i class="bi bi-journal-text me-2"></i>
              Események
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/rfid"
              class="nav-link text-white"
              :class="{ active: isActive('/rfid') }"
            >
              <i class="bi bi-credit-card-2-front-fill me-2"></i>
              RFID kezelés
            </router-link>
          </li>

          <li class="nav-item mt-4  mx-auto">
            <button 
              class="btn btn-outline-light px-5"
              @click="logout"
            >
              <i class="bi bi-box-arrow-right me-1"></i>
              Kijelentkezés
            </button>
          </li>

        </ul>
      </div>
    </div>
  </nav>

  <!-- MOBILE: Hamburger button -->
  <button
    class="btn btn-dark d-lg-none position-fixed top-0 start-0 m-3"
    type="button"
    data-bs-toggle="collapse"
    data-bs-target="#sidebarMenu"
  >
    <i class="bi bi-list"></i>
  </button>
</template>

<script setup>
import { ref } from "vue"
import { useRouter, useRoute } from "vue-router"

const router = useRouter()
const route = useRoute()

const user = ref(JSON.parse(localStorage.getItem("user") || "{}"))

const logout = () => {
  localStorage.removeItem("user")
  router.push("/login")
}

const isActive = (path) => {
  return route.path.startsWith(path)
}
</script>

<style scoped>

* {
  color: #DFD0B8 !important;
}

.sidebar {
  width: 240px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}

#sidebarMenu {
  background-color: #393E46 !important;
}

.fotartalom {
  height: calc(100vh - 200px);
  overflow-y: auto;
}

.nav-link.active {
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.15);
  border-left: 4px solid #948979;
}
</style>
