<template>
  <nav>
    <ul>
      <li><router-link to="/create">创建订单</router-link></li>
      <li><router-link to="/getInfo">详情</router-link></li>
    </ul>
    <el-dropdown>
      <span class="el-dropdown-link">
        <el-avatar shape="square" :size="40" :src="'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png'" />
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="loginStore.dialogVisible = true" v-if="!loginStore.isLogin">登录</el-dropdown-item>
          <el-dropdown-item @click="logout" v-if="loginStore.isLogin">退出</el-dropdown-item>
          <el-dropdown-item @click="admin" v-if="is_admin">管理员</el-dropdown-item>
          <el-dropdown-item disabled>乐点 : {{ score }}</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </nav>
</template>

<script setup>
import { useLoginStore } from '@/stores/useLoginStore'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const loginStore = useLoginStore()
const score = ref(0)
const is_admin = ref(false)

const logout = () => {
  loginStore.logout()
  window.location.reload()
}

const getManagerScore = async () => {
  if (loginStore.isLogin) {
    try {
      const response = await axios.post('/api/manager/getManagerScore', {
        manager: loginStore.manager
      })
      if (response.data.code === 200) {
        score.value = response.data.score
        is_admin.value = response.data.is_admin || false
      } else {
        ElMessage.error('获取乐点失败: ' + response.data.message)
      }
    } catch (error) {
      console.error('获取乐点失败:', error)
      ElMessage.error(error.response?.data?.message || '获取乐点失败')
    }
  }
}

onMounted(() => {
  getManagerScore()
})

const admin = async () => {
  if (!is_admin.value) {
    ElMessage.error('您没有管理员权限')
    return
  }
  loginStore.show_admin_dialog = true
  try {
    const response = await axios.post('/api/manager/getAllManager', { manager: loginStore.manager })
    if (response.data.code === 200) {
      // 更新 store 中的 managers
      loginStore.managers = response.data.data
      console.log(loginStore.managers)
    } else {
      ElMessage.error('获取管理员信息失败: ' + response.data.message)
    }
  } catch (error) {
    console.error('获取管理员信息失败:', error)
    ElMessage.error('获取管理员信息时发生错误')
  }
}
</script>

<style scoped>
nav {
  background-color: #333;
  padding: 1em;
  display: flex;
  justify-content: center; /* 居中导航菜单 */
  position: relative;
  margin-bottom: 10px;
}

.el-dropdown {
  position: absolute;
  right: 30px;
  top: 50%;
  transform: translateY(-50%);
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
}

li {
  margin-right: 1.5em;
}

a {
  color: rgb(135, 135, 135);
  text-decoration: none;
  font-weight: 500;
}

a.router-link-active {
  color: rgb(255, 255, 255);
}

a:hover {
  text-decoration: underline;
}

.el-dropdown-menu {
  min-width: 120px;
  display: flex;
  flex-direction: column; 
}

.el-avatar {
  cursor: pointer;
}
</style>