<template>
  <div class="user-list-container">
    <div class="search-box">
      <el-input
        v-model="searchUser"
        placeholder="输入用户名搜索"
        class="search-input"
      />
      <el-button type="primary" @click="searchCustomer">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>
    <div class="user-list">
      <el-table :data="customers" stripe>
        <el-table-column prop="manager" label="管理员" />
        <el-table-column prop="create_time" label="创建时间" width="170" />
        <el-table-column prop="username" label="用户名" width="120"/>
        <el-table-column prop="password" label="密码" width="120"/>
        <el-table-column prop="schoolName" label="学校" />
        <el-table-column prop="runType" label="跑步类型" />
        <el-table-column prop="runTime" label="跑步时间" />
        <el-table-column prop="day_goals" label="每日目标(km)" />
        <el-table-column prop="day_in_week" label="每周目标(天)" />
        <el-table-column prop="complete_day_in_week" label="已完成(天)" />
        <el-table-column prop="total_goals" label="总目标(km)" />
        <el-table-column prop="complete_goals" label="已完成(km)" />
        <el-table-column label="跑步状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_run ? 'success' : 'info'">
              {{ scope.row.is_run ? '已完成' : '未完成' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="开始状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.begin_state ? 'success' : 'info'">
              {{ scope.row.begin_state ? '进行中' : '暂停中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button
              size="small"
              :type="scope.row.begin_state ? 'warning' : 'success'"
              @click="toggleBeginState(scope.row)"
            >
              {{ scope.row.begin_state ? '暂停' : '开始' }}
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteCustomer(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[15, 30, 50, 100]"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          layout="total, sizes, prev, pager, next, jumper"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useLoginStore } from '../stores/useLoginStore';
import axios from 'axios';
import { ElMessageBox, ElMessage } from 'element-plus';

const loginStore = useLoginStore();
const customers = ref([]);
const currentPage = ref(1);
const pageSize = ref(15); // 确保 pageSize 初始化
const total = ref(0);
const isLoading = ref(false); // 添加一个标志位
const searchUser = ref('');

const fetchCustomers = async () => {
  if (isLoading.value) return; // 如果正在加载，则不再请求
  isLoading.value = true; // 开始请求时将标志位设为true
  try {
    const response = await axios.post('/api/legymCustomer/get_info', {
      manager: loginStore.manager,
      pageSize: pageSize.value, // 确保传递 pageSize
      currentPage: currentPage.value,
      searchUser: searchUser.value, // 添加搜索参数
    });
    if (response.data.customer) {
      // 单个用户搜索结果
      customers.value = [response.data.customer];
      total.value = 1;
    } else {
      // 多个用户列表
      customers.value = response.data.customers;
      total.value = response.data.total;
      currentPage.value = response.data.currentPage;
      pageSize.value = response.data.pageSize;
    }
  } catch (error) {
    ElMessage.error(error.response.data.message);
  } finally {
    isLoading.value = false; // 请求结束时将标志位设为false
  }
};

// 确保 onMounted 只调用一次
onMounted(() => {
  fetchCustomers();
});

const handleSizeChange = (val) => {
  pageSize.value = val;
  fetchCustomers();
};

const handleCurrentChange = (val) => {
  currentPage.value = val;
  fetchCustomers();
};

const toggleBeginState = async (customer) => {
  try {
    const response = await axios.post('/api/legymCustomer/begin_state', {
      id: customer.id,
      manager: loginStore.manager,
      username: customer.username,
    });
    if (response.status === 200) {
      customer.begin_state = response.data.begin_state;
      ElMessage.success(response.data.message);
    }
  } catch (error) {
    console.error('更新开始状态失败：', error);
    ElMessage.error('更新开始状态失败');
  }
};

const deleteCustomer = async (customer) => {
  try {
    const result = await ElMessageBox.confirm(
      '确定要删除该用户吗？剩余乐点将返还。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    if (result === 'confirm') {
      const response = await axios.post('/api/legymCustomer/delete', {
        id: customer.id,
        manager: loginStore.manager,
        username: customer.username,
      });
      if (response.status === 200) {
        customers.value = customers.value.filter(c => c.username !== customer.username);
        ElMessage.success(response.data.message);
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败：', error);
      ElMessage.error('删除用户失败');
    }
  }
};

const searchCustomer = () => {
  currentPage.value = 1; // 重置页码
  fetchCustomers();
};

const resetSearch = () => {
  searchUser.value = '';
  currentPage.value = 1;
  fetchCustomers();
};
</script>

<style scoped>
.user-list-container {
  display: flex;
  flex-direction: column; 
  align-items: flex-start; 
  width: 100%;
}

.user-list {
  width: 100%;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.search-box {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.search-input {
  width: 200px;
  margin-right: 10px;
}
</style>
