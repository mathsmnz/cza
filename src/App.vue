<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <div class="flex flex-col h-screen">
    <header>
      <NavBar />
    </header>

    <main class="grow">
      <RouterView />
    </main>
  </div>
</template>

<style scoped></style>
