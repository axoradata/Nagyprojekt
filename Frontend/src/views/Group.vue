<template>
  <div class="page-container-dark">
    <div class="page-content-box" style="width: 500px;">
      
      <h2 class="section-title">Csoportok Kezelése</h2>
      
      <button 
        class="btn custom-btn-primary mb-4 w-100" 
        data-bs-toggle="modal" 
        data-bs-target="#addGroupModal"
      >
        <i class="bi bi-plus-circle-fill me-2"></i> Új Csoport Hozzáadása
      </button>

      <div v-for="g in reactiveGroups" :key="g.id" class="group-card-dark">
        <div class="d-flex justify-content-between align-items-start">
          <h3>{{ g.name }}</h3>
          
          <button 
            class="btn btn-sm delete-btn" 
            @click="deleteGroup(g.id)"
            title="Csoport törlése"
          >
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
        
        <p class="leader-info">Leader: <strong>{{ getLeaderName(g.leader_id) }}</strong></p>
        <p class="mt-3 mb-1">Tagok:</p>
        <ul class="list-unstyled member-list">
          <li v-for="memberId in g.members" :key="memberId">
            <i class="bi bi-person-fill me-1"></i> {{ getUserName(memberId) }}
          </li>
          <li v-if="g.members.length === 0">Nincs tag</li>
        </ul>
      </div>

      <div v-if="reactiveGroups.length === 0" class="text-center mt-4 p-3 no-groups-message">
          Nincsenek létrehozott csoportok.
      </div>

    </div>
  </div>

  <div class="modal fade" id="addGroupModal" tabindex="-1" aria-labelledby="addGroupModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-dark">
        <div class="modal-header modal-dark-header">
          <h5 class="modal-title" id="addGroupModalLabel">Új csoport létrehozása</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="addNewGroup">
          <div class="modal-body">
            
            <div class="mb-3">
              <label for="groupName" class="form-label light-text">Csoport neve</label>
              <input type="text" class="form-control dark-input" id="groupName" v-model="newGroupName" required>
            </div>
            
            <div class="mb-3">
              <label for="groupLeader" class="form-label light-text">Csoportvezető (Leader)</label>
              <select class="form-select dark-input" id="groupLeader" v-model="newGroupLeaderId" required>
                <option disabled value="">Válasszon vezetőt</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }} ({{ u.role }})</option>
              </select>
            </div>
            
          </div>
          <div class="modal-footer modal-dark-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Mégsem</button>
            <button type="submit" class="btn custom-btn-primary">Létrehozás</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { groups, users } from '../data' // Feltételezve, hogy a 'groups' és 'users' innen importálható

// --- Reaktivitás és Funkciók ---
// Deep copy és ref használata a groups tömbön a CRUD műveletek szimulálásához
const reactiveGroups = ref(JSON.parse(JSON.stringify(groups)))
const newGroupName = ref('')
const newGroupLeaderId = ref('')

const getUserName = (id) => {
  const user = users.find(u => u.id === id)
  return user ? user.username : 'Ismeretlen'
}

const getLeaderName = (leader_id) => {
  return getUserName(leader_id)
}

const deleteGroup = (id) => {
  if (confirm('Biztosan törölni szeretnéd ezt a csoportot?')) {
    reactiveGroups.value = reactiveGroups.value.filter(g => g.id !== id)
  }
}

const addNewGroup = () => {
  if (newGroupName.value && newGroupLeaderId.value) {
    const newId = Math.max(...reactiveGroups.value.map(g => g.id), 0) + 1
    
    const newGroup = {
      id: newId,
      name: newGroupName.value,
      leader_id: newGroupLeaderId.value,
      members: [],
    }

    reactiveGroups.value.push(newGroup)

    // Reset űrlap és modal bezárása (feltételezve, hogy a Bootstrap elérhető)
    newGroupName.value = ''
    newGroupLeaderId.value = ''
    
    // Manuális bezárás (a Bootstrap JS-t feltételezi)
    const modalElement = document.getElementById('addGroupModal')
    if (modalElement) {
        // Ellenőrzés, hogy a Bootstrap JS importálva van-e
        const bootstrapModal = bootstrap.Modal.getInstance(modalElement)
        if (bootstrapModal) {
            bootstrapModal.hide()
        } else {
            console.warn("Bootstrap JS Modal objektum nem található. A Modalt manuálisan kell bezárni.")
        }
    }
  }
}
</script>

<style scoped>
/* --- FŐ ELRENDEZÉS STÍLUSOK (Logs.vue alapján) --- */
.page-container-dark {
  background-color: #222831; 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100%; 
  width: 100%; 
}

.page-content-box {
  background-color: #393E46; 
  color: #DFD0B8; 
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.section-title {
    color: #DFD0B8;
    border-bottom: 2px solid #948979;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

/* --- CSOPORTKÁRTYA STÍLUSOK --- */
.group-card-dark {
  background-color: #222831; /* Legsötétebb háttér, kontraszt a listaboxhoz */
  color: #DFD0B8; 
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  border: 1px solid #948979; /* Vékony kiemelő keret */
}

.group-card-dark h3 {
  color: #DFD0B8;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.leader-info strong {
    color: #948979; /* Leader nevének kiemelése */
}

.member-list li {
    padding-left: 0.5rem;
    line-height: 1.5;
}

/* Törlés Gomb Stílusok */
.delete-btn {
    background: none;
    border: none;
    color: #D63031; /* Piros a veszély jelzésére */
    padding: 0;
    font-size: 1.2rem;
    transition: color 0.2s;
}
.delete-btn:hover {
    color: #FF6B6B;
}

.no-groups-message {
    background-color: #333940;
    color: #DFD0B8;
    border-radius: 8px;
    border: 1px dashed #948979;
}

/* --- MODÁLIS ABLAK STÍLUSOK (A meglévő stílusok kiterjesztése) --- */
.modal-dark {
    background-color: #393E46;
    color: #DFD0B8;
}

.modal-dark-header {
    border-bottom: 1px solid #222831;
}

.modal-dark-footer {
    border-top: 1px solid #222831;
}

.btn-close-white {
    filter: invert(1); /* Fehérré teszi a zárt gombot sötét háttéren */
}

/* Input és Gomb stílusok a korábbi komponensekből */
.custom-btn-primary {
    background-color: #948979;
    border-color: #948979;
    color: white;
    font-weight: 600;
}
.custom-btn-primary:hover {
    background-color: #7d7264;
    border-color: #7d7264;
    color: white;
}

.dark-input {
    background-color: #222831;
    border-color: #555;
    color: #DFD0B8;
}
.dark-input:focus {
    border-color: #948979;
    box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.25);
}

.light-text {
    color: #DFD0B8 !important;
}
</style>