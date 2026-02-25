<template>
  <div class="user-card">
    <h3 class="user-title">{{ user.full_name || 'Névtelen felhasználó' }}</h3>
    
    <div class="user-info">
      <p>Beosztás: <span class="role-text">{{ user.disposition || 'Nincs megadva' }}</span></p>
      
      <p>Kártya ID: <span class="info-value code-font">{{ user.card_id }}</span></p>
      
      <p v-if="user.group">Csoport: <span class="info-value">{{ user.group }}</span></p>
    </div>

    <div class="card-actions mt-3">
       <button @click="$emit('delete', user.card_id)" class="btn-delete">
         <i class="bi bi-trash"></i> Törlés
       </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

defineEmits(['delete'])
</script>

<style scoped>
.user-card {
  background-color: var(--bg-inner); 
  color: var(--text-main); 
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.user-title {
  color: var(--accent); /* Kiemeljük a nevet az accent színnel */
  margin-top: 0;
  border-bottom: 1px dashed var(--border-color); 
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  font-weight: bold;
}

.user-info p {
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.role-text {
  font-weight: bold; 
  color: var(--text-main);
  text-transform: uppercase;
  font-size: 0.85rem;
  background: var(--border-color);
  padding: 2px 8px;
  border-radius: 4px;
}

.code-font {
  font-family: monospace;
  background: rgba(0,0,0,0.1);
  padding: 2px 4px;
  border-radius: 4px;
}

.btn-delete {
  background: transparent;
  color: #e74c3c;
  border: 1px solid #e74c3c;
  border-radius: 6px;
  padding: 5px 10px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-delete:hover {
  background: #e74c3c;
  color: white;
}

.user-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}
</style>