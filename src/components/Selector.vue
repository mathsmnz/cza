<template>
    <div class="w-full flex flex-col gap-2 p-6 bg-gray-100 outline outline-black outline-2">
        <!-- Section Header -->
        <div class="text-center">
            <h1 class="text-3xl font-bold text-gray-800">Escolha o Tipo de Mudança</h1>
            <p class="text-lg text-gray-600">
                Será possível alterar sua escolha mais tarde na opção
                <strong class="font-semibold text-gray-800">"Redefinir o tipo de mudança"</strong>.
            </p>
        </div>

        <!-- Options Section -->
        <div class="flex flex-col gap-2">
            <div
                v-for="(option, index) in options"
                :key="index"
                class="bg-white p-4 rounded-lg border border-gray-300 shadow-sm hover:shadow-md transition-shadow"
            >
                <!-- Main Option -->
                <label class="flex items-center gap-3 cursor-pointer">
                    <input
                        type="checkbox"
                        :name="option.id"
                        :value="option.id"
                        v-model="selectedGroups"
                        class="h-5 w-5 text-blue-600 focus:ring focus:ring-blue-300 rounded"
                    />
                    <span class="text-xl font-semibold text-gray-800">{{ option.label }}</span>
                </label>

                <!-- Nested Combos -->
                <div
                    v-for="(combo, comboIndex) in option.combos"
                    :key="comboIndex"
                    class="ml-6 mt-2"
                >
                    <label class="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            :name="combo.id"
                            :value="combo.associated"
                            v-model="selectedCombos"
                            :disabled="!selectedGroups.includes(option.id)"
                            class="h-4 w-4 text-blue-500 focus:ring focus:ring-blue-200 rounded"
                        />
                        <span
                            :class="{
                                'text-gray-700': selectedGroups.includes(option.id),
                                'text-gray-400': !selectedGroups.includes(option.id),
                            }"
                        >
                            {{ combo.label }}
                        </span>
                    </label>
                </div>
            </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-row w-full gap-2 mt-4">
            <!-- Button to submit the form -->
            <button
                @click="submitForm"
                :disabled="selectedCombos.length === 0"
                class="w-5/6 p-4 bg-black text-white rounded-xl disabled:text-gray-600 disabled:cursor-not-allowed disabled:bg-gray-400"
            >
                Prosseguir
            </button>
            <!-- Button to reset the form -->
            <button @click="resetForm" class="p-4 bg-black text-white rounded-xl">
                Redefinir
            </button>
        </div>
    </div>
</template>

<script>
import { ref, watch } from "vue";

export default {
    props: {
        optionsData: {
            type: Array,
            required: true,
        },
        modelValue: {
            type: Array,
            default: () => [],
        },
    },
    emits: ["update:modelValue"], // Declare emit event for v-model
    setup(props, { emit }) {
        const options = ref(props.optionsData);
        const selectedGroups = ref([]); // Tracks selected groups
        const selectedCombos = ref([...props.modelValue]); // Sync with modelValue

        // Watch selectedCombos to sync with parent
        watch(selectedCombos, (newCombos) => {
            emit("update:modelValue", newCombos); // Emit the updated value to parent
        });

        const resetForm = () => {
            // Clear selected groups and combos
            selectedGroups.value = [];
            selectedCombos.value = [];
        };

        const submitForm = () => {
            console.log("Formulário enviado!", selectedCombos.value);
            alert("Formulário enviado! Verifique o console para detalhes.");
        };

        return {
            options,
            selectedGroups,
            selectedCombos,
            resetForm,
            submitForm,
        };
    },
};
</script>

<style scoped>
/* Add styles if additional custom styling is necessary. Tailwind should cover most cases. */
</style>
