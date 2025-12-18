<template>
  <div class="user-card">
    <h3 class="user-title">{{ user.username }}</h3>
    <div class="user-info">
      <p>Szerepkör: <span class="role-text">{{ user.role }}</span></p>
      <p>Email: <span class="info-value">{{ user.email }}</span></p>
      <p>Regisztrálva: <span class="info-value">{{ user.created_at }}</span></p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  user: Object
})
</script>

<style scoped>
.user-card {
  /* Fix #222831 helyett a belső háttér változó */
  background-color: var(--bg-inner); 
  color: var(--text-main); 
  padding: 1.25rem;
  border-radius: 12px;
  margin: 1rem 0;
  /* Az accent színünket használjuk a kerethez */
  border: 1px solid var(--accent);
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.user-title {
  color: var(--text-main);
  margin-top: 0;
  /* Fix #393E46 helyett a téma szerinti szegély */
  border-bottom: 1px dashed var(--border-color); 
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.user-info p {
  margin-bottom: 0.4rem;
  font-size: 0.95rem;
  color: var(--text-main);
  opacity: 0.9;
}

.info-value {
    color: var(--text-main);
}

.role-text {
  font-weight: bold; 
  /* Kiemelő szín sötétben bézs, világosban sötétszürke */
  color: var(--accent); 
  text-transform: capitalize;
}

/* Hover effektus, hogy interaktívabb legyen */
.user-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-hover);
}
</style>