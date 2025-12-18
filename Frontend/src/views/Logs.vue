<template>
  <div class="page-container">
    <div class="page-content-box">
      <h2 class="section-title">Eseménynapló</h2>
      <LogTable />
    </div>
  </div>
</template>

<script setup>
import LogTable from '../components/LogTable.vue'
</script>

<style scoped>
.page-container {
  /* Fix #222831 helyett a fő háttér */
  background-color: var(--bg-main); 
  display: flex;
  justify-content: center;
  padding: 30px; 
  min-height: 100vh; 
  width: 100%; 
  transition: background-color 0.3s ease;
}

.page-content-box {
  /* Fix #393E46 helyett a kártya háttér */
  background-color: var(--bg-card); 
  color: var(--text-main); 
  
  padding: 2rem;
  border-radius: 16px;
  
  /* Szélesebb konténer a táblázatoknak */
  width: 1000px; 
  max-width: 95%; 
  
  /* Finomabb keret és dinamikus árnyék */
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
</style>