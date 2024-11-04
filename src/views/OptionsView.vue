<template>
  <main class="h-full w-full flex items-center justify-center bg-white">
    <div class="w-full h-full">
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-8 items-center h-full w-full">
        <!-- Imagem da capa com desfoque -->
        <div
          class="sm:col-span-2 flex justify-center sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full w-full">
          <img alt="casa" src="/casa.png?url" class="w-full h-full object-cover" />
        </div>

        <div class="sm:col-span-3 w-fit">
          <div class="flex flex-col gap-4 px-2">
            <div class="flex flex-col gap-2 text-2xl">
              <span class="font-semibold">
                O que deseja modificar?
              </span>
              <span class="w-5/6 text-lg font-light">
                (Será possível mudar essa escolha mais tarde na opção "Redefinir o tipo de mudança")
              </span>
            </div>
            <div class="flex flex-col bg-gray-100 border-black border-2 p-4 rounded-lg relative">
              <!-- Renderiza cada opção de modificação como um acordeão -->
              <div v-for="(option, index) in options" :key="index" class="mb-4 divide-y divide-solid divide-black">
                <div @click="toggleAccordion(index)" class="cursor-pointer flex justify-between items-center">
                  <span>{{ option.label }}</span>
                  <svg class="w-5 h-5 transform transition-transform" :class="{ 'rotate-180': isOpen(index) }"
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>

                <!-- Renderiza as opções combináveis dentro do acordeão -->
                <div v-show="isOpen(index)" class="pl-4 mt-2">
                  <div v-for="(combo, comboIndex) in option.combos" :key="comboIndex">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="combo.selected" class="mr-2"
                        @change="updateAssociatedOption(option.label, combo)">
                      {{ combo.label }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex flex-row w-full gap-2 mt-4">
                <!-- Botão para enviar o formulário -->
                <button @click="submitForm" class="w-5/6  p-4 bg-black text-white rounded-xl">Enviar</button>
                <!-- Botão para resetar o formulário -->
                <button @click="resetForm" class="p-4 bg-black text-white rounded-xl">Redefinir</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </main>
</template>

<script>
import { ref } from 'vue';
import optionsData from '@/data/optionsData.json';

export default {
  setup() {
    const openAccordion = ref(null);
    const options = ref(optionsData.map(option => ({
      ...option,
      combos: option.combos.map(combo => ({ ...combo, selected: false }))
    })));

    const toggleAccordion = (index) => {
      openAccordion.value = openAccordion.value === index ? null : index;
    };

    const isOpen = (index) => openAccordion.value === index;

    const updateAssociatedOption = (optionLabel, combo) => {
      if (combo.selected) {
        console.log(`Selecionado: ${optionLabel} - ${combo.label} (${combo.associated})`);
      }
    };

    const resetForm = () => {
      options.value.forEach(option => {
        option.combos.forEach(combo => combo.selected = false);
      });
    };

    const submitForm = () => {
      const selectedCombos = options.value
        .map(option => ({
          option: option.label,
          selectedCombos: option.combos.filter(combo => combo.selected)
        }))
        .filter(option => option.selectedCombos.length > 0);
      console.log('Formulário enviado!', selectedCombos);
      alert('Formulário enviado! Verifique o console para detalhes.');
    };

    return {
      options,
      openAccordion,
      toggleAccordion,
      isOpen,
      updateAssociatedOption,
      resetForm,
      submitForm
    };
  }
};
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>
