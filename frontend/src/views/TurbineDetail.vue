<template>
  <div class="page">
    <header class="page-header">
      <router-link to="/" class="back-btn">← 返回大屏</router-link>
      <h2 class="page-title" v-if="turbine">{{ turbine.name }} 详情</h2>
      <div class="header-spacer"></div>
    </header>

    <!-- 加载态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>

    <template v-if="turbine && !loading">
      <!-- 概览卡片 -->
      <div class="overview-row">
        <div class="info-card">
          <div class="label">运行状态</div>
          <div class="value" :class="'tag-' + turbine.status">
            <span class="status-dot" :class="'dot-' + turbine.status"></span>
            {{ statusLabel(turbine.status) }}
          </div>
        </div>
        <div class="info-card">
          <div class="label">当前功率</div>
          <div class="value primary">{{ turbine.power_output?.toFixed(1) }} <small>kW</small></div>
        </div>
        <div class="info-card">
          <div class="label">日发电量</div>
          <div class="value success">{{ turbine.daily_energy?.toFixed(1) }} <small>kWh</small></div>
        </div>
        <div class="info-card">
          <div class="label">总发电量</div>
          <div class="value info">{{ turbine.total_energy?.toFixed(1) }} <small>MWh</small></div>
        </div>
      </div>

      <!-- 详细参数 -->
      <div class="detail-grid">
        <div class="detail-card">
          <div class="detail-label">风速</div>
          <div class="detail-value">{{ turbine.wind_speed?.toFixed(1) }} <small>m/s</small></div>
        </div>
        <div class="detail-card">
          <div class="detail-label">风向</div>
          <div class="detail-value">{{ turbine.wind_direction?.toFixed(1) }} <small>°</small></div>
        </div>
        <div class="detail-card">
          <div class="detail-label">转速</div>
          <div class="detail-value">{{ turbine.rotor_speed?.toFixed(1) }} <small>rpm</small></div>
        </div>
        <div class="detail-card">
          <div class="detail-label">温度</div>
          <div class="detail-value">{{ turbine.temperature?.toFixed(1) }} <small>°C</small></div>
        </div>
        <div class="detail-card">
          <div class="detail-label">更新时间</div>
          <div class="detail-value time">{{ formatTime(turbine.updated_at) }}</div>
        </div>
      </div>

      <!-- ECharts 功率趋势 -->
      <PanelContainer title="功率历史趋势" :flex="2">
        <div ref="trendRef" class="full-chart"></div>
      </PanelContainer>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { fetchTurbineDetail, fetchPowerHistory } from '../api/modules'
import { TurbineStatusLabel, type Turbine, type TurbineStatusEnum, type PowerRecord } from '../types'
import PanelContainer from '../components/common/PanelContainer.vue'

const route = useRoute()
const turbine = ref<Turbine | null>(null)
const loading = ref(true)
const trendRef = ref<HTMLDivElement | null>(null)
let trendChart: echarts.ECharts | null = null
let trendObserver: ResizeObserver | null = null

const historyData = ref<PowerRecord[]>([])

const chartOption = computed<echarts.EChartsOption | null>(() => {
  if (!historyData.value.length) return null
  const data = historyData.value.slice(-48)
  return {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(2,13,31,0.85)', textStyle: { color: '#e0e6ed' } },
    grid: { left: 50, right: 16, top: 10, bottom: 24 },
    xAxis: {
      type: 'category',
      data: data.map(d => new Date(d.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })),
      axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 10 },
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
      type: 'bar',
      data: data.map(d => d.total_power),
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#00d4ff' },
            { offset: 1, color: 'rgba(0,212,255,0.3)' },
          ],
        },
      },
    }],
  }
})

function statusLabel(s: TurbineStatusEnum): string {
  return TurbineStatusLabel[s] || s
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString('zh-CN')
}

onMounted(async () => {
  const id = Number(route.params.id)
  try {
    const [turbineRes, historyRes] = await Promise.all([
      fetchTurbineDetail(id),
      fetchPowerHistory(4),
    ])
    turbine.value = turbineRes.data
    historyData.value = historyRes.data

    // 初始化图表
    if (trendRef.value) {
      trendChart = echarts.init(trendRef.value, 'dark')
      trendChart.setOption(chartOption.value!)
      trendObserver = new ResizeObserver(() => trendChart?.resize())
      trendObserver.observe(trendRef.value)
    }
  } catch (err) {
    console.error('获取风机详情失败:', err)
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => {
  trendObserver?.disconnect()
  trendChart?.dispose()
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
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: clamp(12px, 1.5vh, 20px);
  flex-shrink: 0;
}
.back-btn {
  color: var(--color-primary);
  text-decoration: none;
  font-size: var(--text-sm);
}
.page-title {
  font-size: var(--text-xl);
  color: #fff;
  font-weight: 700;
  letter-spacing: 4px;
}
.header-spacer { width: 80px; }

.loading-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-secondary);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.overview-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: clamp(8px, 1vw, 14px);
  margin-bottom: clamp(8px, 1.5vh, 16px);
  flex-shrink: 0;
}
.info-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: clamp(10px, 1.5vw, 20px);
}
.label { font-size: var(--text-xs); color: var(--text-secondary); margin-bottom: 4px; }
.value { font-size: var(--text-lg); font-weight: 700; color: #fff; font-family: 'Courier New', monospace; }
.value small { font-size: var(--text-xs); color: var(--text-muted); font-weight: 400; }
.value.primary { color: var(--color-primary); }
.value.success { color: var(--color-success); }
.value.info { color: var(--color-info); }
.value.time { font-size: var(--text-sm); color: var(--text-secondary); }

.tag-running, .dot-running { color: var(--color-success); }
.dot-running, .dot-stopped, .dot-maintenance, .dot-fault {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 50%;
  margin-right: 6px;
}
.dot-running { background: var(--color-success); box-shadow: 0 0 8px rgba(0,255,136,0.5); }
.dot-stopped { background: var(--color-warning); box-shadow: 0 0 8px rgba(255,217,61,0.5); }
.dot-maintenance { background: var(--color-primary); box-shadow: 0 0 8px rgba(0,212,255,0.5); }
.dot-fault { background: var(--color-danger); box-shadow: 0 0 8px rgba(255,107,107,0.5); animation: blink 1s infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

.detail-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: clamp(6px, 0.8vw, 12px);
  margin-bottom: clamp(8px, 1.5vh, 16px);
  flex-shrink: 0;
}
.detail-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: clamp(8px, 1vw, 16px);
  text-align: center;
}
.detail-label { font-size: var(--text-xs); color: var(--text-secondary); margin-bottom: 4px; }
.detail-value { font-size: var(--text-base); font-weight: 600; color: var(--text-primary); font-family: 'Courier New', monospace; }
.detail-value small { font-size: var(--text-xs); color: var(--text-muted); font-weight: 400; }

.full-chart { width: 100%; height: 100%; min-height: 200px; }
</style>
