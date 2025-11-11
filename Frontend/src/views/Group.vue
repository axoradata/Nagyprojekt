<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>Csoportok</h2>
      <div v-for="g in groups" :key="g.id" class="group-card">
        <h3>{{ g.name }}</h3>
        <p>Leader: {{ getLeaderName(g.leader_id) }}</p>
        <p>Tagok:</p>
        <ul class="list">
          <li v-for="memberId in g.members" :key="memberId">{{ getUserName(memberId) }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { groups, users } from '../data'

const getUserName = (id) => {
  const user = users.find(u => u.id === id)
  return user ? user.username : 'Ismeretlen'
}

const getLeaderName = (leader_id) => {
  return getUserName(leader_id)
}
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
  width: 400px;
}

.list li {
    text-align: left;
}

.group-card {
  background-color: #2c3e50;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  color: white;
}
</style>
