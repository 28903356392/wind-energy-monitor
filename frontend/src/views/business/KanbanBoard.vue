<template>
  <div class="kanban-page">
    <div class="toolbar">
      <el-button type="primary" size="small" @click="$emit('add')">新增</el-button>
      <el-input v-model="searchKeyword" placeholder="搜索..." size="small" style="width:200px;margin-left:auto" clearable />
    </div>
    <div class="kanban-columns">
      <div v-for="col in columns" :key="col.status" class="kanban-col">
        <div class="col-header">
          <span class="col-title">{{ col.label }}</span>
          <el-tag size="small" :type="col.tag">{{ grouped[col.status]?.length || 0 }}</el-tag>
        </div>
        <div class="col-body" @dragover.prevent @drop="onDrop($event, col.status)">
          <div v-for="card in grouped[col.status] || []" :key="card.id" class="kanban-card"
            draggable="true" @dragstart="onDragStart($event, card, col.status)"
            @dblclick="$emit('edit', card)">
            <div class="card-title">{{ card.title || card.name }}</div>
            <div class="card-meta">
              <span v-if="card.priority" class="priority-tag" :class="'p-'+card.priority">
                {{ priorityMap[card.priority] || card.priority }}
              </span>
              <span v-if="card.assignee" class="assignee">{{ card.assignee }}</span>
            </div>
            <div v-if="card.progress !== undefined" class="progress-bar">
              <el-progress :percentage="card.progress" size="small" :stroke-width="4" />
            </div>
            <div class="card-footer">
              <span v-if="card.deadline" class="deadline">截止: {{ card.deadline }}</span>
              <span v-if="card.turbine_name" class="turbine">{{ card.turbine_name }}</span>
            </div>
          </div>
          <el-empty v-if="!grouped[col.status]?.length" description="暂无" :image-size="60" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = withDefaults(defineProps<{
  data: any[]
  columns: { status: string; label: string; tag: string }[]
  statusField?: string
}>(), { statusField: 'status' })

defineEmits<{ add: []; edit: [row: any] }>()

const priorityMap: Record<string, string> = { low: '低', medium: '中', high: '高', urgent: '紧急' }
const searchKeyword = ref('')
const draggedItem = ref<any>(null)
const draggedFrom = ref('')

const grouped = computed(() => {
  const groups: Record<string, any[]> = {}
  props.columns.forEach(c => { groups[c.status] = [] })
  const kw = searchKeyword.value.toLowerCase()
  props.data.forEach(item => {
    if (kw && !JSON.stringify(item).toLowerCase().includes(kw)) return
    const st = item[props.statusField] || 'pending'
    if (groups[st]) groups[st].push(item)
  })
  return groups
})

function onDragStart(e: DragEvent, item: any, from: string) {
  draggedItem.value = item; draggedFrom.value = from
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

function onDrop(e: DragEvent, toStatus: string) {
  if (draggedItem.value && toStatus !== draggedFrom.value) {
    // 触发父组件更新状态
    window.dispatchEvent(new CustomEvent('kanban-move', {
      detail: { item: draggedItem.value, from: draggedFrom.value, to: toStatus }
    }))
  }
  draggedItem.value = null
}
</script>

<style scoped>
.kanban-page { padding: 4px; }
.toolbar { display: flex; align-items: center; margin-bottom: 12px; gap: 8px; }
.kanban-columns { display: flex; gap: 12px; overflow-x: auto; min-height: 70vh; }
.kanban-col {
  flex: 1; min-width: 220px;
  background: rgba(255,255,255,.03);
  border-radius: 8px;
  border: 1px solid rgba(0,212,255,.08);
}
.col-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid rgba(0,212,255,.08);
}
.col-title { font-size: 14px; font-weight: 600; color: #e0e6ed; }
.col-body { padding: 8px; min-height: 200px; }
.kanban-card {
  background: rgba(255,255,255,.06);
  border-radius: 6px;
  padding: 10px;
  margin-bottom: 8px;
  cursor: grab; transition: background .15s;
  border-left: 3px solid transparent;
}
.kanban-card:hover { background: rgba(255,255,255,.1); }
.kanban-card:active { cursor: grabbing; }
.card-title { font-size: 13px; font-weight: 500; color: #fff; margin-bottom: 6px; }
.card-meta { display: flex; gap: 6px; align-items: center; margin-bottom: 4px; }
.priority-tag { font-size: 11px; padding: 1px 6px; border-radius: 3px; }
.p-low { background: rgba(0,200,83,.15); color: #00c853; }
.p-medium { background: rgba(255,193,7,.15); color: #ffc107; }
.p-high { background: rgba(255,152,0,.15); color: #ff9800; }
.p-urgent { background: rgba(244,67,54,.15); color: #f44336; }
.assignee { font-size: 11px; color: #a3b1cc; }
.progress-bar { margin-bottom: 4px; }
.card-footer { display: flex; justify-content: space-between; font-size: 11px; color: #7a8ba8; }
:deep(.el-empty__description p) { color: #5a6a8a; }
</style>
