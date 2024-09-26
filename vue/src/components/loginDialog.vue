<template>
    <el-dialog
      v-model="loginStore.dialogVisible"
      :title="isLogin ? '登录' : '注册'"
      :width="dialogWidth"
      :before-close="handleClose"
    >
      <el-form :model="form" :rules="rules" ref="formRef" class="login-form">
        <el-form-item prop="username" label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input
            v-model="form.password"
            :type="passwordVisible ? 'text' : 'password'"
            placeholder="请输入密码"
          >
            <template #suffix>
              <span class="password-icon" @click="togglePasswordVisibility">
                <svg v-if="passwordVisible" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                  <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
                  <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
                  <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/>
                  <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"/>
                  <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"/>
                </svg>
              </span>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="switchMode">{{ isLogin ? '切换到注册' : '切换到登录' }}</el-button>
          <el-button :type="isLogin ? 'primary' : 'success'" @click="submitForm">{{ isLogin ? '登录' : '注册' }}</el-button>
        </span>
      </template>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref, computed, reactive } from 'vue'
  import { ElMessageBox, ElMessage } from 'element-plus'
  import axios from 'axios'
  import { useLoginStore } from '@/stores/useLoginStore'

  const loginStore = useLoginStore()
  const isLogin = ref(true)
  const formRef = ref(null)

  const form = reactive({
    username: '',
    password: ''
  })

  const rules = {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
  }

  const dialogWidth = computed(() => {
    return window.innerWidth <= 768 ? '90%' : '30%'
  })

  const handleClose = (done) => {
    ElMessageBox.confirm('确定要关闭吗？')
      .then(() => {
        done()
      })
      .catch(() => {
        // catch error
      })
  }

  const switchMode = () => {
    isLogin.value = !isLogin.value
  }

  const submitForm = async () => {
    if (!formRef.value) return
    
    await formRef.value.validate(async (valid) => {
      if (valid) {
        try {
          const url = isLogin.value ? '/api/manager/login' : '/api/manager/register'
          const response = await axios.post(url, {
            manager: form.username,
            password: form.password
          })
          if (response.data.code === 200) {
            loginStore.login(form.username)
            ElMessage.success(isLogin.value ? '登录成功' : '注册成功')
            loginStore.dialogVisible = false
            window.location.reload()
          } else {
            ElMessage.error(response.data.message || '操作失败，请重试')
          }
          // 这里可以添加登录成功后的处理逻辑，比如保存token、跳转页面等
        } catch (error) {
          ElMessage.error(error.response?.data?.message || '操作失败，请重试')
        }
      } else {
        ElMessage.error('请填写正确的信息')
      }
    })
  }

  const passwordVisible = ref(false)

  const togglePasswordVisibility = () => {
    passwordVisible.value = !passwordVisible.value
  }

  // 添加窗口大小变化监听
  window.addEventListener('resize', () => {
    // 强制更新 computed 属性
    dialogWidth.value
  })
  </script>
  <style scoped>
  .dialog-footer button:first-child {
    margin-right: 10px;
  }
  .password-icon {
    cursor: pointer;
    display: flex;
    align-items: center;
    height: 100%;
  }
  .password-icon svg {
    vertical-align: middle;
  }
  .login-form {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding: 0 10px;
  }
  .login-form :deep(.el-form-item) {
    margin-bottom: 20px;
  }
  .login-form :deep(.el-form-item__label) {
    text-align: right;
    width: 70px;
    padding-right: 8px;
  }
  .login-form :deep(.el-form-item__content) {
    margin-left: 30px !important;
  }
  .login-form :deep(.el-input) {
    width: 100%;
  }
  .login-form :deep(.el-input__wrapper) {
    width: 100%;
  }
  .login-form :deep(.el-input__suffix) {
    display: flex;
    align-items: center;
  }

  @media screen and (max-width: 768px) {
    .login-form {
      padding: 0 5px;
    }
    .login-form :deep(.el-form-item__label) {
      width: 60px;
      padding-right: 5px;
    }
    .login-form :deep(.el-form-item__content) {
      margin-left: 20px !important;
    }
  }
  </style>
