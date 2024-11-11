<template>
    <div class="flex flex-col gap-4 px-4 outline outline-2 outline-black">
        <div class="flex flex-col gap-2 text-2xl">
            <span class="font-semibold">
                Selecione o tipo de mudança que deseja fazer
            </span>
            <span class="w-5/6 text-lg font-light">
                (Será possível mudar essa escolha mais tarde na opção "Redefinir o tipo de mudança")
            </span>

            <div class="w-full h-full">
                <div v-for="(option, index) in options" :key="index" class="flex flex-col">
                    <label for="thing" class="flex items-center">
                        <input type="checkbox" :name="option.group" :value="option.group" class="mr-2" />
                        <span class="text-base font-semibold">{{ option.label }}</span>
                    </label>
                    <div v-for="(combo, comboIndex) in option.combos" class="ml-6">
                        <label class="flex items-center">
                            <input type="checkbox" v-model="combo.selected" class="mr-2">
                            <span class="text-sm">{{ combo.label }}</span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
    props: {
        optionsData: {
            type: Array,
            required: true,
        },
        selectedInfo: {
            type: Array,
            required: true,
        },
    },
    setup(props) {
        const options = ref(props.optionsData.map(option => ({
            ...option,
            combos: option.combos.map(combo => ({ ...combo, selected: false }))
        })));

        const isOpen = (index) => openAccordion.value === index;

        const resetForm = () => {
            options.value.forEach(option => {
                option.combos.forEach(combo => {
                    combo.selected = false;
                });
            });
            props.selectedInfo.length = 0; // Reset the selected info in the parent
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
            isOpen,
            resetForm,
            submitForm,
        };
    },
};
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>