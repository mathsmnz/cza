<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <header>
    <NavBar />
  </header>

  <body class="h-dvh">
    <RouterView />
  </body>
</template>

<style scoped></style>
