<template>
  <div class="wind-info">
    <div class="gauge-section">
      <div class="gauge-title">实时风速</div>
      <div ref="gaugeRef" class="gauge-chart"></div>
      <div class="gauge-value">
        <span class="gauge-num">{{ overview?.avg_wind_speed?.toFixed(1) ?? '--' }}</span>
        <span class="gauge-unit">m/s</span>
      </div>
    </div>

    <div class="stats-section">
      <div class="stat-row">
        <span class="stat-label">总发电量</span>
        <span class="stat-value">{{ formatEnergy(overview?.total_energy) }}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">日发电量</span>
        <span class="stat-value">{{ formatEnergy(overview?.total_daily_energy, 'kWh') }}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">运行风机</span>
        <span class="stat-value highlight">{{ overview?.running_count ?? 0 }}<small>/{{ overview?.turbine_count ?? 0 }}</small></span>
      </div>
      <div class="stat-row">
        <span class="stat-label">故障风机</span>
        <span class="stat-value" :class="(overview?.fault_count ?? 0) > 0 ? 'danger' : ''">{{ overview?.fault_count ?? 0 }}</span>
      </div>
    </div>

    <div class="ring-section">
      <div class="ring-title">风机状态占比</div>
      <div ref="ringRef" class="ring-chart"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'
import type { OverviewData } from '../types'

const props = defineProps<{
  overview: OverviewData | null
}>()

const gaugeRef = ref<HTMLDivElement | null>(null)
const ringRef = ref<HTMLDivElement | null>(null)
let gaugeChart: echarts.ECharts | null = null
let ringChart: echarts.ECharts | null = null
let gaugeObserver: ResizeObserver | null = null
let ringObserver: ResizeObserver | null = null

function formatEnergy(val: number | null | undefined, unit = 'MWh'): string {
  if (!val && val !== 0) return '--'
  if (val >= 1000000) return (val / 10000).toFixed(1) + '万' + unit
  if (val >= 1000) return (val / 1000).toFixed(1) + '千' + unit
  return val.toFixed(1) + ' ' + unit
}

// 仪表盘配置
const gaugeOption = computed<echarts.EChartsOption>(() => {
  const val = props.overview?.avg_wind_speed ?? 0
  return {
    series: [{
      type: 'gauge',
      startAngle: 200,
      endAngle: -20,
      min: 0, max: 20,
      center: ['50%', '60%'],
      radius: '90%',
      progress: {
        show: true,
        width: 8,
        itemStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 1, y2: 0,
            colorStops: [
              { offset: 0, color: '#00d4ff' },
              { offset: 0.5, color: '#00ff88' },
              { offset: 1, color: '#ffd93d' },
            ],
          },
        },
      },
      axisLine: { lineStyle: { width: 8, color: [[1, 'rgba(255,255,255,0.05)']] } },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: { show: false },
      data: [{ value: val }],
    }],
  }
})

// 环图配置
const ringOption = computed<echarts.EChartsOption>(() => {
  const running = props.overview?.running_count ?? 0
  const stopped = props.overview?.stopped_count ?? 0
  const maint = props.overview?.maintenance_count ?? 0
  const fault = props.overview?.fault_count ?? 0

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(2, 13, 31, 0.85)',
      borderColor: 'rgba(0, 212, 255, 0.3)',
      textStyle: { color: '#e0e6ed', fontSize: 11 },
      formatter: '{b}: {c}台 ({d}%)',
    },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 4,
        borderColor: 'rgba(2, 13, 31, 0.5)',
        borderWidth: 2,
      },
      label: {
        show: true,
        color: 'rgba(255,255,255,0.5)',
        fontSize: 9,
        formatter: '{b}\n{d}%',
      },
      labelLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      data: [
        { value: running, name: '运行', itemStyle: { color: '#00ff88' } },
        { value: stopped, name: '停机', itemStyle: { color: '#ffd93d' } },
        { value: maint, name: '维护', itemStyle: { color: '#00d4ff' } },
        { value: fault, name: '故障', itemStyle: { color: '#ff6b6b' } },
      ],
    }],
  }
})

function initCharts() {
  if (gaugeRef.value && !gaugeChart) {
    gaugeChart = echarts.init(gaugeRef.value, 'dark')
    gaugeChart.setOption(gaugeOption.value)
    gaugeObserver = new ResizeObserver(() => gaugeChart?.resize())
    gaugeObserver.observe(gaugeRef.value)
  }
  if (ringRef.value && !ringChart) {
    ringChart = echarts.init(ringRef.value, 'dark')
    ringChart.setOption(ringOption.value)
    ringObserver = new ResizeObserver(() => ringChart?.resize())
    ringObserver.observe(ringRef.value)
  }
}

watch(gaugeOption, (opt) => gaugeChart?.setOption(opt, true), { deep: true })
watch(ringOption, (opt) => ringChart?.setOption(opt, true), { deep: true })

onMounted(initCharts)

onBeforeUnmount(() => {
  gaugeObserver?.disconnect()
  ringObserver?.disconnect()
  gaugeChart?.dispose()
  ringChart?.dispose()
})
</script>

<style scoped>
.wind-info { display: flex; flex-direction: column; height: 100%; }
.gauge-section { position: relative; height: 120px; flex-shrink: 0; }
.gauge-title, .ring-title { font-size: var(--text-xs); color: var(--text-secondary); margin-bottom: 2px; }
.gauge-chart { width: 100%; height: 100px; }

.gauge-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -30%);
  text-align: center;
}
.gauge-num { font-size: var(--text-2xl); font-weight: 700; color: #fff; font-family: 'Courier New', monospace; }
.gauge-unit { font-size: var(--text-xs); color: var(--text-muted); margin-left: 2px; }

.stats-section { flex: 1; padding: 8px 0; display: flex; flex-direction: column; gap: 6px; }
.stat-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 5px 8px; background: rgba(255,255,255,0.02);
  border-radius: var(--radius-sm); font-size: var(--text-xs);
}
.stat-label { color: var(--text-secondary); }
.stat-value { font-family: 'Courier New', monospace; font-weight: 600; color: var(--text-primary); }
.stat-value.highlight { color: var(--color-success); }
.stat-value.danger { color: var(--color-danger); }
.stat-value small { color: var(--text-muted); font-size: 10px; }

.ring-section { height: 120px; flex-shrink: 0; }
.ring-chart { width: 100%; height: 100px; }
</style>
