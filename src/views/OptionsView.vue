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
            <!-- The selected info will be displayed here -->
            {{ selectedInfo }}
          </div>
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
                      <input :name="option.group" type="radio" :value="[combo, option.group]" v-model="selectedInfo"
                        class="mr-2">
                      {{ combo.label }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex flex-row w-full gap-2 mt-4">
                <!-- Botão para enviar o formulário -->
                <button @click="submitForm" :disabled="selectedInfo.length === 0"
                  class="w-5/6 p-4 bg-black text-white rounded-xl 
                       disabled:text-gray-600 disabled:cursor-not-allowed disabled:bg-gray-400">Prosseguir</button>
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
import { ref, watch } from 'vue';
import optionsData from '@/data/optionsData.json';

export default {
  setup() {
    const openAccordion = ref(null);
    const options = ref(optionsData.map(option => ({
      ...option,
      combos: option.combos.map(combo => ({ ...combo, selected: false }))
    })));

    const selectedInfo = ref([])

    console.log(options);

    watch(
      () => selectedInfo.value,
      (newVal) => {
        console.log(newVal)
      }
    )

    const toggleAccordion = (index) => {
      openAccordion.value = openAccordion.value === index ? null : index;
    };

    const isOpen = (index) => openAccordion.value === index;

    const updateAssociatedOption = (optionLabel, combo, group) => {
      if (combo.selected) {
        console.log(`Selecionado: ${optionLabel} ${group} - ${combo.label} (${combo.associated})`);
      }
    };

    const updateSelections = (optionLabel, selectedCombo) => {
      selectedCombo.selected = !selectedCombo.selected;

      if (selectedCombo.selected) {
        // Desativa as opções incompatíveis
        options.value.forEach(option => {
          option.combos.forEach(combo => {
            if (combo !== selectedCombo) {
              combo.available = false;
            }
          });
        });
      } else {
        // Reativa todas as opções quando desmarcado
        options.value.forEach(option => {
          option.combos.forEach(combo => {
            combo.available = true;
          });
        });
      }
    };

    const resetForm = () => {
      // options.value.forEach(option => {
      //   option.combos.forEach(combo => combo.selected = false);
      // });
      selectedInfo.value = []
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
      selectedInfo,
      openAccordion,
      toggleAccordion,
      isOpen,
      updateAssociatedOption,
      updateSelections,
      resetForm,
      submitForm
    };
  }
};
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>
