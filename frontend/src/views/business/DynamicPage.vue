<template>
  <div>
    <div class="page-header">
      <h3>{{ config?.title || '加载中...' }}</h3>
    </div>

    <!-- 关键：每个子组件加 :key="resource"，切换菜单时强制重建，防止数据窜页 -->
    <BusinessCrud v-if="config && pageType === 'table'"
      :key="'t-' + resource"
      :api="config.api" :columns="config.columns" :form-fields="config.formFields"
      :searchable="config.searchable !== false" :default-form="defaultForm" />

    <KanbanBoard v-else-if="config && pageType === 'kanban'"
      :key="'k-' + resource" :data="listData"
      :columns="kanbanColumns" @add="openCrudDialog()" @edit="openCrudDialog($event)" />

    <DashboardCharts v-else-if="config && pageType === 'dashboard'"
      :key="'d-' + resource"
      :kpis="dashboardKpis" :charts="dashboardCharts"
      :detail-title="config.title + '明细'" :table-columns="config.columns"
      :table-data="listData" />

    <el-empty v-else description="未知模块" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import BusinessCrud from './BusinessCrud.vue'
import KanbanBoard from './KanbanBoard.vue'
import DashboardCharts from './DashboardCharts.vue'
import { PAGE_CONFIGS } from './pageConfigs'
import { getPageType, getKanbanColumns } from '../../config/pageConfig'
import * as api from '../../api/business'

const route = useRoute()
const resource = computed(() => route.params.resource as string)
const config = computed(() => PAGE_CONFIGS[resource.value])
const listData = ref<any[]>([])
const loading = ref(false)

const pageType = computed(() => getPageType(resource.value))
const kanbanColumns = computed<any[]>(() => getKanbanColumns(resource.value))

// 仪表盘 KPI 数据
const dashboardKpis = computed(() => {
  if (resource.value === 'power-targets') {
    const items = listData.value
    const totalTarget = items.reduce((s, i) => s + (i.target_kwh || 0), 0)
    const totalActual = items.reduce((s, i) => s + (i.actual_kwh || 0), 0)
    const rate = totalTarget ? (totalActual / totalTarget * 100).toFixed(1) : '0'
    return [
      { label: '总目标电量', value: totalTarget.toLocaleString() + ' kWh', color: '#6190e8' },
      { label: '总实际电量', value: totalActual.toLocaleString() + ' kWh', color: '#49cc90' },
      { label: '综合完成率', value: rate + '%', sub: totalTarget > totalActual ? '未达标' : '超额完成', color: parseFloat(rate) >= 100 ? '#49cc90' : '#fca130' },
      { label: '统计月份', value: items.length + ' 个月', color: '#a3b1cc' },
    ]
  }
  if (resource.value === 'revenue-items') {
    const total = listData.value.reduce((s, i) => s + (i.total_revenue || 0), 0)
    const energy = listData.value.reduce((s, i) => s + (i.energy_revenue || 0), 0)
    const carbon = listData.value.reduce((s, i) => s + (i.carbon_revenue || 0), 0)
    return [
      { label: '总收入', value: '¥' + total.toLocaleString(), color: '#49cc90' },
      { label: '电费收入', value: '¥' + energy.toLocaleString(), color: '#6190e8' },
      { label: '碳交易收入', value: '¥' + carbon.toLocaleString(), color: '#fca130' },
      { label: '数据月份', value: listData.value.length + ' 个月', color: '#a3b1cc' },
    ]
  }
  if (resource.value === 'carbon-reductions') {
    const co2 = listData.value.reduce((s, i) => s + (i.reduction_co2 || 0), 0)
    const coal = listData.value.reduce((s, i) => s + (i.standard_coal_saved || 0), 0)
    const trees = listData.value.reduce((s, i) => s + (i.trees_equivalent || 0), 0)
    return [
      { label: 'CO₂减排', value: co2.toLocaleString() + ' kg', color: '#49cc90' },
      { label: '节约标准煤', value: coal.toLocaleString() + ' kg', color: '#6190e8' },
      { label: '等效植树', value: Math.round(trees).toLocaleString() + ' 棵', color: '#fca130' },
      { label: '数据月份', value: listData.value.length + ' 个月', color: '#a3b1cc' },
    ]
  }
  return []
})

