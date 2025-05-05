declare module '@/stores/data.js' {
    import { Ref } from 'vue'
  
    type Selection = string[]
  
    export const useDataStore: () => {
      currentSelection: Ref<Selection>
      selectionID: string
  
      getSelectionId: (selection: string) => Promise<string>
      getCurrentSelection: () => Selection
      getSelectionID: () => string
      setCurrentSelection: (value: Selection) => void
      setSelectionID: (value: string) => void
    }
  
    export default useDataStore
  }
  