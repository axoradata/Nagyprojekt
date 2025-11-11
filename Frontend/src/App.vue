<template>
  <div id="app">
    <Sidebar v-if="$route.name !== 'Login'" />

    <main :class="{ 'with-sidebar': $route.name !== 'Login' }">
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
#app {
  display: flex;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

/* Alap layout */
main {
  flex: 1;
  color: #2c3e50;
  transition: margin-left 0.3s ease;
}

.with-sidebar {
  margin-left: 240px; 
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
