<template>
  <el-dialog
    :title="epayStore.dialogName"
    v-model="epayStore.show_epay_dialog"
    :width="dialogWidth"
    :close-on-click-modal="false"
  >
    <template #title>
      <div class="dialog-title">
        <el-icon v-if="epayStore.showConfirm" class="back-icon" @click="goBack">
          <ArrowLeft />
        </el-icon>
        <span>{{ epayStore.dialogName }}</span>
      </div>
    </template>
    <select_package v-if="!epayStore.showConfirm" />
    <confirm_package v-else />
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useEpayStore } from '@/stores/useEpayStore'
import select_package from './select_package.vue'
import confirm_package from './confirm_package.vue'
import { ArrowLeft } from '@element-plus/icons-vue'

const epayStore = useEpayStore()
const isMobile = ref(false)

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  updateIsMobile()
  window.addEventListener('resize', updateIsMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateIsMobile)
})
const dialogWidth = computed(() => isMobile.value ? '90%' : '25%')

const goBack = () => {
  epayStore.setShowConfirm(false)
  epayStore.dialogName = '选择套餐'
}
</script>

<style scoped>
.dialog-title {
  display: flex;
  align-items: center;
}

.back-icon {
  margin-right: 10px;
  cursor: pointer;
}
</style>
