<template>
    <el-card class="package-card" v-for="(pkg, index) in packages" :key="index">
      <div class="package-info">
        <span class="points">{{ pkg.points }} 乐点</span>
        <el-button 
          :type="selectedPackage?.points === pkg.points ? 'success' : 'primary'" 
          plain 
          circle 
          size="small" 
          @click="handlePackageSelection(pkg)"
        >
          <el-icon>
            <component :is="selectedPackage?.points === pkg.points ? 'Check' : 'Plus'" />
          </el-icon>
        </el-button>
      </div>
      <div class="package-price">
        <span class="price">￥{{ calculatePrice(pkg.points, pkg.rate) }}</span>
        <span class="explain">{{ pkg.rate }}/km</span>
      </div>
    </el-card>

    <!-- 自定义乐点选项 -->
    <el-card class="package-card custom-package">
      <div class="package-info">
        <el-input-number
          v-model="customPoints" 
          :min="200" 
          :controls="false"
          placeholder="自定义乐点"
          @focus="showCustomPointsTip"
        />
        <el-button 
          :type="isCustomPackageSelected ? 'success' : 'primary'" 
          plain 
          circle 
          size="small" 
          @click="handleCustomPackageSelection" 
          :disabled="!isValidCustomPoints"
        >
          <el-icon>
            <component :is="isCustomPackageSelected ? 'Check' : 'Plus'" />
          </el-icon>
        </el-button>
      </div>
      <div class="package-price" v-if="isValidCustomPoints">
        <span class="price">￥{{ customPrice }}</span>
        <span class="explain">0.16/km</span>
      </div>
    </el-card>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { ref, computed } from 'vue'
import { useEpayStore } from '@/stores/useEpayStore'

const epayStore = useEpayStore()

const packages = [
  { points: 500, rate: '0.16' },
  { points: 1000, rate: '0.14' },
  { points: 2000, rate: '0.12' },
  { points: 5000, rate: '0.10' },
]

const calculatePrice = (points, rate) => {
  return (points * parseFloat(rate)).toFixed(2)
}

const customPoints = ref(200)
const selectedPackage = ref(null)
const isCustomPackageSelected = ref(false)

const isValidCustomPoints = computed(() => customPoints.value >= 200)

const customPrice = computed(() => calculatePrice(customPoints.value, 0.16))

const showCustomPointsTip = () => {
  ElMessage({
    message: '请输入不少于200的乐点数量',
    type: 'info',
    duration: 3000
  })
}

const handlePackageSelection = (pkg) => {
  if (selectedPackage.value?.points === pkg.points) {
    selectedPackage.value = null
    epayStore.updatePackage(0, 0.16) // 重置为默认值
  } else {
    selectedPackage.value = pkg
    isCustomPackageSelected.value = false
    epayStore.updatePackage(pkg.points, parseFloat(pkg.rate))
    ElMessage.success('选择成功')
    epayStore.setShowConfirm(true)
    epayStore.dialogName = '确认订单'
  }
  console.log('选择了套餐:', selectedPackage.value)
}

const handleCustomPackageSelection = () => {
  if (isValidCustomPoints.value) {
    if (isCustomPackageSelected.value) {
      isCustomPackageSelected.value = false
      epayStore.updatePackage(0, 0.16) // 重置为默认值
    } else {
      const customPackage = {
        points: customPoints.value,
        price: customPrice.value,
        rate: '0.16'
      }
      selectedPackage.value = null
      isCustomPackageSelected.value = true
      epayStore.updatePackage(customPoints.value, 0.16)
      ElMessage.success('选择成功')
      epayStore.setShowConfirm(true)
      epayStore.dialogName = '确认订单'
      console.log('选择了自定义套餐:', customPackage)
    }
  }
}
</script>

<style scoped>
.package-card {
  margin-bottom: 10px;
  border-radius: 10px;
}

.package-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.explain {
  margin-left: 15px;
  font-size: 12px;
  color: #909399;
}

.points {
  font-size: 18px;
  font-weight: bold;
}

.package-price {
  margin-top: 5px;
}

.price {
  font-size: 14px;
  color: #909399;
}

.custom-package .package-info {
  justify-content: space-between;
}

.custom-package .el-input-number {
  width: 150px;
}

.el-button.is-plain.el-button--success {
  color: #67c23a;
  border-color: #67c23a;
}

.el-button.is-plain.el-button--success:hover {
  background: #67c23a;
  color: #ffffff;
}
</style>
