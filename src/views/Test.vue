<template>
    <div class="max-w-xl mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Customize Sua Casa</h1>
  
      <!-- Renderiza cada opção de modificação como um acordeão -->
      <div v-for="(option, index) in options" :key="index" class="mb-4">
        <div @click="toggleAccordion(index)" class="cursor-pointer p-2 bg-gray-200 rounded-md flex justify-between items-center">
          <span>{{ option.label }}</span>
          <svg class="w-5 h-5 transform transition-transform" :class="{'rotate-180': isOpen(index)}" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
  
        <!-- Renderiza as opções combináveis dentro do acordeão -->
        <div v-show="isOpen(index)" class="pl-4 mt-2">
          <div v-for="(combo, comboIndex) in option.combos" :key="comboIndex">
            <label class="flex items-center">
              <input type="checkbox" v-model="combo.selected" class="mr-2" @change="updateAssociatedOption(option.label, combo)">
              {{ combo.label }}
            </label>
          </div>
        </div>
      </div>
  
      <!-- Botão para enviar o formulário -->
      <button @click="submitForm" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md">Enviar</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        openAccordion: null,
        options: [
          {
            label: 'Separar Cozinha da Sala de Estar',
            combos: [
              { label: 'Expandir Cozinha/Sala de Estar para a Frente', selected: false, associated: 'Opção N' },
              { label: 'Expandir Cozinha/Sala de Estar para Frente e Lado', selected: false, associated: 'Opção D' }
            ]
          },
          {
            label: 'Expandir Cozinha/Sala de Estar para a Frente',
            combos: [
              { label: 'Separar Cozinha da Sala de Estar', selected: false, associated: 'Opção B' },
              { label: 'Expandir Cozinha/Sala de Estar para a Frente', selected: false, associated: 'Opção A' },
              { label: 'Expandir Cozinha/Sala de Estar para Frente e Lado', selected: false, associated: 'Opção C' },
              { label: 'Adicionar Cômodo na Frente', selected: false, associated: 'Opção N' },
              { label: 'Adicionar Cômodo nos Fundos', selected: false, associated: null }
            ]
          },
          {
            label: 'Expandir Cozinha/Sala de Estar para o Lado',
            combos: [
              { label: 'Expandir Cozinha/Sala de Estar para a Frente', selected: false, associated: 'Opção C' },
              { label: 'Expandir Cozinha/Sala de Estar para o Lado', selected: false, associated: 'Opção E' },
              { label: 'Adicionar Cômodo na Frente', selected: false, associated: 'Opção o' },
              { label: 'Adicionar Cômodo nos Fundos', selected: false, associated: 'Opção //' },
              { label: 'Adicionar Lavanderia', selected: false, associated: 'Opção F' }
            ]
          },
          {
            label: 'Expandir Cozinha/Sala de Estar para Frente e Lado',
            combos: [
              { label: 'Separar Cozinha da Sala de Estar', selected: false, associated: 'Opção D' },
              { label: 'Expandir Cozinha/Sala de Estar para Frente e Lado', selected: false, associated: 'Opção C' },
              { label: 'Adicionar Cômodo na Frente', selected: false, associated: 'Opção P' }
            ]
          },
          {
            label: 'Adicionar Cômodo na Frente',
            combos: [
              { label: 'Expandir Cozinha/Sala de Estar para a Frente', selected: false, associated: 'Opção N' },
              { label: 'Expandir Cozinha/Sala de Estar para o Lado', selected: false, associated: 'Opção O' },
              { label: 'Expandir Cozinha/Sala de Estar para Frente e Lado', selected: false, associated: 'Opção P' },
              { label: 'Adicionar Cômodo na Frente', selected: false, associated: 'Opção G' },
              { label: 'Adicionar Cômodo nos Fundos', selected: false, associated: 'Opção //' },
              { label: 'Adicionar Lavanderia', selected: false, associated: 'Opção L' }
            ]
          },
          {
            label: 'Adicionar Cômodo nos Fundos (pode incluir banheiro extra)',
            combos: [
              { label: 'Expandir Cozinha/Sala de Estar para a Frente', selected: false, associated: 'Opção //' },
              { label: 'Expandir Cozinha/Sala de Estar para o Lado', selected: false, associated: 'Opção //' },
              { label: 'Expandir Cozinha/Sala de Estar para Frente e Lado', selected: false, associated: 'Opção //' },
              { label: 'Adicionar Cômodo na Frente', selected: false, associated: 'Opção //' },
              { label: 'Adicionar Cômodo nos Fundos', selected: false, associated: 'Opções H/I/J/K' }
            ]
          },
          {
            label: 'Adicionar Lavanderia',
            combos: [
              { label: 'Expandir Cozinha/Sala de Estar para o Lado', selected: false, associated: 'Opção F' },
              { label: 'Adicionar Cômodo nos Fundos', selected: false, associated: 'Opção L' },
              { label: 'Adicionar Lavanderia', selected: false, associated: 'Opção M' }
            ]
          }
        ]
      };
    },
    methods: {
      toggleAccordion(index) {
        this.openAccordion = this.openAccordion === index ? null : index;
      },
      isOpen(index) {
        return this.openAccordion === index;
      },
      updateAssociatedOption(optionLabel, combo) {
        if (combo.selected) {
          console.log(`Selecionado: ${optionLabel} - ${combo.label} (${combo.associated})`);
        }
      },
      submitForm() {
        const selectedCombos = this.options
          .map(option => ({
            option: option.label,
            selectedCombos: option.combos.filter(combo => combo.selected)
          }))
          .filter(option => option.selectedCombos.length > 0);
        console.log('Formulário enviado!', selectedCombos);
        alert('Formulário enviado! Verifique o console para detalhes.');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Adicione estilos personalizados se necessário */
  </style>
  