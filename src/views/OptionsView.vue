<template>
  <main class="h-full w-full flex items-center justify-center bg-white">
    <div class="w-full h-full">
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-8 items-center h-full w-full">
        <!-- Imagem da capa com desfoque -->
        <div
          class="relative sm:col-span-2 flex justify-center sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full w-full">
          <!-- Image with blur effect -->
          <img alt="casa" src="/casa.png?url" class="w-full h-full object-cover filter blur-sm" />

          <!-- Text overlay (selectedInfo) -->
          <div
            class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-4xl font-extrabold z-10">
            {{ selectedInfo }}
          </div>
        </div>

        <div class="sm:col-span-3 w-fit">
          <!-- Using the new SelectorB here -->
          <SelectorC :optionsData="option" :selectedInfo="selectedInfo" />
        </div>

      </div>
    </div>
  </main>
</template>

<script>
import { ref } from 'vue';
import optionsData from '@/data/optionsData.json';
import options from '@/data/options.json'
import SelectorB from '@/components/SelectorB.vue';
import SelectorA from '@/components/SelectorA.vue';
import SelectorC from '@/components/SelectorC.vue';

export default {
  components: {
    SelectorB,
    SelectorA,
    SelectorC
  },
  setup() {
    const selectedInfo = ref([]);
    const optionData = ref(optionsData);
    const option = ref(options);

    return {
      selectedInfo,
      option,
    };
  }
};
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>
