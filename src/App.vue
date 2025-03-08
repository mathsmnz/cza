<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <div class="flex flex-col h-screen font-montserrat">
    <header>
      <NavBar />
    </header>

    <main class="flex grow">
      <RouterView />
    </main>
  </div>
</template>

<style scoped></style>
