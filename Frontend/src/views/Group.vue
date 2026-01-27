<template>
  <div class="page-container">
    <div class="page-content-box">
      
      <h2 class="section-title">Csoportok</h2>
      
      <button 
        class="btn custom-btn-primary mb-4 w-100" 
        data-bs-toggle="modal" 
        data-bs-target="#addGroupModal"
      >
        <i class="bi bi-plus-circle-fill me-2"></i> Új csoport hozzáadása
      </button>

      <div class="group-grid">
        <div v-for="g in reactiveGroups" :key="g.id" class="group-card">
          
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
                <li v-if="g.members.length === 0" class="no-member">Nincs tag</li>
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
      <div class="modal-content custom-modal">
        <div class="modal-header">
          <h5 class="modal-title" id="addGroupModalLabel">Új csoport létrehozása</h5>
          <button type="button" class="btn-close" :class="{'btn-close-white': isDarkMode}" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="addNewGroup">
          <div class="modal-body">
            
            <div class="mb-3">
              <label for="groupName" class="form-label">Csoport neve</label>
              <input type="text" class="form-control custom-input" id="groupName" v-model="newGroupName" required>
            </div>
            
            <div class="mb-3">
              <label for="groupLeader" class="form-label">Csoportvezető (Leader)</label>
              <select class="form-select custom-input" id="groupLeader" v-model="newGroupLeaderId" required>
                <option disabled value="">Válasszon vezetőt</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }} ({{ u.role }})</option>
              </select>
            </div>
            
          </div>
          <div class="modal-footer">
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
import { groups, users } from '../data' 

const reactiveGroups = ref(JSON.parse(JSON.stringify(groups)))
const newGroupName = ref('')
const newGroupLeaderId = ref('')

// Figyeljük az aktuális témát a bezáró gomb (X) színe miatt
const isDarkMode = computed(() => {
    return document.documentElement.getAttribute('data-theme') !== 'light';
});

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
    const maxId = reactiveGroups.value.length > 0 
                  ? Math.max(...reactiveGroups.value.map(g => g.id))
                  : 0
    const newId = maxId + 1
    
    const newGroup = {
      id: newId,
      name: newGroupName.value,
      leader_id: parseInt(newGroupLeaderId.value),
      members: [],
    }

    reactiveGroups.value.push(newGroup)
    newGroupName.value = ''
    newGroupLeaderId.value = ''
    
    const modalElement = document.getElementById('addGroupModal')
    if (modalElement && window.bootstrap) {
        const bootstrapModal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement)
        bootstrapModal.hide()
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 2rem; 
  min-height: 100vh; 
  width: 100%; 
}

.page-content-box {
  background-color: var(--bg-card); 
  color: var(--text-main); 
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 1000px; 
  margin: 0 auto;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.section-title {
    color: var(--text-main);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
}

.group-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem; 
}

.group-card {
  background-color: var(--bg-inner); 
  color: var(--text-main); 
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
}

.group-card:hover {
    transform: translateY(-3px);
    border-color: var(--accent);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.card-header-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.5rem;
}

.group-name {
  color: var(--text-main);
  font-size: 1.3rem;
  margin: 0;
  font-weight: 600;
}

.leader-name {
    color: var(--accent);
}

.card-divider {
    border-top: 1px solid var(--border-color);
    margin: 1rem 0;
    opacity: 0.5;
}

.member-list {
    margin-top: 0.5rem;
    padding-left: 0.5rem;
    font-size: 0.9rem;
}

.member-list li {
    color: var(--text-main);
    opacity: 0.8;
    margin-bottom: 0.2rem;
}

.no-member {
    font-style: italic;
    opacity: 0.5;
}

.delete-btn {
    color: #e74c3c; 
    transition: transform 0.2s;
}

.delete-btn:hover {
    color: #c0392b;
    transform: scale(1.2);
}

/* --- MODAL STÍLUSOK --- */
.custom-modal {
    background-color: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border-color);
}

.modal-header, .modal-footer {
    border-color: var(--border-color);
}

.custom-input {
    background-color: var(--bg-inner);
    border-color: var(--border-color);
    color: var(--text-main);
}

.custom-input:focus {
    background-color: var(--bg-inner);
    color: var(--text-main);
    border-color: var(--accent);
    box-shadow: 0 0 0 0.25rem rgba(148, 137, 121, 0.25);
}

.custom-btn-primary {
  background-color: var(--accent);
  border-color: var(--accent);
  color: white;
}

.custom-btn-primary:hover {
  filter: brightness(1.1);
}

.no-groups-message {
    background-color: var(--bg-inner);
    border-radius: 8px;
    border: 1px dashed var(--accent);
    color: var(--accent);
}

/* Bootstrap "X" gomb invertálása sötét módban */
.btn-close-white {
    filter: invert(1) grayscale(100%) brightness(200%);
}
</style>