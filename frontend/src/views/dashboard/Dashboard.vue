<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="12">
      <el-col :span="6" v-for="card in stats" :key="card.label">
        <div class="stat-card" :style="{ borderLeftColor: card.color }">
          <div class="stat-label">{{ card.label }}</div>
          <div class="stat-value" :style="{ color: card.color }">{{ card.value }}</div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="12" style="margin-top: 12px;">
      <el-col :span="16">
        <div class="panel"><div ref="powerChartRef" style="height:300px"></div></div>
      </el-col>
      <el-col :span="8">
        <div class="panel"><div ref="statusChartRef" style="height:300px"></div></div>
      </el-col>
    </el-row>

    <!-- 表格 -->
    <el-row style="margin-top:12px;">
      <el-col>
        <div class="panel">
          <div style="padding:8px 12px;border-bottom:1px solid rgba(0,212,255,.08)">
            <span style="color:#00d4ff;font-size:13px">风机实时状态</span>
          </div>
          <el-table :data="turbines" size="small" style="width:100%" max-height="220"
            :header-cell-style="{ background:'rgba(0,212,255,.04)',color:'#a3b1cc' }"
            :cell-style="{ background:'transparent',color:'#e0e6ed' }">
            <el-table-column prop="name" label="名称" width="90" />
            <el-table-column label="状态" width="80">
              <template #default="{row}">
                <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="power_output" label="功率(kW)" width="100" />
            <el-table-column prop="wind_speed" label="风速(m/s)" width="100" />
            <el-table-column prop="rotor_speed" label="转速(rpm)" width="100" />
            <el-table-column prop="temperature" label="温度(°C)" width="100" />
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '../../utils/request.js'

const powerChartRef = ref(null)
const statusChartRef = ref(null)
let powerChart = null, statusChart = null

const stats = ref([])
const turbines = ref([])

function statusType(s) {
  return { running: 'success', stopped: 'warning', maintenance: 'info', fault: 'danger' }[s] || 'info'
}
function statusText(s) {
  return { running: '运行', stopped: '停机', maintenance: '维护', fault: '故障' }[s] || s
}

async function loadData() {
  try {
    const [overview, turbinesRes, historyRes] = await Promise.all([
      request.get('/overview'), request.get('/turbines'), request.get('/power/history?hours=24')
    ])
    const ov = overview.data.data
    stats.value = [
      { label: '总功率', value: ov.total_power + ' kW', color: '#00d4ff' },
      { label: '日发电量', value: ov.total_daily_energy + ' kWh', color: '#00ff88' },
      { label: '平均风速', value: ov.avg_wind_speed + ' m/s', color: '#ffd93d' },
      { label: '运行风机', value: ov.running_count + '/' + ov.turbine_count + ' 台', color: '#c084fc' },
    ]
    turbines.value = turbinesRes.data.data
    renderPowerChart(historyRes.data.data)
    renderStatusChart(ov)
  } catch (e) { /* ignore */ }
}

function renderPowerChart(data) {
  if (!powerChart) return
  const d = data.slice(-60)
  powerChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(2,13,31,.85)', textStyle: { color: '#e0e6ed' } },
    grid: { left: 50, right: 20, top: 30, bottom: 20 },
    xAxis: { type: 'category', data: d.map(i => new Date(i.timestamp).getHours() + ':' + String(new Date(i.timestamp).getMinutes()).padStart(2,'0')),
      axisLine: { lineStyle: { color: 'rgba(0,212,255,.15)' } },
      axisLabel: { color: 'rgba(255,255,255,.3)', fontSize: 10 } },
    yAxis: { type: 'value', name: 'kW', nameTextStyle: { color: 'rgba(255,255,255,.3)' },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,.06)' } } },
    series: [{
      type: 'line', data: d.map(i => i.total_power), smooth: true, symbol: 'none',
      lineStyle: { width: 2, color: '#00d4ff' },
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [{ offset: 0, color: 'rgba(0,212,255,.25)' }, { offset: 1, color: 'rgba(0,212,255,.02)' }] } }
    }]
  }, true)
}

function renderStatusChart(ov) {
  if (!statusChart) return
  statusChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(2,13,31,.85)', textStyle: { color: '#e0e6ed' } },
    series: [{
      type: 'pie', radius: ['40%', '70%'],
      itemStyle: { borderRadius: 4, borderColor: 'rgba(2,13,31,.5)', borderWidth: 2 },
      label: { color: 'rgba(255,255,255,.5)', fontSize: 11 },
      data: [
        { value: ov.running_count, name: '运行', itemStyle: { color: '#00ff88' } },
        { value: ov.stopped_count, name: '停机', itemStyle: { color: '#ffd93d' } },
        { value: ov.maintenance_count, name: '维护', itemStyle: { color: '#00d4ff' } },
        { value: ov.fault_count, name: '故障', itemStyle: { color: '#ff6b6b' } },
      ]
    }]
  }, true)
}

onMounted(() => {
  powerChart = echarts.init(powerChartRef.value, 'dark')
  statusChart = echarts.init(statusChartRef.value, 'dark')
  loadData()
})
onBeforeUnmount(() => { powerChart?.dispose(); statusChart?.dispose() })
</script>

<style scoped>
.dashboard { padding: 4px; }
.stat-card {
  background: rgba(10,22,40,.6);
  border: 1px solid rgba(0,212,255,.1);
  border-left: 3px solid;
  border-radius: 6px;
  padding: 14px 16px;
}
.stat-label { font-size: 12px; color: rgba(255,255,255,.4); margin-bottom: 4px; }
.stat-value { font-size: 22px; font-weight: 700; font-family: monospace; }
.panel {
  background: rgba(10,22,40,.6);
  border: 1px solid rgba(0,212,255,.1);
  border-radius: 6px;
  overflow: hidden;
}
:deep(.el-table) { background: transparent; --el-table-border-color: rgba(0,212,255,.06); }
:deep(.el-table tr) { background: transparent; }
</style>