// 仪表盘图表配置
const dashboardCharts = computed<any[]>(() => {
  const items = [...listData.value].reverse()
  const months = items.map(i => `${i.year}-${String(i.month).padStart(2, '0')}`)
  
  if (resource.value === 'power-targets') {
    return [{
      title: '目标 vs 实际电量',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['目标电量', '实际电量'], textStyle: { color: '#a3b1cc' } },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', axisLabel: { color: '#a3b1cc' } },
        series: [
          { name: '目标电量', type: 'bar', data: items.map(i => i.target_kwh), itemStyle: { color: '#6190e8' } },
          { name: '实际电量', type: 'bar', data: items.map(i => i.actual_kwh), itemStyle: { color: '#49cc90' } },
        ]
      }
    }, {
      title: '完成率趋势',
      option: {
        tooltip: { trigger: 'axis' },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', max: 150, axisLabel: { color: '#a3b1cc', formatter: '{value}%' } },
        series: [{
          type: 'line', data: items.map(i => (i.completion_rate * 100).toFixed(1)),
          lineStyle: { color: '#fca130', width: 3 },
          itemStyle: { color: '#fca130' },
          areaStyle: { color: 'rgba(252,161,48,0.1)' },
        }]
      }
    }]
  }
  if (resource.value === 'revenue-items') {
    return [{
      title: '收入构成',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['电费收入', '补贴收入', '碳交易收入', '其他收入'], textStyle: { color: '#a3b1cc' } },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', axisLabel: { color: '#a3b1cc' } },
        series: [
          { name: '电费收入', type: 'bar', stack: 'total', data: items.map(i => i.energy_revenue), itemStyle: { color: '#6190e8' } },
          { name: '补贴收入', type: 'bar', stack: 'total', data: items.map(i => i.subsidy_revenue), itemStyle: { color: '#49cc90' } },
          { name: '碳交易收入', type: 'bar', stack: 'total', data: items.map(i => i.carbon_revenue), itemStyle: { color: '#fca130' } },
        ]
      }
    }, {
      title: '总收入趋势',
      option: {
        tooltip: { trigger: 'axis' },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', axisLabel: { color: '#a3b1cc' } },
        series: [{
          type: 'line', data: items.map(i => i.total_revenue),
          lineStyle: { color: '#49cc90', width: 3 },
          itemStyle: { color: '#49cc90' },
          areaStyle: { color: 'rgba(73,204,144,0.1)' },
        }]
      }
    }]
  }
  if (resource.value === 'carbon-reductions') {
    return [{
      title: 'CO₂减排趋势',
      option: {
        tooltip: { trigger: 'axis' },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', axisLabel: { color: '#a3b1cc' } },
        series: [{
          type: 'bar', data: items.map(i => i.reduction_co2),
          itemStyle: { color: '#49cc90' },
        }]
      }
    }, {
      title: '节约资源对比',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['节约标准煤(kg)', '等效植树(棵)'], textStyle: { color: '#a3b1cc' } },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: { type: 'category', data: months, axisLabel: { color: '#a3b1cc' } },
        yAxis: { type: 'value', axisLabel: { color: '#a3b1cc' } },
        series: [
          { name: '节约标准煤(kg)', type: 'line', data: items.map(i => i.standard_coal_saved), itemStyle: { color: '#6190e8' } },
          { name: '等效植树(棵)', type: 'bar', data: items.map(i => i.trees_equivalent), itemStyle: { color: '#49cc90' } },
        ]
      }
    }]
  }
  return []
})

const defaultForm = computed(() => {
  if (!config.value) return {}
  const form: Record<string, any> = {}
  for (const field of config.value.formFields) {
    if (field.type === 'switch') form[field.prop] = true
    else if (field.type === 'number') form[field.prop] = 0
    else form[field.prop] = ''
  }
  return form
})

async function refreshData() {
  if (pageType.value === 'kanban' || pageType.value === 'dashboard') {
    await loadListData()
  }
}

async function loadListData() {
  loading.value = true
  try {
    const res = await config.value.api.list({ page: 1, size: 200 })
    listData.value = res.list
  } finally { loading.value = false }
}

function openCrudDialog(row?: any) {
  // 对于看板, 使用 Crud 对话框
  window.dispatchEvent(new CustomEvent('open-crud-dialog', { detail: { row, resource: resource.value } }))
}

onMounted(() => {
  if (pageType.value === 'kanban' || pageType.value === 'dashboard') {
    loadListData()
  }
})

watch(resource, () => {
  if (pageType.value === 'kanban' || pageType.value === 'dashboard') {
    loadListData()
  }
})
</script>

<style scoped>
.page-header h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #e0e6ed;
  padding: 4px 0;
  border-bottom: 1px solid rgba(0,212,255,.06);
}
</style>
