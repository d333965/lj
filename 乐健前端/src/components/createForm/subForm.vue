<template>
    <el-form ref="form" :model="subForm" :rules="rules" size="large" class="center-form" style="width: 100%;" v-loading="loading" element-loading-text="正在提交..." element-loading-spinner="el-icon-loading" element-loading-background="rgba(255, 255, 255, 0.8)" element-loading-svg-view-box="-10, -10, 50, 50" element-loading-custom-class="custom-loading">
      <el-form-item label="账号" prop="username" style="margin-top: 10px;">
        <el-input v-model="subForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="subForm.password"></el-input>
      </el-form-item>

      <el-form-item label="学校" prop="schoolName">
        <el-select v-model="subForm.schoolName" placeholder="请选择">
          <el-option label="川农成都" value="川农成都" @click="subForm.day_goals='5',subForm.day_in_week='7'"></el-option>
          <el-option label="川农雅安" value="川农雅安" @click="subForm.day_goals='5',subForm.day_in_week='7'"></el-option>
          <el-option label="川农都江堰" value="川农都江堰" @click="subForm.day_goals='5',subForm.day_in_week='7'"></el-option>
          <el-option label="川农雅安老校区" value="川农雅安老校区" @click="subForm.day_goals='5',subForm.day_in_week='7'"></el-option>
          <el-option label="西油成都" value="西油成都"@click="subForm.runType = '自由跑',subForm.day_goals='2.4',subForm.day_in_week='6'"></el-option>
          <el-option label="西油南充" value="西油南充" @click="subForm.runType = '定点跑',subForm.rounds = '1',subForm.day_goals='3',subForm.day_in_week='5'"></el-option>
          <el-option label="电子科大清水河" value="电子科大清水河" @click="subForm.day_goals='3.5',subForm.day_in_week='7'"></el-option>
          <el-option label="电子科大沙河" value="电子科大沙河" @click="subForm.day_goals='3.5',subForm.day_in_week='7'"></el-option>
          <el-option label="电子科大成都学院" value="电子科大成都学院"></el-option>
          <el-option label="重庆交通" value="重庆交通"></el-option>  
          <el-option label="轻化工李白河" value="轻化工李白河" @click="subForm.day_goals='4',subForm.day_in_week='7'"></el-option>
          <el-option label="轻化工汇南" value="轻化工汇南" @click="subForm.day_goals='4',subForm.day_in_week='7'"></el-option>
          <el-option label="轻化工宜宾" value="轻化工宜宾" @click="subForm.day_goals='4',subForm.day_in_week='7'"></el-option>
          <el-option label="中飞院本校" value="中飞院本校" @click="subForm.runType = '定点跑',subForm.rounds = '1',subForm.day_goals='3',subForm.day_in_week='2'"></el-option>
          <el-option label="中飞院天府" value="中飞院天府" @click="subForm.day_goals='3',subForm.day_in_week='2'"></el-option>
          <el-option label="四川卫康" value="四川卫康" @click="subForm.runType = '范围跑',subForm.day_goals='4',subForm.day_in_week='4',subForm.runTime='21~24'"></el-option>
          <el-option label="成都大学" value="成都大学" @click="subForm.runType = '定点跑',subForm.rounds = '1',subForm.day_goals='2.5',subForm.day_in_week='7'"></el-option>
          <el-option label="川北医学院" value="川北医学院" @click="subForm.day_goals='5',subForm.day_in_week='5',subForm.runTime='21~24'"></el-option>
          <el-option label="攀枝花学院" value="攀枝花学院" @click="subForm.day_goals='3',subForm.day_in_week='7'"></el-option>
          <el-option label="攀枝花西苑" value="攀枝花西苑" @click="subForm.day_goals='3',subForm.day_in_week='7'"></el-option>
          <el-option label="西南交通九里" value="西南交通九里"></el-option>
          <el-option label="西南交通犀浦" value="西南交通犀浦"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="跑步类型" prop="runType">
        <el-select v-model="subForm.runType" placeholder="请选择">
          <el-option label="范围跑" value="范围跑"></el-option>
          <el-option label="自由跑" value="自由跑"></el-option>
          <el-option label="定点跑" value="定点跑"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="跑步时间" prop="runTime" v-show="!subForm.coverRun">
        <el-select v-model="subForm.runTime" placeholder="请选择">
          <el-option label="8点~12点" value="8~12"></el-option>
          <el-option label="13点~18点" value="13~18"></el-option>
          <el-option label="19点~21点" value="19~21"></el-option>
          <el-option label="21点~24点" value="21~24"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="总km数" prop="total_goals" v-show="!subForm.coverRun">
        <el-input v-model="subForm.total_goals"></el-input>
      </el-form-item>
      <el-form-item label="每天km" prop="day_goals">
        <el-input v-model="subForm.day_goals"></el-input>
      </el-form-item>
      <el-form-item label="每周几天" prop="day_in_week" v-show="!subForm.coverRun">
        <el-input v-model="subForm.day_in_week"></el-input>
      </el-form-item>
      <el-form-item label="跑步圈数" prop="rounds">
        <el-input v-model="subForm.rounds"></el-input>
      </el-form-item>
      <el-form-item label="是否补跑" prop="coverRun" style="margin: -10px 0 10px 10px;" @click="subForm.total_goals = 0">
        <el-switch v-model="subForm.coverRun"></el-switch>
        <el-check-tag v-show="subForm.coverRun" :checked="subForm.day1" type="success" @change="onChange1" style="margin: 0 5px 0 10px;">
      昨天
    </el-check-tag>
    <el-check-tag v-show="subForm.coverRun" :checked="subForm.day2" type="success" @change="onChange2">
      前天
    </el-check-tag>
     <span v-show="subForm.coverRun" style="color:gray;margin-left: 10px;">(点击选择)</span>
      </el-form-item>      
      <el-form-item class="center-button">
        <el-button type="primary" :loading="loading" @click="handleSubmit">提交</el-button>
      </el-form-item>
    </el-form>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useLoginStore } from '@/stores/useLoginStore'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
const loginStore = useLoginStore()



const onChange1 = () => {
  subForm.day1 = !subForm.day1
}

const onChange2 = () => {
  subForm.day2 = !subForm.day2
}

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
    rounds: '6',
    coverRun:false,
    day1:false,
    day2:false
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
    subForm.coverRun=false,
    subForm.day1=false,
    subForm.day2=false
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

const loading = ref(false);

const handleSubmit = () => {
    if (loading.value) return; // 如果正在提交中，直接返回
    loading.value = true; // 开始提交时设置 loading

    form.value.validate((valid) => {
        if (valid) {
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
                rounds: parseInt(subForm.rounds),
                coverRun: Boolean(subForm.coverRun),
                day1: Boolean(subForm.day1),
                day2: Boolean(subForm.day2),
            }).then(response => {
                ElMessage.success({
                    message: response.data.message,
                    duration: 1000
                });
                resetForm();
            }).catch(error => {
                ElMessageBox.confirm(error.response.data.message, '提示', {
                    confirmButtonText: '清空',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    resetForm();
                }).catch(() => {
                    ElMessage.info({
                        message: '取消清空',
                        duration: 1000
                    });
                });
            }).finally(() => {
                loading.value = false; // 无论成功还是失败，都需要关闭 loading
            });
        } else {
            console.log('表单验证失败');
            loading.value = false; // 验证失败时也要关闭 loading
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

:deep(.custom-loading) {
  .el-loading-text {
    color: #409EFF;
    font-size: 16px;
  }
}
</style>

