<template>
  <div class="page-container">
    <div class="page-content-box">
      <h2 class="section-title">Csoportok</h2>
      
      <div v-if="currentUser.disposition !== 'worker'" class="mb-4 text-center">
        <button class="btn custom-btn-primary action-btn-width" @click="showGroupModal = true">
          <i class="bi bi-plus-circle-fill me-2"></i> Új csoport
        </button>
      </div>

      <div class="profile-section">
        <h3 class="section-subtitle">Aktív munkacsoportok</h3>
        <hr class="section-divider">

        <div v-if="displayGroups.length === 0" class="text-center py-5">
          <p class="empty-text">Nincsenek aktív csoportok.</p>
        </div>

        <div v-for="g in displayGroups" :key="g.name" class="group-container mb-4">
          <div class="data-row header-row align-items-center">
            <div class="data-label fw-bold">{{ g.name }}</div>
            <div class="data-value">
              <button @click="handleDeleteGroup(g.name)" class="btn btn-sm text-danger border-0 p-0 shadow-none">
                <i class="bi bi-trash3-fill fs-5"></i>
              </button>
            </div>
          </div>

          <div class="data-row">
            <div class="data-label text-secondary">Csoportvezető:</div>
            <div class="data-value"><span class="role-badge">{{ g.leader || 'Nincs' }}</span></div>
          </div>

          <div class="tag-section">
            <div class="d-flex justify-content-between align-items-center mb-2 mt-2">
              <span class="small text-secondary fw-bold">Tagok:</span>
              <button class="btn btn-sm add-member-btn" @click="openAddMember(g.name)">
                <i class="bi bi-plus-lg"></i>
              </button>
            </div>
            
            <div class="d-flex flex-wrap gap-2">
              <div v-for="m in g.members" :key="m.card_id" class="member-chip">
                <span>{{ m.full_name }}</span>
                <button @click="removeMemberFromGroup(m.card_id)" class="btn-remove-member">
                  <i class="bi bi-x-circle-fill"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showGroupModal || showMemberModal" class="custom-backdrop" @click.self="closeModals">
      
      <div v-if="showGroupModal" class="custom-modal shadow-lg">
        <h4 class="mb-4 text-center">Új csoport létrehozása</h4>
        <div class="mb-3">
          <label class="small mb-1 text-secondary">Csoport neve:</label>
          <input type="text" v-model="newGroupName" class="form-control custom-input">
        </div>

        <div v-if="currentUser.disposition === 'admin'" class="mb-3">
          <label class="small mb-1 text-secondary">Vezető kinevezése:</label>
          <div class="dropdown w-100">
            <button class="btn dropdown-toggle w-100 custom-select-btn" type="button" data-bs-toggle="dropdown">
              {{ getSelectedLeaderName }}
            </button>
            <ul class="dropdown-menu w-100 custom-dropdown-menu shadow">
              <li v-for="l in freeLeaders" :key="l.card_id">
                <button class="dropdown-item" type="button" @click="selectedLeaderId = l.card_id">
                  {{ l.full_name }}
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div class="d-flex gap-2 mt-4">
          <button class="btn btn-dark-outline w-100" @click="closeModals">Mégse</button>
          <button class="btn custom-btn-primary w-100" @click="handleCreateGroup" :disabled="!newGroupName || (currentUser.disposition === 'admin' && !selectedLeaderId)">Mentés</button>
        </div>
      </div>

      <div v-if="showMemberModal" class="custom-modal shadow-lg">
        <h4 class="mb-3 text-center">Tagok hozzáadása</h4>
        <div class="scroll-list">
          <div v-for="u in freeUsers" :key="u.card_id" class="list-item" @click="addMemberToGroup(u.card_id)">
            <span>{{ u.full_name }}</span>
            <i class="bi bi-plus-circle text-accent"></i>
          </div>
          <div v-if="freeUsers.length === 0" class="p-4 text-center text-muted">Nincs szabad dolgozó.</div>
        </div>
        <button class="btn custom-btn-primary w-100 mt-4" @click="closeModals">Bezárás</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const allUsers = ref([]);
const showGroupModal = ref(false);
const showMemberModal = ref(false);
const newGroupName = ref('');
const activeGroupName = ref('');
const selectedLeaderId = ref('');
const currentUser = ref(JSON.parse(localStorage.getItem('user') || '{}'));

const fetchData = async () => {
  const token = localStorage.getItem('token');
  try {
    const res = await axios.get('http://localhost:8000/user/all', { params: { token } });
    if (res.data.status === 1) allUsers.value = res.data.users;
  } catch (err) { console.error(err); }
};

onMounted(fetchData);

const freeLeaders = computed(() => 
  allUsers.value.filter(u => 
    u.disposition?.toLowerCase().includes('leader') && 
    (!u.group_name || u.group_name === 'null' || u.group_name === 'None' || u.group_name === '')
  )
);

const freeUsers = computed(() => 
  allUsers.value.filter(u => (!u.group_name || u.group_name === 'null' || u.group_name === 'None' || u.group_name === ''))
);

