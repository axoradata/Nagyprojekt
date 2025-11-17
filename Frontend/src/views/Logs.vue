<template>
  <div class="page-container-dark">
    <div class="page-content-box">
      <LogTable />
    </div>
  </div>
</template>

<script setup>
import LogTable from '../components/LogTable.vue'
</script>

<style scoped>
.page-container-dark {
  /* Alap háttér, ami a main elemen belül van */
  background-color: #222831; 
  display: flex;
  justify-content: center;
  
  /* Hely a felső és alsó görgetéshez, ha szükséges */
  padding: 30px; 
  min-height: 100%; 
  width: 100%; 
}

.page-content-box {
  /* Kártya/Konténer háttér (világosabb sötét) */
  background-color: #393E46; 
  color: #DFD0B8; 
  
  padding: 2rem;
  border-radius: 16px;
  
  /* Szélesebb konténer a táblázatoknak */
  width: 900px; 
  max-width: 95%; 
  
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}
</style>