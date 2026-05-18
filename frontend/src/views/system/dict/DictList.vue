<template>
  <div class="crud-page">
    <div class="toolbar"><el-button type="primary" size="small">新增字典</el-button></div>
    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="name" label="字典名称" width="150" />
      <el-table-column prop="code" label="字典标识" width="150" />
      <el-table-column label="状态" width="80">
        <template #default="{row}"><el-tag :type="row.status?'success':'danger'" size="small">{{ row.status?'正常':'停用' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../../../utils/request.js'
const list = ref([]), loading = ref(false)
async function loadData() {
  loading.value = true
  try { const res = await request.get('/system/dict/types'); list.value = res.data.data.list }
  finally { loading.value = false }
}
onMounted(loadData)
</script>
<style scoped>
.crud-page { padding:4px; }
.toolbar { display:flex; margin-bottom:8px; }
:deep(.el-table) { background:transparent; --el-table-border-color:rgba(0,212,255,.06); }
:deep(.el-table tr) { background:transparent; }
</style>
