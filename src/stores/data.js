import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
  const currentSelection = ref([])
  const selectionID = ref('')

  async function getSelectionId(selection) {
    currentSelection.value = selection
    const enconder = new TextEncoder()
    const encodedText = enconder.encode(selection)
    const hash = await window.crypto.subtle.digest('SHA-256', encodedText)
    const hashArray = Array.from(new Uint8Array(hash)) // convert buffer to byte array
    // convert bytes to hex string
    selectionID.value = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')
    return selectionID.value
  }

  return { getSelectionId, currentSelection, selectionID }
})