const getSelectedLeaderName = computed(() => {
  if (!selectedLeaderId.value) return 'Válassz egy vezetőt...';
  const leader = freeLeaders.value.find(l => l.card_id === selectedLeaderId.value);
  return leader ? leader.full_name : 'Válassz egy vezetőt...';
});

const displayGroups = computed(() => {
  const groupsMap = {};
  allUsers.value.forEach(u => {
    if (u.group_name && u.group_name !== 'null' && u.group_name !== 'None' && u.group_name !== '') {
      if (!groupsMap[u.group_name]) groupsMap[u.group_name] = { name: u.group_name, leader: '', members: [] };
      if (u.disposition?.toLowerCase().includes('leader')) {
        groupsMap[u.group_name].leader = u.full_name;
      } else {
        groupsMap[u.group_name].members.push({ full_name: u.full_name, card_id: u.card_id });
      }
    }
  });
  return Object.values(groupsMap);
});

const openAddMember = (name) => {
  activeGroupName.value = name;
  showMemberModal.value = true;
};

// JAVÍTVA: Hozzáadva a .value minden ref változóhoz
const closeModals = () => {
  showGroupModal.value = false;
  showMemberModal.value = false;
  newGroupName.value = '';
  selectedLeaderId.value = '';
};

const handleCreateGroup = async () => {
  try {
    const leaderId = currentUser.value.disposition === 'admin' ? selectedLeaderId.value : currentUser.value.card_id;
    await axios.post(`http://localhost:8000/group/register`, null, {
      params: { 
        group_name: newGroupName.value, 
        token: localStorage.getItem('token'),
        leader_card_id: leaderId
      }
    });
    fetchData(); 
    closeModals();
  } catch (err) { console.error(err); }
};

const handleDeleteGroup = async (name) => {
  if (!confirm(`Biztosan törlöd a(z) ${name} csoportot?`)) return;
  try {
    const res = await axios.put(`http://localhost:8000/group/delete_group`, null, {
      params: { group_name: name, token: localStorage.getItem('token') }
    });
    if (res.data.status === 1) fetchData();
    else alert(res.data.message);
  } catch (err) { console.error(err); }
};

const addMemberToGroup = async (card_id) => {
  try {
    await axios.post(`http://localhost:8000/user/update_group`, null, {
      params: { card_id, group_name: activeGroupName.value, token: localStorage.getItem('token') }
    });
    fetchData(); 
    closeModals();
  } catch (err) { console.error(err); }
};

const removeMemberFromGroup = async (card_id) => {
  if (!confirm("Eltávolítod a tagot?")) return;
  try {
    await axios.put(`http://localhost:8000/group/delete_member`, null, {
      params: { card_id: card_id, token: localStorage.getItem('token') }
    });
    fetchData();
  } catch (err) { console.error(err); }
};
</script>

<style scoped>
.page-container { padding: 2rem; min-height: 100vh; background-color: var(--bg-main); }
.page-content-box { background-color: var(--bg-card); color: var(--text-main); padding: 2.5rem; border-radius: 16px; max-width: 900px; margin: 0 auto; border: 1px solid var(--border-color); }
.section-title { border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem; margin-bottom: 2.5rem; }
.profile-section { background-color: var(--bg-inner); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); }

.custom-input, .custom-select-btn {
  background-color: var(--bg-inner) !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-main) !important;
  padding: 0.75rem;
  border-radius: 8px;
}

.custom-dropdown-menu {
  background-color: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

.custom-dropdown-menu .dropdown-item {
  color: var(--text-main) !important;
}

.custom-dropdown-menu .dropdown-item:hover {
  background-color: var(--accent) !important;
  color: white !important;
}

.custom-btn-primary { background-color: var(--accent); color: white; border: none; font-weight: 600; padding: 0.8rem; border-radius: 8px; }

.btn-dark-outline {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-main);
  font-weight: 500;
}

.data-row { display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px dashed var(--border-color); align-items: center; }
.header-row { border-bottom: 2px solid var(--accent) !important; }
.role-badge { background: var(--accent); color: white; padding: 3px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; }

.member-chip { 
  background: var(--bg-card); 
  border: 1px solid var(--border-color); 
  padding: 5px 12px; 
  border-radius: 20px; 
  display: flex; 
  align-items: center;
  gap: 8px;
  color: var(--text-main);
}

.btn-remove-member {
  background: none; border: none; padding: 0; color: #ff4d4d; cursor: pointer; display: flex; align-items: center;
}

.add-member-btn { color: var(--accent); background: transparent; border: 1px solid var(--accent); border-radius: 50%; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; }

.custom-backdrop { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 1050; backdrop-filter: blur(4px); }
.custom-modal { background: var(--bg-card); padding: 2rem; border-radius: 16px; width: 95%; max-width: 400px; border: 1px solid var(--border-color); color: var(--text-main); }
.scroll-list { max-height: 250px; overflow-y: auto; background-color: var(--bg-inner); border: 1px solid var(--border-color); border-radius: 10px; }
.list-item { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid var(--border-color); cursor: pointer; color: var(--text-main); }
.text-accent { color: var(--accent) !important; }
</style>