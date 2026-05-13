<template>
  <div class="stats-cards">
    <div class="card">
      <div class="card-icon power-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00d4ff" stroke-width="2">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
      </div>
      <div class="card-info">
        <div class="card-label">当前总功率</div>
        <div class="card-value">
          {{ formatNum(overview?.total_power) }}
          <span class="card-unit">kW</span>
        </div>
      </div>
      <div class="card-trend up">实时</div>
    </div>
    <div class="card">
      <div class="card-icon energy-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00ff88" stroke-width="2">
          <rect x="2" y="7" width="20" height="14" rx="2"/>
          <path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/>
        </svg>
      </div>
      <div class="card-info">
        <div class="card-label">日发电量</div>
        <div class="card-value">
          {{ formatNum(overview?.total_daily_energy) }}
          <span class="card-unit">kWh</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-icon wind-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffd93d" stroke-width="2">
          <path d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
        </svg>
      </div>
      <div class="card-info">
        <div class="card-label">平均风速</div>
        <div class="card-value">
          {{ overview?.avg_wind_speed ?? '--' }}
          <span class="card-unit">m/s</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-icon turbine-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#c084fc" stroke-width="2">
          <circle cx="12" cy="12" r="3"/>
          <path d="M12 1v4m0 14v4m11-11h-4M5 12H1m17.07-6.07l-2.83 2.83M8.76 15.24l-2.83 2.83M20.49 15.24l-2.83-2.83M8.76 8.76L5.93 5.93"/>
        </svg>
      </div>
      <div class="card-info">
        <div class="card-label">风机总数</div>
        <div class="card-value">
          {{ overview?.turbine_count ?? 0 }}
          <span class="card-unit">台</span>
        </div>
      </div>
      <div class="status-tags">
        <span class="tag tag-running">运行 {{ overview?.running_count ?? 0 }}</span>
        <span class="tag tag-stopped">停机 {{ overview?.stopped_count ?? 0 }}</span>
        <span class="tag tag-fault">故障 {{ overview?.fault_count ?? 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { OverviewData } from '../types'

defineProps<{
  overview: OverviewData | null
}>()

function formatNum(val: number | null | undefined): string {
  if (val === null || val === undefined) return '--'
  return Number(val).toLocaleString('zh-CN', { maximumFractionDigits: 1 })
}
</script>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: clamp(8px, 1vw, 14px);
  margin-bottom: var(--space-sm);
  flex-shrink: 0;
}

.card {
  position: relative;
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: clamp(10px, 1.2vw, 18px);
  display: flex;
  align-items: center;
  gap: clamp(8px, 1vw, 16px);
  overflow: hidden;
  transition: all var(--transition-normal);
}
.card:hover {
  transform: translateY(-2px);
  background: var(--bg-panel-hover);
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px;
  height: 100%;
}
.card:nth-child(1)::before { background: var(--color-primary); }
.card:nth-child(2)::before { background: var(--color-success); }
.card:nth-child(3)::before { background: var(--color-warning); }
.card:nth-child(4)::before { background: var(--color-info); }

.card-icon {
  width: clamp(36px, 3vw, 48px);
  height: clamp(36px, 3vw, 48px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.power-icon { background: rgba(0, 212, 255, 0.12); }
.energy-icon { background: rgba(0, 255, 136, 0.12); }
.wind-icon { background: rgba(255, 217, 61, 0.12); }
.turbine-icon { background: rgba(192, 132, 252, 0.12); }

.card-info { flex: 1; min-width: 0; }
.card-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-bottom: 2px;
}
.card-value {
  font-size: var(--text-xl);
  font-weight: 700;
  color: #fff;
  font-family: 'Courier New', monospace;
  line-height: 1.2;
}
.card-unit {
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 2px;
}

.card-trend {
  position: absolute;
  top: 8px; right: 10px;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: var(--radius-sm);
}
.card-trend.up { color: var(--color-success); background: rgba(0, 255, 136, 0.1); }

.status-tags { display: flex; gap: 4px; flex-wrap: wrap; }
.tag {
  font-size: var(--text-xs);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  white-space: nowrap;
}
.tag-running { background: rgba(0, 255, 136, 0.15); color: var(--color-success); }
.tag-stopped { background: rgba(255, 217, 61, 0.15); color: var(--color-warning); }
.tag-fault { background: rgba(255, 107, 107, 0.15); color: var(--color-danger); }
</style>
