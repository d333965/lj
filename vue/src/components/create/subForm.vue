<template>
    <el-form ref="form" :model="subForm" :rules="rules" size="large" class="center-form" style="width: 100%;">
      <el-form-item label="账号" prop="username" style="margin-top: 10px;">
        <el-input v-model="subForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="subForm.password"></el-input>
      </el-form-item>

      <el-form-item label="学校" prop="schoolName">
        <el-select v-model="subForm.schoolName" placeholder="请选择">
          <el-option label="川农成都" value="川农成都"></el-option>
          <el-option label="川农雅安" value="川农雅安"></el-option>
          <el-option label="川农都江堰" value="川农都江堰"></el-option>
          <el-option label="川农雅安老校区" value="川农雅安老校区"></el-option>
          <el-option label="西油成都" value="西油成都"></el-option>
          <el-option label="西油南充" value="西油南充"></el-option>
          <el-option label="电子科大清水河" value="电子科大清水河"></el-option>
          <el-option label="电子科大沙河" value="电子科大沙河"></el-option>
          <el-option label="电子科大成都学院" value="电子科大成都学院"></el-option>
          <el-option label="重庆交通" value="重庆交通"></el-option>
          <el-option label="轻化工李白河" value="轻化工李白河"></el-option>
          <el-option label="轻化工汇南" value="轻化工汇南"></el-option>
          <el-option label="轻化工宜宾" value="轻化工宜宾"></el-option>
          <el-option label="中飞院本校" value="中飞院本校"></el-option>
          <el-option label="中飞院天府" value="中飞院天府"></el-option>
          <el-option label="四川卫康" value="四川卫康"></el-option>
          <el-option label="成都大学" value="成都大学"></el-option>
          <el-option label="川北医学院" value="川北医学院"></el-option>
          <el-option label="攀枝花学院" value="攀枝花学院"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="跑步类型" prop="runType">
        <el-select v-model="subForm.runType" placeholder="请选择">
          <el-option label="范围跑" value="范围跑"></el-option>
          <el-option label="自由跑" value="自由跑"></el-option>
          <el-option label="定点跑" value="定点跑"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="跑步时间" prop="runTime">
        <el-select v-model="subForm.runTime" placeholder="请选择">
          <el-option label="8点~12点" value="8~12"></el-option>
          <el-option label="13点~18点" value="13~18"></el-option>
          <el-option label="19点~21点" value="19~21"></el-option>
          <el-option label="22点~24点" value="22~24"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="总km数" prop="total_goals">
        <el-input v-model="subForm.total_goals"></el-input>
      </el-form-item>
      <el-form-item label="每天km" prop="day_goals">
        <el-input v-model="subForm.day_goals"></el-input>
      </el-form-item>
      <el-form-item label="每周几天" prop="day_in_week">
        <el-input v-model="subForm.day_in_week"></el-input>
      </el-form-item>
      <el-form-item label="跑步圈数" prop="rounds">
        <el-input v-model="subForm.rounds"></el-input>
      </el-form-item>
      <el-form-item class="center-button">
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </el-form-item>
    </el-form>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useLoginStore } from '@/stores/useLoginStore'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
const loginStore = useLoginStore()

const subForm = reactive({
    manager: loginStore.manager,
    username: '',
    password: '',
    runType: '范围跑', // 设置默认值为范围跑
    schoolName: '',
    runTime: '19~21',
    total_goals: '',
    day_goals: '',
    day_in_week: '',
    rounds: '6'
});

// 还原
const resetForm = () => {
    subForm.username = '';
    subForm.password = '';
    subForm.runType = '范围跑';
    subForm.schoolName = '';
    subForm.runTime = '19~21';
    subForm.total_goals = '';
    subForm.day_goals = '';
    subForm.day_in_week = '';
    subForm.rounds = '6';
}

const rules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    runType: [{ required: true, message: '请选择跑步类型', trigger: 'change' }],
    schoolName: [{ required: true, message: '请选择学校', trigger: 'change' }],
    runTime: [{ required: true, message: '请选择跑步时间', trigger: 'change' }],
    total_goals: [{ required: true, message: '请输入总km', trigger: 'blur' }],
    day_goals: [{ required: true, message: '请输入每天km', trigger: 'blur' }],
    day_in_week: [{ required: true, message: '请输入每周几天', trigger: 'blur' }],
    rounds: [{ required: true, message: '请输入跑步圈数', trigger: 'blur' }]
};

const form = ref(null);

const handleSubmit = () => {
    form.value.validate((valid) => {
        if (valid) {
            console.log(subForm);
            axios.post('/api/legymCustomer/create', {
                manager: String(subForm.manager),
                username: String(subForm.username),
                password: String(subForm.password),
                runType: String(subForm.runType),
                schoolName: String(subForm.schoolName),
                runTime: String(subForm.runTime),
                total_goals: parseFloat(subForm.total_goals),
                day_goals: parseFloat(subForm.day_goals),
                day_in_week: parseInt(subForm.day_in_week),
                rounds: parseInt(subForm.rounds)
            }).then(response => {
                console.log(response.data);
                ElMessage.success(response.data.message);
                resetForm()
            }).catch(error => {
                // 弹出提示框,账号密码错误是否重新创建
                ElMessageBox.confirm(error.response.data.message, '提示', {
                    confirmButtonText: '清空',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    resetForm()
                }).catch(() => {
                    ElMessage.info('取消清空');
                });
            });
        } else {
            console.log('表单验证失败');
            return false;
        }
    });
};
</script>

<style scoped>
.center-form {
    position: relative;
}

.center-button {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
</style>

