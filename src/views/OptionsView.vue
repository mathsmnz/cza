<template>
  <div class="h-full w-full overflow-auto bg-white">
    <div class="grid h-full grid-rows-5 md:grid-rows-none md:grid-cols-5">

      <!-- Left Panel (Image) -->
      <div
        class="border-b-2 border-black md:border-r-2 md:border-b-0 flex justify-center items-center row-span-1 md:col-span-2 p-4">
        <div class="relative w-full h-full flex items-center justify-center">
          <img alt="casa" class="w-auto h-auto max-w-full max-h-full object-contain md:rotate-90 rotate-0"
            :src="imagePath" @error="handleImageError" />
        </div>
      </div>

      <!-- Right Panel (Options) -->
      <div class="row-span-4 md:col-span-3">
        <OptionSelector :optionsData="option" :selectionsData="selections" v-model="selectedInfo"
          class="md:h-full md:w-full" />
      </div>

    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import options from '@/data/options.json'
import OptionSelector from '@/components/OptionSelector.vue'
import { useDataStore } from '@/stores/data'

export default {
  components: {
    OptionSelector,
  },
  setup() {
    const store = useDataStore();
    const selectedInfo = ref([])
    const option = ref(options.data)
    const selections = ref(options.selections)
    const displayId = ref('')
    const imagePath = ref('')

    watch(selectedInfo, (newVal) => {
      if (newVal.length !== 0) {
        const sortedCombos = [newVal].sort()
        //const fileId = btoa(sortedCombos.join(","));
        store.getSelectionId(sortedCombos.join(',')).then((uniqueId) => {
          return (displayId.value = uniqueId)
        })
        console.log('DisplayID is: ', displayId.value)
      }
    })

    watch(displayId, (newVal) => {
      const basePath = '/images/'
      imagePath.value = basePath + newVal + '.png'
    })

    const handleImageError = () => {
      imagePath.value = "/images/base.png"; // Set the backup image when the original fails
      console.log("NO VALID COMBINATION FOUND");
    };

    return {
      selectedInfo,
      displayId,
      option,
      selections,
      imagePath,
      handleImageError,
    }
  },
}
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>
