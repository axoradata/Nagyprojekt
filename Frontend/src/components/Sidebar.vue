<template>
  <nav
    id="sidebarMenu"
    class="d-lg-block sidebar collapse"
  >
    <div class="position-sticky pt-3 sidebar-sticky">
      <div class="canvas-header">
        <h5 class="canvas-title text-center" id="sidebarMenuLabel">
          <img src="../assets/logo.png" style="height:150px;" alt="Logo" />
        </h5>
      </div>

      <div class="fotartalom d-flex flex-column h-100">
        <h5 class="px-3 mb-4 mt-4 user-info">
          Belépve: <span class="fw-bold">{{ user.full_name }}</span>
        </h5>

        <ul class="nav flex-column">

          <li class="nav-item">
            <router-link 
              to="/dashboard"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/dashboard') }"
            >
              <i class="bi bi-speedometer2 me-2"></i>
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link 
              to="/profile"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/profile') }"
            >
              <i class="bi bi-person-circle me-2"></i>
              Profil
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/users"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/users') }"
            >
              <i class="bi bi-people-fill me-2"></i>
              Felhasználók
            </router-link>
          </li>

          <li v-if="user.role === 'admin' || user.role === 'team_leader'" class="nav-item">
            <router-link
              to="/groups"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/groups') }"
            >
              <i class="bi bi-diagram-3-fill me-2"></i>
              Csoportok
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/logs"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/logs') }"
            >
              <i class="bi bi-journal-text me-2"></i>
              Eseménynapló
            </router-link>
          </li>

          <li v-if="user.role === 'admin'" class="nav-item">
            <router-link
              to="/rfid"
              class="nav-link custom-nav-link"
              :class="{ active: isActive('/rfid') }"
            >
              <i class="bi bi-credit-card-2-front-fill me-2"></i>
              RFID kezelés
            </router-link>
          </li>

          <li class="nav-item mt-4 mx-auto w-100 px-3">
            <button 
              class="btn btn-logout w-100"
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

  <button
    class="btn btn-mobile-toggle d-lg-none position-fixed top-0 start-0 m-3"
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
import axios from "axios"

const router = useRouter()
const route = useRoute()

const user = ref(JSON.parse(localStorage.getItem("user") || "{}"))

const logout = async () => {
  const token = localStorage.getItem('token');
  
  try {
    if (token) {
      // A második paraméter a Body (null), a harmadik a config, amiben a params van
      await axios.post('http://localhost:8000/user/logout', null, { 
        params: { token: token } 
      });
    }
  } catch (err) {
    console.error("Logout hiba:", err);
  } finally {
    // Akár sikerült a backendnek, akár nem, mi kiléptetjük a felhasználót
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  }
};

const isActive = (path) => {
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  /* A változókat használjuk */
  background-color: var(--bg-card) !important;
  border-right: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.user-info {
  color: var(--text-main);
  font-size: 1.1rem;
}

.fotartalom {
  height: calc(100vh - 200px);
  overflow-y: auto;
}

/* Navigációs linkek alapstílusa */
.custom-nav-link {
  color: var(--text-main) !important;
  padding: 0.8rem 1.5rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.custom-nav-link:hover {
  background-color: rgba(148, 137, 121, 0.1);
  color: var(--accent) !important;
}

/* Aktív link stílusa */
.custom-nav-link.active {
  font-weight: bold;
  background-color: rgba(148, 137, 121, 0.15);
  border-left: 4px solid var(--accent);
  color: var(--accent) !important;
}

/* Kijelentkezés gomb */
.btn-logout {
  border: 1px solid var(--accent);
  color: var(--accent);
  background: transparent;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background-color: var(--accent);
  color: #fff !important; /* Ez maradhat fehér hoverkor */
}

/* Mobil kapcsoló gomb */
.btn-mobile-toggle {
  background-color: var(--bg-card);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  z-index: 1100;
}

/* Eltávolítottam a "*" color kényszerítést, mert az elrontja az ikonokat 
   és egyéb finomabb színeket. Helyette a konténer szintjén állítjuk be. */
</style>