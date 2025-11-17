<template>
  <div id="app" class="d-flex min-vh-100">
    
    <!-- Sidebar mindenhol, kivéve Login -->
    <Sidebar v-if="$route.name !== 'Login'" />

    <!-- Tartalom -->
    <main 
      class="flex-grow-1"
      :class="{ 'ms-sidebar': $route.name !== 'Login' }"
    >
      <router-view />
    </main>

  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: { Sidebar }
}
</script>

<style scoped>

.ms-sidebar {
    margin-left: 240px;
    height: 100vh; 
    overflow-y: auto;
}
</style>
