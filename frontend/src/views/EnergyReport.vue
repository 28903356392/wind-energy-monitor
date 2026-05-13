<template>
  <div class="page">
    <header class="page-header">
      <router-link to="/" class="back-btn">← 返回大屏</router-link>
      <h2 class="page-title">能源报告</h2>
      <div class="header-spacer"></div>
    </header>

    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">今日发电</div>
        <div class="stat-value success">{{ formatEnergy(stats.today) }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">昨日发电</div>
        <div class="stat-value">{{ formatEnergy(stats.yesterday) }}</div>
        <div class="stat-compare" :class="trendClass">环比 {{ trendPercent }}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">本周发电</div>
        <div class="stat-value primary">{{ formatEnergy(stats.this_week) }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">本月发电</div>
        <div class="stat-value info">{{ formatEnergy(stats.this_month) }}</div>
      </div>
    </div>

    <div class="charts-grid">
      <!-- 功率趋势图 -->
      <PanelContainer title="发电功率趋势 (24h)" :flex="1.5">
        <div ref="powerTrendRef" class="full-chart"></div>
      </PanelContainer>

      <!-- 风速 vs 功率散点图 -->
      <PanelContainer title="风速-功率相关性" :flex="1">
        <div ref="scatterRef" class="full-chart"></div>
      </PanelContainer>
    </div>

    <!-- 效率指标 -->
    <PanelContainer title="运行效率指标" :flex="0.4">
      <div class="efficiency-row">
        <div class="efficiency-item">
          <div class="eff-label">容量利用率</div>
          <div class="eff-bar">
            <div class="eff-fill" style="width: 78%"></div>
          </div>
          <div class="eff-val">78%</div>
        </div>
        <div class="efficiency-item">
          <div class="eff-label">可利用率</div>
          <div class="eff-bar">
            <div class="eff-fill" style="width: 92%"></div>
          </div>
          <div class="eff-val">92%</div>
        </div>
        <div class="efficiency-item">
          <div class="eff-label">综合效率</div>
          <div class="eff-bar">
            <div class="eff-fill" style="width: 85%"></div>
          </div>
          <div class="eff-val">85%</div>
        </div>
      </div>
    </PanelContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import * as echarts from 'echarts'
import { fetchPowerHistory, fetchEnergyStats } from '../api/modules'
import PanelContainer from '../components/common/PanelContainer.vue'
import type { PowerRecord } from '../types'

const stats = ref({
  today: 0, yesterday: 0, this_week: 0, this_month: 0,
  last_month: 0, total: 0, efficiency: 0,
})

const powerHistory = ref<PowerRecord[]>([])

// 环比计算
const trendPercent = computed(() => {
  if (!stats.value.yesterday) return 0
  return (((stats.value.today - stats.value.yesterday) / stats.value.yesterday) * 100).toFixed(1)
})
const trendClass = computed(() =>
  Number(trendPercent.value) >= 0 ? 'trend-up' : 'trend-down'
)

function formatEnergy(val: number): string {
  if (val >= 1000000) return (val / 10000).toFixed(1) + '万kWh'
  if (val >= 1000) return (val / 1000).toFixed(1) + '千kWh'
  return val.toFixed(1) + ' kWh'
}

// 图表
const powerTrendRef = ref<HTMLDivElement | null>(null)
const scatterRef = ref<HTMLDivElement | null>(null)
let powerTrendChart: echarts.ECharts | null = null
let scatterChart: echarts.ECharts | null = null
let observers: ResizeObserver[] = []

const powerTrendOption = computed<echarts.EChartsOption | null>(() => {
  if (!powerHistory.value.length) return null
  const data = powerHistory.value.slice(-96)
  return {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(2,13,31,0.85)', textStyle: { color: '#e0e6ed' } },
    grid: { left: 50, right: 16, top: 10, bottom: 24 },
    xAxis: {
      type: 'category',
      data: data.map(d => new Date(d.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })),
      axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 9 },
      axisLine: { lineStyle: { color: 'rgba(0,212,255,0.15)' } },
    },
    yAxis: {
      type: 'value',
      name: 'kW',
      nameTextStyle: { color: 'rgba(255,255,255,0.3)' },
      axisLabel: { color: 'rgba(255,255,255,0.3)' },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,0.06)', type: 'dashed' } },
    },
    series: [{
      type: 'line',
      data: data.map(d => d.total_power),
      smooth: true,
      symbol: 'none',
      lineStyle: { width: 2, color: '#00d4ff' },
      areaStyle: {
        color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [
          { offset: 0, color: 'rgba(0,212,255,0.2)' },
          { offset: 1, color: 'rgba(0,212,255,0.02)' },
        ]},
      },
    }],
  }
})

