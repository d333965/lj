import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEpayStore = defineStore('epay', () => {
  const dialogName = ref('选择套餐')
  const show_epay_dialog = ref(false)
  const score = ref(0)
  const rate = ref(0.16)
  const showConfirm = ref(false) // 新增状态
  
  // 添加新的函数来更新 score 和 rate
  const updatePackage = (newScore, newRate) => {
    score.value = newScore
    rate.value = newRate
  }

  const setShowConfirm = (value) => { // 新增方法
    showConfirm.value = value
  }

  return {
    dialogName,
    show_epay_dialog,
    score,
    rate,
    showConfirm,
    updatePackage,
    setShowConfirm
  }
})
