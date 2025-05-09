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
  
      telemetry: {
        userID: string
        sessionStart: number
        groupSelections: Record<string, number>
        comboSelections: Record<string, number>
        formSubmissions: number
        finalSelection: string[]
        formResets: number
        elapsedTime: number
      }
  
      trackGroupSelection: (groupID: string) => void
      trackComboSelection: (comboID: string) => void
      trackFormSubmission: () => void
      trackFormReset: () => void
      setFinalSelection: (selection: string[]) => void
    }
  
    export default useDataStore
  }
  