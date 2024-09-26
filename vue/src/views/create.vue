<template>
    <div class="container">
        <subForm />
    </div>
</template>

<script setup>
import subForm from '@/components/create/subForm.vue';
</script>

<style scoped>
.container {
    display: flex;
    height: 100%; /* 使容器占满整个视口高度 */
    width: 50vh; /* 调整容器的宽度 */
    margin: 0 auto; /* 使容器居中 */
}
</style>
