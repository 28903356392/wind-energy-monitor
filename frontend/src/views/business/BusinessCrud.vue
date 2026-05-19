<template>
  <div class="crud-page">
    <div class="toolbar">
      <el-button type="primary" size="small" @click="openDialog()">新增</el-button>
      <el-input v-if="searchable" v-model="keyword" placeholder="搜索..." size="small" style="width:200px;margin-left:auto"
        clearable @keyup.enter="loadData" @clear="loadData" />
    </div>

    <el-table :data="list" size="small" v-loading="loading" style="width:100%"
      :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
      :cell-style="{ background:'transparent',color:'#e0e6ed' }">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column v-for="col in columns" :key="col.prop" :prop="col.prop" :label="col.label" :width="col.width"
        :formatter="col.formatter" :min-width="col.minWidth" show-overflow-tooltip />
      <el-table-column label="操作" :width="actionWidth" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button v-if="showDetail" link type="info" size="small" @click="$emit('detail', row)">详情</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination background layout="prev,pager,next" :total="total" :page-size="pageSize" small
        @current-change="(p)=>{ page=p;loadData() }" />
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑' : '新增'" width="600px" :close-on-click-modal="false"
      @closed="resetForm">
      <el-form :model="form" label-width="100px" size="small" ref="formRef">
        <el-form-item v-for="field in formFields" :key="field.prop" :label="field.label"
          :prop="field.prop" :rules="field.rules || []">
          <!-- 输入框 -->
          <el-input v-if="field.type === 'input' || !field.type" v-model="form[field.prop]" :placeholder="field.placeholder || ''" />
          <!-- 下拉选择 -->
          <el-select v-else-if="field.type === 'select'" v-model="form[field.prop]" placeholder="请选择" style="width:100%">
            <el-option v-for="opt in field.options || []" :key="opt.value" :label="opt.label" :value="opt.value" />
          </el-select>
          <!-- 数字输入 -->
          <el-input-number v-else-if="field.type === 'number'" v-model="form[field.prop]" :min="field.min || 0" style="width:100%" />
          <!-- 开关 -->
          <el-switch v-else-if="field.type === 'switch'" v-model="form[field.prop]" />
          <!-- 文本域 -->
          <el-input v-else-if="field.type === 'textarea'" v-model="form[field.prop]" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button size="small" @click="dialogVisible = false">取消</el-button>
        <el-button size="small" type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
export interface CrudColumn {
  prop: string
  label: string
  width?: string | number
  minWidth?: string | number
  formatter?: (row: any, column: any, value: any, index: number) => string
}

export interface CrudField {
  prop: string
  label: string
  type?: 'input' | 'select' | 'number' | 'switch' | 'textarea'
  placeholder?: string
  options?: { label: string; value: any }[]
  rules?: any[]
  min?: number
}
</script>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = withDefaults(defineProps<{
  api: any
  columns: CrudColumn[]
  formFields: CrudField[]
  searchable?: boolean
  pageSize?: number
  showDetail?: boolean
  actionWidth?: string | number
  defaultForm?: Record<string, any>
  filterParams?: Record<string, any>
}>(), {
  searchable: true,
  pageSize: 20,
  showDetail: false,
  actionWidth: 150,
  defaultForm: () => ({}),
  filterParams: () => ({}),
})

const emit = defineEmits<{
  detail: [row: any]
  saved: []
}>()

const list = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const keyword = ref('')
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const form = ref<Record<string, any>>({})
const formRef = ref<any>(null)

function resetForm() {
  form.value = { ...props.defaultForm }
  isEdit.value = false
  editId.value = 0
}

async function loadData() {
  loading.value = true
  try {
    const res = await props.api.list({
      page: page.value,
      size: props.pageSize,
      keyword: keyword.value,
      ...props.filterParams,
    })
    list.value = res.list
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function openDialog(row?: any) {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.value = { ...row }
  } else {
    resetForm()
  }
  dialogVisible.value = true
}

async function handleSave() {
  try {
    if (isEdit.value) {
      await props.api.update(editId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await props.api.create(form.value)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    emit('saved')
    loadData()
  } catch { /* ignore */ }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm('确认删除该记录？', '提示')
    await props.api.del(row.id)
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
:deep(.el-dialog) { background: #1d1d1d; border: 1px solid #3d3d3d; }
:deep(.el-dialog__title) { color: #e0e0e0; }
</style>
