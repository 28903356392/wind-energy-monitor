<template>
  <div class="dashboard">
    <!-- 顶部标题栏 -->
    <header class="header">
      <div class="header-decoration left"></div>
      <div class="header-content">
        <h1 class="title">🌬️ 风电场智能监控平台</h1>
        <div class="subtitle">Wind Energy Monitoring System</div>
      </div>
      <div class="header-decoration right"></div>
      <div class="clock">{{ currentTime }}</div>
    </header>

    <!-- 核心指标 -->
    <StatsCards :overview="overviewData" />

    <!-- 中间主体 -->
    <div class="main-content">
      <!-- 左侧：风机状态列表 -->
      <div class="panel panel-left">
        <div class="panel-header">
          <span class="panel-dot"></span>
          风机运行状态
        </div>
        <div class="panel-body">
          <TurbineStatus :turbines="turbines" />
        </div>
      </div>

      <!-- 中间：发电量趋势图 -->
      <div class="panel panel-center">
        <div class="panel-header">
          <span class="panel-dot"></span>
          发电功率趋势 (kW)
        </div>
        <div class="panel-body">
          <PowerChart :history="powerHistory" :realtime-total="overviewData?.total_power || 0" />
        </div>
      </div>

      <!-- 右侧：风况信息 -->
      <div class="panel panel-right">
        <div class="panel-header">
          <span class="panel-dot"></span>
          风况统计
        </div>
        <div class="panel-body">
          <WindInfo :overview="overviewData" />
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <footer class="footer">
      <span>数据每3秒自动更新</span>
      <span class="sep">|</span>
      <span v-if="wsConnected" class="status-online">🟢 WebSocket 已连接</span>
      <span v-else class="status-offline">🔴 WebSocket 未连接</span>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { getOverview, getTurbines, getPowerHistory, createWebSocket } from '../api/index.js'
import StatsCards from '../components/StatsCards.vue'
import TurbineStatus from '../components/TurbineStatus.vue'
import PowerChart from '../components/PowerChart.vue'
import WindInfo from '../components/WindInfo.vue'

const overviewData = ref(null)
const turbines = ref([])
const powerHistory = ref([])
const currentTime = ref('')
const wsConnected = ref(false)

let timer = null
let ws = null

function updateClock() {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false
  })
}

async function fetchData() {
  try {
    const [overviewRes, turbinesRes, historyRes] = await Promise.all([
      getOverview(),
      getTurbines(),
      getPowerHistory(24)
    ])
    overviewData.value = overviewRes.data.data
    turbines.value = turbinesRes.data.data
    powerHistory.value = historyRes.data.data
  } catch (err) {
    console.error('数据获取失败:', err)
  }
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
  fetchData()

  // 建立 WebSocket 实时连接
  ws = createWebSocket((data) => {
    wsConnected.value = true
    if (data.type === 'update') {
      overviewData.value = {
        ...(overviewData.value || {}),
        total_power: data.total_power,
        updated_at: data.timestamp
      }
      turbines.value = data.turbines
    }
  })
})

onBeforeUnmount(() => {
  clearInterval(timer)
  if (ws) ws.close()
})
</script>

<style scoped>
.dashboard {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #020d1f 0%, #0a1a3a 50%, #020d1f 100%);
  padding: 12px 16px;
  overflow: hidden;
}

/* 顶部标题 */
.header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70px;
  min-height: 70px;
  margin-bottom: 12px;
}

.header-decoration {
  width: 200px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.header-decoration.left { transform: rotate(180deg); }

.header-content {
  text-align: center;
  padding: 0 30px;
}

.title {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(90deg, #00d4ff, #00ff88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 6px;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
}

.subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 4px;
  margin-top: 2px;
}

.clock {
  position: absolute;
  right: 10px;
  font-size: 16px;
  color: #00d4ff;
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
}

/* 中间内容 */
.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 12px;
  min-height: 0;
}

.panel {
  background: rgba(0, 40, 80, 0.35);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 10px 14px;
  font-size: 14px;
  font-weight: 600;
  color: #00d4ff;
  background: rgba(0, 212, 255, 0.06);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.panel-dot {
  width: 8px;
  height: 8px;
  background: #00d4ff;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.6);
}

.panel-body {
  flex: 1;
  padding: 10px;
  overflow: auto;
}

/* 底部 */
.footer {
  height: 32px;
  min-height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  border-top: 1px solid rgba(0, 212, 255, 0.08);
  margin-top: 8px;
}

.sep { color: rgba(255, 255, 255, 0.15); }

.status-online { color: #00ff88; }
.status-offline { color: #ff6b6b; }

/* 滚动条美化 */
.panel-body::-webkit-scrollbar {
  width: 4px;
}
.panel-body::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 2px;
}
</style>
