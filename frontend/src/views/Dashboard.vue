<template>
  <div class="dashboard">
    <!-- 顶部标题栏 -->
    <header class="header">
      <div class="header-decoration left"></div>
      <div class="header-content">
        <h1 class="title">风电场智能监控平台</h1>
        <div class="subtitle">Wind Energy Monitoring System</div>
      </div>
      <div class="header-decoration right"></div>
      <div class="header-right">
        <nav class="nav-links">
          <router-link to="/" class="nav-link active">总览</router-link>
          <router-link to="/alarms" class="nav-link">告警</router-link>
          <router-link to="/energy" class="nav-link">报告</router-link>
        </nav>
        <div class="clock">{{ time }}</div>
      </div>
    </header>

    <!-- 核心指标 -->
    <StatsCards :overview="overviewData" />

    <!-- 中间主体 -->
    <div class="main-content">
      <div class="panel panel-left">
        <div class="panel-header">
          <span class="panel-dot"></span>
          风机运行状态
        </div>
        <div class="panel-body">
          <TurbineStatus :turbines="turbines" />
        </div>
      </div>

      <div class="panel panel-center">
        <div class="panel-header">
          <span class="panel-dot"></span>
          发电功率趋势 (kW)
        </div>
        <div class="panel-body">
          <PowerChart :history="powerHistory" :realtime-total="overviewData?.total_power || 0" />
        </div>
      </div>

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
      <span v-if="wsConnected" class="status-online">WebSocket 已连接</span>
      <span v-else class="status-offline">WebSocket 未连接</span>
      <span class="sep">|</span>
      <span class="alarm-badge" v-if="alarmCount > 0" @click="$router.push('/alarms')">
        未处理告警 {{ alarmCount }} 条
      </span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useClock } from '../composables/useClock'
import { useWebSocket } from '../composables/useWebSocket'
import { fetchDashboardData } from '../api/modules'
import StatsCards from '../components/StatsCards.vue'
import TurbineStatus from '../components/TurbineStatus.vue'
import PowerChart from '../components/PowerChart.vue'
import WindInfo from '../components/WindInfo.vue'
import type { OverviewData, Turbine, PowerRecord, WsMessage } from '../types'

const router = useRouter()
const { time } = useClock()

const overviewData = ref<OverviewData | null>(null)
const turbines = ref<Turbine[]>([])
const powerHistory = ref<PowerRecord[]>([])
const alarmCount = ref(0)

// WebSocket
const { connected: wsConnected, connect: wsConnect } = useWebSocket((data: WsMessage) => {
  if (data.type === 'update') {
    overviewData.value = {
      ...(overviewData.value || {} as OverviewData),
      total_power: data.total_power,
      updated_at: data.timestamp,
    } as OverviewData
    turbines.value = data.turbines as Turbine[]
  } else if (data.type === 'alarm') {
    alarmCount.value++
  }
})

// 初始加载
onMounted(async () => {
  try {
    const data = await fetchDashboardData()
    overviewData.value = data.overview
    turbines.value = data.turbines
    powerHistory.value = data.powerHistory
  } catch (err) {
    console.error('数据获取失败:', err)
  }
  wsConnect()
})
</script>

<style scoped>
.dashboard {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
  padding: clamp(8px, 1.2vh, 16px) clamp(10px, 1.5vw, 24px);
  overflow: hidden;
}

/* 顶部标题 */
.header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: clamp(56px, 6vh, 80px);
  min-height: 56px;
  margin-bottom: clamp(8px, 1vh, 16px);
}
.header-decoration {
  width: clamp(120px, 15vw, 240px);
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
}
.header-decoration.left { transform: rotate(180deg); }
.header-content { text-align: center; padding: 0 clamp(16px, 3vw, 40px); }

.title {
  font-size: clamp(20px, 2.5vw, 34px);
  font-weight: 700;
  background: linear-gradient(90deg, var(--color-primary), var(--color-success));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 6px;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
}
.subtitle {
  font-size: clamp(10px, 0.7vw, 13px);
  color: var(--text-muted);
  letter-spacing: 4px;
  margin-top: 2px;
}

.header-right {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-links { display: flex; gap: 4px; }
.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  font-size: var(--text-xs);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}
.nav-link:hover, .nav-link.active {
  color: var(--color-primary);
  background: rgba(0, 212, 255, 0.1);
}

.clock {
  font-size: var(--text-sm);
  color: var(--color-primary);
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
  white-space: nowrap;
}

/* 中间内容 */
.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: clamp(220px, 18vw, 320px) 1fr clamp(220px, 18vw, 320px);
  gap: clamp(8px, 1vw, 14px);
  min-height: 0;
}

.panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.panel-header {
  padding: var(--space-sm) var(--space-md);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-primary);
  background: rgba(0, 212, 255, 0.06);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;
}
.panel-dot { width: 8px; height: 8px; background: var(--color-primary); border-radius: 50%; box-shadow: 0 0 8px rgba(0, 212, 255, 0.6); }
.panel-body { flex: 1; padding: var(--space-md); overflow: auto; min-height: 0; }

/* 底部 */
.footer {
  height: clamp(28px, 3vh, 36px);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(8px, 1vw, 16px);
  font-size: var(--text-xs);
  color: var(--text-muted);
  border-top: 1px solid var(--border-light);
  margin-top: clamp(4px, 0.8vh, 10px);
  flex-shrink: 0;
}
.sep { color: rgba(255, 255, 255, 0.1); }
.status-online { color: var(--color-success); }
.status-offline { color: var(--color-danger); }
.alarm-badge { color: var(--color-warning); cursor: pointer; }
.alarm-badge:hover { text-decoration: underline; }
</style>
