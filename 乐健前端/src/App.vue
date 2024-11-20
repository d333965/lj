<template >
  <Headbar />
  <LoginDialog />
  <AdminDialog v-if="loginStore.show_admin_dialog" />
  <EpayDialog v-if="epayStore.show_epay_dialog" />
  <router-view></router-view>
</template>

<script setup>
import { useLoginStore } from '@/stores/useLoginStore'
import { useEpayStore } from '@/stores/useEpayStore'
import Headbar from '@/components/headbar.vue'
import LoginDialog from '@/components/loginDialog.vue'
import AdminDialog from '@/components/adminDialog.vue'
import EpayDialog from '@/components/Epay/epayDialog.vue'
const loginStore = useLoginStore()
const epayStore = useEpayStore()
// 页面进入的时候，检查如果没有登录，则弹出登录对话框
if (!loginStore.isLogin) {
  loginStore.dialogVisible = true
}
</script>
