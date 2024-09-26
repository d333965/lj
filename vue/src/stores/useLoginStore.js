import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoginStore = defineStore('login', () => {
  const dialogVisible = ref(true)
  const isLogin = ref(false)
  const manager = ref('')
  const show_admin_dialog = ref(false) 
  const managers = ref([])

  const login = (managerName) => {
    isLogin.value = true
    manager.value = managerName
  }

  const logout = () => {
    isLogin.value = false
    manager.value = ''
  }



  return {
    dialogVisible,
    isLogin,
    manager,
    login,
    logout,
    show_admin_dialog,
    managers,
  }
}, {
    persist: {
        key: "managerInfo",
        paths: ['isLogin','manager'], // 只持久化 isLogin 和 manager
      }
})
