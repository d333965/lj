<template>
  <el-card class="confirm-card" >
    <div class="package-details">
      <p><strong>选择的套餐：</strong><span>{{ packageInfo.score }} 乐点</span></p>
      <p><strong>单价：</strong><span>{{ packageInfo.rate }}/km</span></p>
      <p><strong>总价：</strong><span>￥{{ packageInfo.price }}</span></p>
    </div>
    <el-button type="primary" @click="confirmOrder" :loading="isLoading">确认支付</el-button>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useEpayStore } from '@/stores/useEpayStore'
import { useLoginStore } from '@/stores/useLoginStore'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const epayStore = useEpayStore()
const loginStore = useLoginStore()
const isLoading = ref(false)

const packageInfo = computed(() => ({
  score: epayStore.score,
  rate: epayStore.rate,
  price: (epayStore.score * epayStore.rate).toFixed(2)
}))

const confirmOrder = async () => {
  isLoading.value = true
  try {
    // 调用API并获取返回的HTML内容
    const response = await axios.post('/api/epay/epay_order', {
      manager: loginStore.manager,
      out_trade_no: Date.now(),
      type: 'alipay',
      score: packageInfo.value.score,
      rate: packageInfo.value.rate,
      price: packageInfo.value.price
    })
    
    // 创建一个新的窗口并写入HTML内容
    const paymentWindow = window.open('', '_blank')
    paymentWindow.document.write(response.data)
    paymentWindow.document.close()

    ElMessage.success('订单提交成功！请在新窗口完成支付')
    setTimeout(() => {
      epayStore.setShowConfirm(false)
      epayStore.show_epay_dialog = false // 关闭对话框
    }, 1000)
  } catch (error) {
    ElMessage.error('订单提交失败，请重试')
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.confirm-card {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.package-details {
  margin-bottom: 20px;
}

.package-details p {
  margin: 10px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.package-details p strong {
  width: 100px;
  text-align: right;
  margin-right: 5px;
}

.package-details p span {
  width: 100px;
  text-align: left;
}
</style>
