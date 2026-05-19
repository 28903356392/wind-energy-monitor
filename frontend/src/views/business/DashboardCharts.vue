<template>
  <div class="dashboard-page">
    <!-- KPI 卡片 -->
    <div class="kpi-row">
      <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card" :style="{ borderTopColor: kpi.color }">
        <div class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</div>
        <div class="kpi-label">{{ kpi.label }}</div>
        <div v-if="kpi.sub" class="kpi-sub">{{ kpi.sub }}</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-row">
      <div v-for="(chart, i) in charts" :key="i" class="chart-card">
        <div class="chart-title">{{ chart.title }}</div>
        <div :id="'chart-' + i" class="chart-container" ref="chartRefs"></div>
      </div>
    </div>

    <!-- 详情表格 -->
    <div class="table-section">
      <div class="toolbar">
        <span class="section-title">{{ detailTitle }}</span>
        <el-button size="small" text @click="$emit('viewAll')">查看全部 &gt;</el-button>
      </div>
      <el-table :data="tableData" size="small" style="width:100%"
        :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
        :cell-style="{ background:'transparent',color:'#e0e6ed' }">
        <el-table-column v-for="col in tableColumns" :key="col.prop" :prop="col.prop" :label="col.label" :width="col.width" show-overflow-tooltip />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

const props = defineProps<{
  kpis: { label: string; value: string; sub?: string; color: string }[]
  charts: { title: string; option: any }[]
  detailTitle: string
  tableColumns: { prop: string; label: string; width?: number }[]
  tableData: any[]
}>()

defineEmits<{ viewAll: [] }>()
const chartRefs = ref<any[]>([])

onMounted(() => {
  nextTick(() => {
    // 动态加载 echarts
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/echarts@5/dist/echarts.min.js'
    script.onload = () => {
      const echarts = (window as any).echarts
      props.charts.forEach((chart, i) => {
        const el = document.getElementById('chart-' + i)
        if (el && echarts) {
          const instance = echarts.init(el, 'dark')
          instance.setOption(chart.option)
        }
      })
    }
    document.head.appendChild(script)
  })
})
</script>

<style scoped>
.dashboard-page { padding: 4px; }
.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 16px; }
.kpi-card {
  background: rgba(255,255,255,.03); border-radius: 8px;
  padding: 16px; border-top: 3px solid;
  border: 1px solid rgba(0,212,255,.08);
  border-top-width: 3px;
}
.kpi-value { font-size: 28px; font-weight: 700; }
.kpi-label { font-size: 13px; color: #a3b1cc; margin-top: 4px; }
.kpi-sub { font-size: 12px; color: #6a7a9a; margin-top: 2px; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.chart-card {
  background: rgba(255,255,255,.03); border-radius: 8px;
  padding: 12px; border: 1px solid rgba(0,212,255,.08);
}
.chart-title { font-size: 14px; font-weight: 600; color: #e0e6ed; margin-bottom: 8px; }
.chart-container { height: 280px; }
.table-section {
  background: rgba(255,255,255,.03); border-radius: 8px;
  padding: 12px; border: 1px solid rgba(0,212,255,.08);
}
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.section-title { font-size: 14px; font-weight: 600; color: #e0e6ed; }
@media (max-width: 900px) { .charts-row { grid-template-columns: 1fr; } }
</style>
