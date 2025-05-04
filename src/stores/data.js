import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useDataStore = defineStore('data', () => {
  const currentSelection = ref([])
  const selectionID = ref('')

  // Utility: Try loading from localStorage if empty
  function restoreFromLocalStorage() {
    if (currentSelection.value.length === 0) {
      const storedSelection = localStorage.getItem('currentSelection')
      if (storedSelection) {
        try {
          currentSelection.value = JSON.parse(storedSelection)
        } catch (e) {
          console.error('Failed to parse currentSelection from localStorage:', e)
        }
      }
    }

    if (!selectionID.value) {
      const storedSelectionID = localStorage.getItem('selectionID')
      if (storedSelectionID) {
        selectionID.value = storedSelectionID
      }
    }
  }

  // Sync to localStorage
  watch(
    currentSelection,
    (newVal) => {
      localStorage.setItem('currentSelection', JSON.stringify(newVal))
    },
    { deep: true },
  )

  watch(selectionID, (newVal) => {
    localStorage.setItem('selectionID', newVal)
  })

  // Hashing and ID logic
  async function getSelectionId(selection) {
    setCurrentSelection(selection)
    const encoder = new TextEncoder()
    const encodedText = encoder.encode(selection)
    const hash = await window.crypto.subtle.digest('SHA-256', encodedText)
    const hashArray = Array.from(new Uint8Array(hash))
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')
    setSelectionID(hashHex)
    return hashHex
  }

  // Getters
  function getCurrentSelection() {
    if (currentSelection.value.length === 0) restoreFromLocalStorage()
    return currentSelection.value
  }

  function getSelectionID() {
    if (!selectionID.value) restoreFromLocalStorage()
    return selectionID.value
  }

  // Setters
  function setCurrentSelection(value) {
    currentSelection.value = value
  }

  function setSelectionID(value) {
    selectionID.value = value
  }

  // Initial restore in case store is imported but not accessed yet
  restoreFromLocalStorage()

  return {
    currentSelection,
    selectionID,
    getSelectionId,
    getCurrentSelection,
    getSelectionID,
    setCurrentSelection,
    setSelectionID,
  }
})
