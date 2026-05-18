<template>
  <div class="crud-page">
    <div class="toolbar">
      <el-button type="primary" size="small" @click="openEdit()">新增用户</el-button>
      <el-input v-model="keyword" placeholder="搜索用户名" size="small" style="width:200px;margin-left:auto" @keyup.enter="loadData" />
    </div>
    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column label="状态" width="80">
        <template #default="{row}">
          <el-tag :type="row.status?'success':'danger'" size="small">{{ row.status?'正常':'停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{row}">
          <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination background layout="prev,pager,next" :total="total" :page-size="20" small
        @current-change="(p)=> { page=p;loadData() }" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../../utils/request.js'

const list = ref([])
const total = ref(0)
const page = ref(1)
const keyword = ref('')
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await request.get('/system/users', { params: { page: page.value, size: 20, keyword: keyword.value } })
    list.value = res.data.data.list
    total.value = res.data.data.total
  } finally { loading.value = false }
}

function openEdit(row) {
  ElMessage.info(row ? '编辑功能开发中' : '新增功能开发中')
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确认删除用户 ' + row.username + ' ？', '提示')
    await request.delete('/system/users/' + row.id)
    ElMessage.success('已删除')
    loadData()
  } catch { /* ignore */ }
}

onMounted(loadData)
</script>

<style scoped>
.crud-page { padding: 4px; }
.toolbar { display:flex; align-items:center; margin-bottom:8px; gap:8px; }
.pagination { margin-top:12px; display:flex; justify-content:center; }
:deep(.el-table) { background: transparent; --el-table-border-color: rgba(0,212,255,.06); }
:deep(.el-table tr) { background: transparent; }
</style>
