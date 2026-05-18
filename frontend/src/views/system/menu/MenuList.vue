<template>
  <div class="crud-page">
    <div class="toolbar"><el-button type="primary" size="small" @click="openEdit()">新增菜单</el-button></div>
    <el-table :data="tree" size="small" v-loading="loading" row-key="id" default-expand-all style="width:100%"
      :tree-props="{ children: 'children' }"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column prop="name" label="菜单名称" width="180" />
      <el-table-column prop="icon" label="图标" width="80" />
      <el-table-column prop="path" label="路由地址" width="180" />
      <el-table-column prop="permission" label="权限标识" width="180" />
      <el-table-column prop="sort" label="排序" width="60" />
      <el-table-column label="类型" width="80">
        <template #default="{row}">
          <el-tag size="small">{{ {directory:'目录',menu:'菜单',button:'按钮'}[row.type]||row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{row}">
          <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../../utils/request.js'

const tree = ref([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await request.get('/system/menus')
    tree.value = res.data.data
  } finally { loading.value = false }
}
function openEdit(row) { ElMessage.info(row ? '编辑功能开发中' : '新增功能开发中') }
onMounted(loadData)
</script>

<style scoped>
.crud-page { padding: 4px; }
.toolbar { display:flex; margin-bottom:8px; }
:deep(.el-table) { background: transparent; --el-table-border-color: rgba(0,212,255,.06); }
:deep(.el-table tr) { background: transparent; }
</style>
