<template>
  <div class="crud-page">
    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="username" label="操作人" width="100" />
      <el-table-column prop="module" label="模块" width="100" />
      <el-table-column prop="action" label="操作类型" width="100" />
      <el-table-column prop="method" label="请求方式" width="80" />
      <el-table-column prop="url" label="请求地址" width="200" />
      <el-table-column prop="ip" label="IP" width="130" />
      <el-table-column label="结果" width="70">
        <template #default="{row}"><el-tag :type="row.result==='success'?'success':'danger'" size="small">{{ row.result }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="cost_time" label="耗时(ms)" width="90" />
      <el-table-column prop="created_at" label="操作时间" width="180" />
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request.js'
const list = ref([]), loading = ref(false)
async function loadData() {
  loading.value = true
  try { const res = await request.get('/system/logs/operation'); list.value = res.data.data.list }
  finally { loading.value = false }
}
onMounted(loadData)
</script>
<style scoped>
.crud-page { padding:4px; }
:deep(.el-table) { background:transparent; --el-table-border-color:rgba(0,212,255,.06); }
:deep(.el-table tr) { background:transparent; }
</style>
