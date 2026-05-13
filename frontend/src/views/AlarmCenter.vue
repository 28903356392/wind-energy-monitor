<template>
  <div class="page">
    <!-- 顶部 -->
    <header class="page-header">
      <router-link to="/" class="back-btn">← 返回大屏</router-link>
      <h2 class="page-title">告警中心</h2>
      <div class="header-spacer"></div>
    </header>

    <!-- 告警统计 -->
    <div class="stats-row">
      <div class="stat-card critical">
        <div class="stat-num">{{ stats.critical }}</div>
        <div class="stat-lbl">严重告警</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-num">{{ stats.warning }}</div>
        <div class="stat-lbl">普通警告</div>
      </div>
      <div class="stat-card info">
        <div class="stat-num">{{ stats.info }}</div>
        <div class="stat-lbl">提示信息</div>
      </div>
      <div class="stat-card total">
        <div class="stat-num">{{ stats.total }}</div>
        <div class="stat-lbl">告警总数</div>
      </div>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <button
        v-for="f in filters"
        :key="f.key"
        class="filter-btn"
        :class="{ active: activeFilter === f.key }"
        @click="activeFilter = f.key"
      >{{ f.label }}</button>
    </div>

    <!-- 告警列表 -->
    <div class="alarm-list">
      <div v-for="alarm in filteredAlarms" :key="alarm.id" class="alarm-item" :class="'level-' + alarm.level">
        <div class="alarm-icon" :style="{ background: getLevelColor(alarm.level) + '22', color: getLevelColor(alarm.level) }">
          {{ alarm.level === 'critical' ? '✕' : alarm.level === 'warning' ? '!' : 'i' }}
        </div>
        <div class="alarm-info">
          <div class="alarm-msg">{{ alarm.message }}</div>
          <div class="alarm-meta">
            {{ alarm.turbine_name }} · 当前值: {{ alarm.value }} · 阈值: {{ alarm.threshold }}
          </div>
        </div>
        <div class="alarm-time">{{ formatTime(alarm.created_at) }}</div>
      </div>
      <div v-if="!filteredAlarms.length" class="empty-state">
        <div class="empty-icon">✓</div>
        <div>暂无告警</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { fetchAlarms, fetchAlarmStats } from '../api/modules'
import { AlarmLevel, type Alarm } from '../types'

const alarms = ref<Alarm[]>([])
const stats = ref({ total: 0, critical: 0, warning: 0, info: 0 })
const activeFilter = ref<string>('all')

const filters = [
  { key: 'all', label: '全部' },
  { key: 'critical', label: '严重' },
  { key: 'warning', label: '警告' },
  { key: 'info', label: '提示' },
]

const filteredAlarms = computed(() => {
  if (activeFilter.value === 'all') return alarms.value
  return alarms.value.filter((a) => a.level === activeFilter.value)
})

function getLevelColor(level: string): string {
  const map: Record<string, string> = {
    critical: 'var(--color-danger)',
    warning: 'var(--color-warning)',
    info: 'var(--color-primary)',
  }
  return map[level] || 'var(--text-muted)'
}

function formatTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', {
    month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}

onMounted(async () => {
  try {
    const [alarmRes, statsRes] = await Promise.all([
      fetchAlarms(),
      fetchAlarmStats(),
    ])
    alarms.value = alarmRes.data
    stats.value = statsRes.data
  } catch (err) {
    console.error('获取告警失败:', err)
  }
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
.back-btn:hover { text-decoration: underline; }
.page-title {
  font-size: var(--text-xl);
  color: #fff;
  font-weight: 700;
  letter-spacing: 4px;
}
.header-spacer { width: 80px; }

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: clamp(8px, 1vw, 14px);
  margin-bottom: clamp(8px, 1.5vh, 16px);
  flex-shrink: 0;
}
.stat-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: clamp(10px, 1.5vw, 20px);
  text-align: center;
}
.stat-num { font-size: var(--text-2xl); font-weight: 700; font-family: 'Courier New', monospace; }
.stat-lbl { font-size: var(--text-xs); color: var(--text-secondary); margin-top: 4px; }
.stat-card.critical .stat-num { color: var(--color-danger); }
.stat-card.warning .stat-num { color: var(--color-warning); }
.stat-card.info .stat-num { color: var(--color-primary); }
.stat-card.total .stat-num { color: var(--color-info); }

.filter-bar {
  display: flex;
  gap: 8px;
  margin-bottom: clamp(8px, 1vh, 14px);
  flex-shrink: 0;
}
.filter-btn {
  padding: 6px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-size: var(--text-xs);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.filter-btn:hover, .filter-btn.active {
  background: rgba(0, 212, 255, 0.1);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.alarm-list { flex: 1; overflow: auto; display: flex; flex-direction: column; gap: 6px; }
.alarm-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: clamp(8px, 1vw, 14px) clamp(10px, 1.2vw, 18px);
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  border-left: 4px solid transparent;
}
.alarm-item.level-critical { border-left-color: var(--color-danger); }
.alarm-item.level-warning { border-left-color: var(--color-warning); }
.alarm-item.level-info { border-left-color: var(--color-primary); }

.alarm-icon {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}
.alarm-info { flex: 1; min-width: 0; }
.alarm-msg { font-size: var(--text-sm); color: var(--text-primary); font-weight: 500; }
.alarm-meta { font-size: var(--text-xs); color: var(--text-secondary); margin-top: 2px; }
.alarm-time { font-size: var(--text-xs); color: var(--text-muted); white-space: nowrap; flex-shrink: 0; }

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: var(--text-base);
  gap: 8px;
}
.empty-icon {
  width: 60px; height: 60px;
  border-radius: 50%;
  background: rgba(0, 255, 136, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: var(--color-success);
}
</style>
