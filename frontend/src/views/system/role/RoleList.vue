<template>
  <div class="crud-page">
    <div class="toolbar"><el-button type="primary" size="small" @click="openEdit()">新增角色</el-button></div>
    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="name" label="角色名称" width="150" />
      <el-table-column prop="code" label="角色标识" width="150" />
      <el-table-column prop="sort" label="排序" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{row}">
          <el-tag :type="row.status?'success':'danger'" size="small">{{ row.status?'正常':'停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{row}">
          <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../../utils/request.js'

const list = ref([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await request.get('/system/roles')
    list.value = res.data.data.list
  } finally { loading.value = false }
}
function openEdit(row) { ElMessage.info(row ? '编辑功能开发中' : '新增功能开发中') }
async function handleDelete(row) { ElMessage.info('删除功能开发中') }
onMounted(loadData)
</script>

<style scoped>
.crud-page { padding: 4px; }
.toolbar { display:flex; margin-bottom:8px; }
:deep(.el-table) { background: transparent; --el-table-border-color: rgba(0,212,255,.06); }
:deep(.el-table tr) { background: transparent; }
</style>
