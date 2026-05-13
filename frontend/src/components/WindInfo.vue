<template>
  <div class="wind-info">
    <!-- 风速仪表盘 -->
    <div class="gauge-section">
      <div class="gauge-title">实时风速</div>
      <div ref="gaugeRef" class="gauge-chart"></div>
      <div class="gauge-value">
        <span class="gauge-num">{{ overview?.avg_wind_speed?.toFixed(1) ?? '--' }}</span>
        <span class="gauge-unit">m/s</span>
      </div>
    </div>

    <!-- 风能统计 -->
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

    <!-- 功率占比环 -->
    <div class="ring-section">
      <div class="ring-title">功率占比</div>
      <div ref="ringRef" class="ring-chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  overview: { type: Object, default: null }
})

const gaugeRef = ref(null)
const ringRef = ref(null)
let gaugeChart = null
let ringChart = null

function formatEnergy(val, unit = 'MWh') {
  if (!val && val !== 0) return '--'
  if (val >= 1000000) return (val / 10000).toFixed(1) + '万' + unit
  if (val >= 1000) return (val / 1000).toFixed(1) + '千' + unit
  return val.toFixed(1) + ' ' + unit
}

function initGauge() {
  if (!gaugeRef.value) return
  gaugeChart = echarts.init(gaugeRef.value, 'dark')
  updateGauge()
}

function updateGauge() {
  if (!gaugeChart) return
  const val = props.overview?.avg_wind_speed ?? 0
  const option = {
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
              { offset: 1, color: '#ffd93d' }
            ]
          }
        }
      },
      axisLine: {
        lineStyle: { width: 8, color: [[1, 'rgba(255,255,255,0.05)']] }
      },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      detail: { show: false },
      data: [{ value: val }]
    }]
  }
  gaugeChart.setOption(option, true)
}

function initRing() {
  if (!ringRef.value) return
  ringChart = echarts.init(ringRef.value, 'dark')
  updateRing()
}

function updateRing() {
  if (!ringChart) return
  const running = props.overview?.running_count ?? 0
  const stopped = props.overview?.stopped_count ?? 0
  const maint = props.overview?.maintenance_count ?? 0
  const fault = props.overview?.fault_count ?? 0
  const total = running + stopped + maint + fault || 1

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(2, 13, 31, 0.85)',
      borderColor: 'rgba(0, 212, 255, 0.3)',
      textStyle: { color: '#e0e6ed', fontSize: 11 },
      formatter: '{b}: {c}台 ({d}%)'
    },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 4,
        borderColor: 'rgba(2, 13, 31, 0.5)',
        borderWidth: 2
      },
      label: {
        show: true,
        color: 'rgba(255,255,255,0.5)',
        fontSize: 9,
        formatter: '{b}\n{d}%'
      },
      labelLine: {
        lineStyle: { color: 'rgba(255,255,255,0.1)' }
      },
      data: [
        { value: running, name: '运行', itemStyle: { color: '#00ff88' } },
        { value: stopped, name: '停机', itemStyle: { color: '#ffd93d' } },
        { value: maint, name: '维护', itemStyle: { color: '#00d4ff' } },
        { value: fault, name: '故障', itemStyle: { color: '#ff6b6b' } }
      ]
    }]
  }
  ringChart.setOption(option, true)
}

watch(() => props.overview, () => {
  updateGauge()
  updateRing()
}, { deep: true })

onMounted(() => {
  initGauge()
  initRing()
})

onBeforeUnmount(() => {
  gaugeChart?.dispose()
  ringChart?.dispose()
})
</script>

<style scoped>
.wind-info {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.gauge-section {
  position: relative;
  height: 120px;
  flex-shrink: 0;
}

.gauge-title, .ring-title {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  margin-bottom: 2px;
}

.gauge-chart {
  width: 100%;
  height: 100px;
}

.gauge-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -30%);
  text-align: center;
}
.gauge-num {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  font-family: 'Courier New', monospace;
}
.gauge-unit {
  font-size: 11px;
  color: rgba(255,255,255,0.3);
  margin-left: 2px;
}

.stats-section {
  flex: 1;
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 8px;
  background: rgba(255,255,255,0.02);
  border-radius: 4px;
  font-size: 12px;
}
.stat-label { color: rgba(255,255,255,0.5); }
.stat-value { font-family: 'Courier New', monospace; font-weight: 600; color: #e0e6ed; }
.stat-value.highlight { color: #00ff88; }
.stat-value.danger { color: #ff6b6b; }
.stat-value small { color: rgba(255,255,255,0.3); font-size: 10px; }

.ring-section {
  height: 120px;
  flex-shrink: 0;
}
.ring-chart {
  width: 100%;
  height: 100px;
}
</style>
