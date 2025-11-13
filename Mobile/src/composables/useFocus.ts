import { onMounted } from 'vue'

export function useFocus() {
  onMounted(() => {
    const firstInput = document.querySelector('ion-input')
    if(firstInput) (firstInput as any).setFocus()
  })
}
