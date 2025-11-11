<template>
  <div class="auth-container">
    <div class="auth-box">
      <LogTable />
    </div>
  </div>
</template>

<script setup>
import LogTable from '../components/LogTable.vue'
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.auth-box {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  width: 600px;
}
</style>
