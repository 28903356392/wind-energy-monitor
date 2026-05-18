<template>
  <div class="crud-page">
    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column label="结果" width="80">
        <template #default="{row}"><el-tag :type="row.status==='success'?'success':'danger'" size="small">{{ row.status }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="ip" label="IP地址" width="140" />
      <el-table-column prop="message" label="消息" />
      <el-table-column prop="created_at" label="登录时间" width="180" />
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request.js'
const list = ref([]), loading = ref(false)
async function loadData() {
  loading.value = true
  try { const res = await request.get('/system/logs/login'); list.value = res.data.data.list }
  finally { loading.value = false }
}
onMounted(loadData)
</script>
<style scoped>
.crud-page { padding:4px; }
:deep(.el-table) { background:transparent; --el-table-border-color:rgba(0,212,255,.06); }
:deep(.el-table tr) { background:transparent; }
</style>
