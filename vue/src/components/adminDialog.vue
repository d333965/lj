<template>
  <el-dialog
    v-model="loginStore.show_admin_dialog" 
    title="管理员对话框"
    width="550"
  >
    <el-table 
      :data="loginStore.managers" 
      style="width: 100%" 
      :highlight-current-row="true"
    >
      <el-table-column
        prop="manager"
        label="管理员"
        width="180"
      ></el-table-column>
      <el-table-column
        prop="score"
        label="乐点"
        width="150"
      >
        <template #default="scope">
          <span v-if="!isEditing(scope.row.id)">{{ scope.row.score }}</span>
          <el-input
            v-else
            v-model.number="editedScores[scope.row.id]"
            type="number"
            min="0"
            style="width: 100px;"
          />
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="200"
      >
        <template #default="scope">
          <el-button 
            type="primary" 
            size="mini" 
            @click="startEdit(scope.row)"
            v-if="!isEditing(scope.row.id)"
          >编辑</el-button>
          <el-button 
            type="success" 
            size="mini" 
            @click="saveEdit(scope.row)"
            v-else
          >保存</el-button>
          <el-button 
            type="warning" 
            size="mini" 
            @click="cancelEdit(scope.row)"
            v-if="isEditing(scope.row.id)"
          >取消</el-button>
        </template>
      </el-table-column>
    </el-table>
    <span slot="footer" class="dialog-footer">
      <el-button @click="loginStore.show_admin_dialog = false">关闭</el-button>
    </span>
  </el-dialog>
</template>

<script setup>
import { useLoginStore } from '@/stores/useLoginStore'
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const loginStore = useLoginStore()
const editingManagerId = ref(null)
const editedScores = reactive({})

const isEditing = (id) => editingManagerId.value === id

const startEdit = (manager) => {
  editingManagerId.value = manager.id
  editedScores[manager.id] = manager.score
}

const saveEdit = async (manager) => {
  const newScore = editedScores[manager.id]
  if (newScore < 0) {
    ElMessage.error('乐点数不能为负数')
    return
  }
  try {
    const response = await axios.post('/api/manager/updateManager', {
      manager: loginStore.manager,
      username: manager.manager,
      score: newScore
    })
    if (response.data.code === 200) {
      // 更新 store 中的 managers
      const updatedManager = loginStore.managers.find(m => m.id === manager.id)
      if (updatedManager) {
        updatedManager.score = newScore
      }
      ElMessage.success('乐点更新成功')
      cancelEdit(manager)
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('更新乐点失败:', error)
    ElMessage.error('更新乐点时发生错误')
  }
}

const cancelEdit = (manager) => {
  editingManagerId.value = null
  delete editedScores[manager.id]
}
</script>

<style scoped>
.el-table .el-button {
  margin-right: 5px;
}
</style>
