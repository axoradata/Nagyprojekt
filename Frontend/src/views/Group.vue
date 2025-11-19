<template>
  <div class="page-container-dark">
    <div class="page-content-box">
      
      <h2 class="section-title">Csoportok Kezelése</h2>
      
      <button 
        class="btn custom-btn-primary mb-4 w-100" 
        data-bs-toggle="modal" 
        data-bs-target="#addGroupModal"
      >
        <i class="bi bi-plus-circle-fill me-2"></i> Új Csoport Hozzáadása
      </button>

      <div class="group-grid">
        <div v-for="g in reactiveGroups" :key="g.id" class="group-card-grid">
          
          <div class="card-header-flex">
            <h4 class="group-name">{{ g.name }}</h4>
            
            <button 
              class="btn btn-sm delete-btn" 
              @click="deleteGroup(g.id)"
              title="Csoport törlése"
            >
              <i class="bi bi-trash-fill"></i>
            </button>
          </div>
          
          <div class="card-body-content">
            <div class="info-row leader-info">
              <i class="bi bi-person-badge-fill me-2"></i> Vezető: 
              <strong class="leader-name">{{ getLeaderName(g.leader_id) }}</strong>
            </div>
            
            <div class="info-row member-count-info">
              <i class="bi bi-people-fill me-2"></i> Tagok száma: 
              <span class="member-count">{{ g.members.length }}</span>
            </div>

            <hr class="card-divider">

            <div class="members-detail">
              <p class="mb-1 fw-bold">Tagok listája:</p>
              <ul class="list-unstyled member-list">
                <li v-for="memberId in g.members" :key="memberId">
                  <i class="bi bi-person-fill me-1"></i> {{ getUserName(memberId) }}
                </li>
                <li v-if="g.members.length === 0">Nincs tag</li>
              </ul>
            </div>

          </div>
        </div>
      </div>

      <div v-if="reactiveGroups.length === 0" class="text-center mt-5 p-4 no-groups-message">
          <i class="bi bi-info-circle-fill me-2"></i> Nincsenek létrehozott csoportok.
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
import { ref } from 'vue'
// Feltételezzük, hogy a users és groups adatok innen jönnek
import { groups, users } from '../data' 

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
    // Győződjünk meg arról, hogy a users-ből származó ID-k számok
    const maxId = reactiveGroups.value.length > 0 
                  ? Math.max(...reactiveGroups.value.map(g => g.id))
                  : 0
    const newId = maxId + 1
    
    const newGroup = {
      id: newId,
      name: newGroupName.value,
      leader_id: parseInt(newGroupLeaderId.value), // Ensure it's a number if IDs are numeric
      members: [],
    }

    reactiveGroups.value.push(newGroup)

    newGroupName.value = ''
    newGroupLeaderId.value = ''
    
    // Bootstrap Modal manuális bezárása
    const modalElement = document.getElementById('addGroupModal')
    if (modalElement && window.bootstrap) {
        const bootstrapModal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement)
        bootstrapModal.hide()
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
  min-height: 100vh; 
  width: 100%; 
}

.page-content-box {
  background-color: #393E46; 
  color: #DFD0B8; 
  padding: 2rem;
  border-radius: 16px;
  
  /* EGYSÉGES SZÉLESSÉG */
  width: 900px; 
  max-width: 95%; 
  
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.section-title {
    color: #DFD0B8;
    border-bottom: 2px solid #948979;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
}

/* --- RÁCS ELRENDEZÉS a kártyákhoz (Mint a Users.vue-ban) --- */
.group-grid {
    display: grid;
    /* Automatikus tördelés: minimum 280px széles oszlopok */
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem; 
}

/* --- CSOPORTKÁRTYA STÍLUSOK --- */
.group-card-grid {
  background-color: #222831; 
  color: #DFD0B8; 
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #484f59; /* Enyhe szegély */
  transition: transform 0.2s, box-shadow 0.2s;
}

.group-card-grid:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
}

.card-header-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #393E46;
    padding-bottom: 0.5rem;
}

.group-name {
  color: #DFD0B8;
  font-size: 1.3rem;
  margin: 0;
}

.card-body-content {
    padding-top: 0.5rem;
}

.info-row {
    display: flex;
    align-items: center;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.leader-info strong {
    color: #948979; /* Kiemelő szín */
    font-weight: 600;
}

.member-count {
    font-weight: 600;
    color: #DFD0B8;
}

.card-divider {
    border-top: 1px solid #393E46;
    margin: 1rem 0;
    opacity: 1;
}

/* Tagok listája a kártyán belül */
.member-list {
    margin-top: 0.5rem;
    padding-left: 1rem;
    font-size: 0.9rem;
    max-height: 90px;
    overflow-y: auto;
}

.member-list li {
    line-height: 1.4;
    color: #b5ac9d;
}

/* Törlés Gomb Stílusok */
.delete-btn {
    background: none;
    border: none;
    color: #D63031; 
    padding: 0;
    font-size: 1.2rem;
    transition: color 0.2s;
}
.delete-btn:hover {
    color: #FF6B6B;
}

/* --- MODAL ÉS FORM STÍLUSOK (Megtartva) --- */
.custom-btn-primary {
  background-color: #948979;
  border-color: #948979;
  color: white;
  font-weight: 600;
}
.custom-btn-primary:hover {
  background-color: #7d7264;
  border-color: #7d7264;
}

.modal-content.modal-dark {
    background-color: #393E46;
    color: #DFD0B8;
}

.modal-header.modal-dark-header {
    border-bottom: 1px solid #484f59;
}

.modal-footer.modal-dark-footer {
    border-top: 1px solid #484f59;
}

.form-control.dark-input, 
.form-select.dark-input {
    background-color: #222831;
    border-color: #484f59;
    color: #DFD0B8;
}
.form-control.dark-input:focus,
.form-select.dark-input:focus {
    border-color: #948979;
    box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.25); 
}

.btn-close-white {
    filter: invert(1);
}

.no-groups-message {
    background-color: #222831;
    border-radius: 8px;
    border: 1px solid #484f59;
    color: #948979;
    font-size: 1.1rem;
}
</style>