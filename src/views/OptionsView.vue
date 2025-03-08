<template>
  <main class="h-full w-full flex items-center justify-center bg-white">
    <div class="w-full h-full">
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-8 items-center h-full w-full">
        <div
<<<<<<< HEAD
          class="relative sm:col-span-2 flex justify-center align-middle sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full w-full"
        >
          <!-- Image with blur effect -->
          <img
            alt="casa"
            :src="imagePath"
            @error="handleImageError"
            :class="imagePath === 'casa.png' ? 'object-cover' : 'object-scale-down'"
=======
          class="relative sm:col-span-2 flex justify-center align-middle sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full w-full">
          <!-- Image with blur effect -->
          <img 
            alt="casa" 
            :src="imagePath" 
            @error="handleImageError" 
            :class="imagePath === 'casa.png' ? 'object-cover' : 'object-scale-down'" 
>>>>>>> 4b6490a5fec1bb0cb22ac4597e069628f18995bf
          />
        </div>

        <div class="sm:col-span-3 w-fit">
          <!-- Using the new SelectorB here -->
          <OptionSelector
            :optionsData="option"
            :selectionsData="selections"
            v-model="selectedInfo"
          />
        </div>
      </div>
    </div>
  </main>
</template>

<script>
<<<<<<< HEAD
import { ref, watch } from 'vue'
=======
import { ref, watch } from 'vue';
>>>>>>> 4b6490a5fec1bb0cb22ac4597e069628f18995bf
import options from '@/data/options.json'
import OptionSelector from '@/components/OptionSelector.vue'

export default {
  components: {
    OptionSelector,
  },
  setup() {
<<<<<<< HEAD
    const selectedInfo = ref([])
    const option = ref(options.data)
    const selections = ref(options.selections)
    const displayId = ref('')
    const imagePath = ref('')

    async function getSelectionId(selection) {
      const enconder = new TextEncoder()
      const encodedText = enconder.encode(selection)
      const hash = await window.crypto.subtle.digest('SHA-256', encodedText)
      const hashArray = Array.from(new Uint8Array(hash)) // convert buffer to byte array
      // convert bytes to hex string
      return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')
    }

    watch(selectedInfo, (newVal) => {
      if (newVal.length !== 0) {
        const sortedCombos = [newVal].sort()
        //const fileId = btoa(sortedCombos.join(","));
        getSelectionId(sortedCombos.join(',')).then((uniqueId) => (displayId.value = uniqueId))
=======
    const selectedInfo = ref([]);
    const option = ref(options.data);
    const displayId = ref("");
    const imagePath = ref("");

    async function getSelectionId(selection) {
      const enconder = new TextEncoder();
      const encodedText = enconder.encode(selection);
      const hash = await window.crypto.subtle.digest("SHA-256", encodedText);
      const hashArray = Array.from(new Uint8Array(hash)); // convert buffer to byte array
      const hashHex = hashArray
        .map((b) => b.toString(16).padStart(2, "0"))
        .join(""); // convert bytes to hex string
      return hashHex;
    }

    watch(selectedInfo, (newVal) => {
      if (newVal.length != 0) {
        const sortedCombos = [newVal].sort();
        const fileId = btoa(sortedCombos.join(","));
        getSelectionId(sortedCombos.join(",")).then((uniqueId) =>
          displayId.value = uniqueId)
>>>>>>> 4b6490a5fec1bb0cb22ac4597e069628f18995bf
        console.log('DisplayID is: ', displayId.value)
      }
    })

    watch(displayId, (newVal) => {
      const basePath = '/images/'
      imagePath.value = basePath + newVal + '.png'
    })

    const handleImageError = () => {
      imagePath.value = '/images/base.png' // Set the backup image when the original fails
      console.log('NO VALID COMBINATION FOUND')
    }

    watch(displayId, (newVal) => {
      const basePath = "/images/"
      imagePath.value = basePath + newVal + ".png";
    });

    const handleImageError = () => {
      imagePath.value = "/images/base.png"; // Set the backup image when the original fails
      console.log("NO VALID COMBINATION FOUND");
    };

    return {
      selectedInfo,
      displayId,
      option,
<<<<<<< HEAD
      selections,
      imagePath,
      handleImageError,
    }
  },
}
=======
      imagePath,
      handleImageError,
    };
  }
};
>>>>>>> 4b6490a5fec1bb0cb22ac4597e069628f18995bf
</script>

<style scoped>
/* Estilos personalizados, se necessário */
</style>
