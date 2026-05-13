<template>
  <div class="stats-cards">
    <div class="card">
      <div class="card-icon power-icon">⚡</div>
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
      <div class="card-icon energy-icon">📊</div>
      <div class="card-info">
        <div class="card-label">日发电量</div>
        <div class="card-value">
          {{ formatNum(overview?.total_daily_energy) }}
          <span class="card-unit">kWh</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-icon wind-icon">🌪️</div>
      <div class="card-info">
        <div class="card-label">平均风速</div>
        <div class="card-value">
          {{ overview?.avg_wind_speed ?? '--' }}
          <span class="card-unit">m/s</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-icon turbine-icon">🏭</div>
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

<script setup>
defineProps({
  overview: { type: Object, default: null }
})

function formatNum(val) {
  if (val === null || val === undefined) return '--'
  return Number(val).toLocaleString('zh-CN', { maximumFractionDigits: 1 })
}
</script>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.card {
  position: relative;
  background: rgba(0, 40, 80, 0.35);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px;
  height: 100%;
}

.card:nth-child(1)::before { background: #00d4ff; }
.card:nth-child(2)::before { background: #00ff88; }
.card:nth-child(3)::before { background: #ffd93d; }
.card:nth-child(4)::before { background: #c084fc; }

.card-icon {
  font-size: 28px;
  width: 44px; height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
}

.power-icon { background: rgba(0, 212, 255, 0.12); }
.energy-icon { background: rgba(0, 255, 136, 0.12); }
.wind-icon { background: rgba(255, 217, 61, 0.12); }
.turbine-icon { background: rgba(192, 132, 252, 0.12); }

.card-info { flex: 1; min-width: 0; }

.card-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 2px;
}

.card-value {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  font-family: 'Courier New', monospace;
}

.card-unit {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 400;
  margin-left: 2px;
}

.card-trend {
  position: absolute;
  top: 8px; right: 10px;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
}

.card-trend.up {
  color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
}

.status-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.tag {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
  white-space: nowrap;
}
.tag-running { background: rgba(0, 255, 136, 0.15); color: #00ff88; }
.tag-stopped { background: rgba(255, 217, 61, 0.15); color: #ffd93d; }
.tag-fault { background: rgba(255, 107, 107, 0.15); color: #ff6b6b; }
</style>