const scatterOption = computed<echarts.EChartsOption | null>(() => {
  if (!powerHistory.value.length) return null
  const data = powerHistory.value.slice(-96).map(d => [d.avg_wind_speed, d.total_power])
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(2,13,31,0.85)',
      textStyle: { color: '#e0e6ed' },
      formatter: (params: any) => `风速: ${params.value[0]} m/s<br/>功率: ${params.value[1]} kW`,
    },
    grid: { left: 50, right: 20, top: 10, bottom: 30 },
    xAxis: {
      type: 'value',
      name: '风速 (m/s)',
      nameTextStyle: { color: 'rgba(255,255,255,0.3)' },
      axisLabel: { color: 'rgba(255,255,255,0.3)' },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,0.06)', type: 'dashed' } },
    },
    yAxis: {
      type: 'value',
      name: '功率 (kW)',
      nameTextStyle: { color: 'rgba(255,255,255,0.3)' },
      axisLabel: { color: 'rgba(255,255,255,0.3)' },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,0.06)', type: 'dashed' } },
    },
    series: [{
      type: 'scatter',
      data,
      symbolSize: 8,
      itemStyle: {
        color: {
          type: 'radial',
          x: 0.5, y: 0.5, r: 0.5,
          colorStops: [
            { offset: 0, color: 'rgba(0,212,255,0.8)' },
            { offset: 1, color: 'rgba(0,255,136,0.2)' },
          ],
        },
      },
    }],
  }
})

function initCharts() {
  if (powerTrendRef.value) {
    powerTrendChart = echarts.init(powerTrendRef.value, 'dark')
    powerTrendChart.setOption(powerTrendOption.value!)
    const obs = new ResizeObserver(() => powerTrendChart?.resize())
    obs.observe(powerTrendRef.value)
    observers.push(obs)
  }
  if (scatterRef.value) {
    scatterChart = echarts.init(scatterRef.value, 'dark')
    scatterChart.setOption(scatterOption.value!)
    const obs = new ResizeObserver(() => scatterChart?.resize())
    obs.observe(scatterRef.value)
    observers.push(obs)
  }
}

onMounted(async () => {
  try {
    const [historyRes, statsRes] = await Promise.all([
      fetchPowerHistory(24),
      fetchEnergyStats(),
    ])
    powerHistory.value = historyRes.data
    stats.value = statsRes.data
  } catch (err) {
    console.error('获取能源数据失败:', err)
  }
  initCharts()
})

onBeforeUnmount(() => {
  observers.forEach(o => o.disconnect())
  powerTrendChart?.dispose()
  scatterChart?.dispose()
})
</script>

<style scoped>
.page {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
  padding: clamp(12px, 2vh, 24px) clamp(16px, 2vw, 32px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  gap: clamp(8px, 1vh, 16px);
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}
.back-btn { color: var(--color-primary); text-decoration: none; font-size: var(--text-sm); }
.page-title { font-size: var(--text-xl); color: #fff; font-weight: 700; letter-spacing: 4px; }
.header-spacer { width: 80px; }

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: clamp(8px, 1vw, 14px);
  flex-shrink: 0;
}
.stat-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: clamp(10px, 1.5vw, 20px);
}
.stat-label { font-size: var(--text-xs); color: var(--text-secondary); margin-bottom: 4px; }
.stat-value { font-size: var(--text-lg); font-weight: 700; color: #fff; font-family: 'Courier New', monospace; }
.stat-value.success { color: var(--color-success); }
.stat-value.primary { color: var(--color-primary); }
.stat-value.info { color: var(--color-info); }
.stat-compare { font-size: 11px; margin-top: 4px; }
.trend-up { color: var(--color-success); }
.trend-down { color: var(--color-danger); }

.charts-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: clamp(8px, 1vw, 14px);
  min-height: 0;
}
.full-chart { width: 100%; height: 100%; min-height: 180px; }

.efficiency-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  align-items: center;
  padding: 8px 0;
}
.efficiency-item { display: flex; align-items: center; gap: 12px; }
.eff-label { font-size: var(--text-sm); color: var(--text-secondary); min-width: 80px; }
.eff-bar {
  flex: 1;
  height: 10px;
  background: rgba(255,255,255,0.05);
  border-radius: 5px;
  overflow: hidden;
}
.eff-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-success));
  border-radius: 5px;
  transition: width 1s ease;
}
.eff-val { font-size: var(--text-sm); font-weight: 600; color: #fff; min-width: 40px; text-align: right; }
</style>
