<template>
  <div class="turbine-list">
    <div
      v-for="t in turbines"
      :key="t.id"
      class="turbine-item"
      :class="'status-' + t.status"
    >
      <div class="item-dot" :class="'dot-' + t.status"></div>
      <div class="item-info">
        <span class="item-name">{{ t.name }}</span>
        <span class="item-status">{{ statusLabel(t.status) }}</span>
      </div>
      <div class="item-power">
        <span class="power-val">{{ t.power_output?.toFixed(1) }}</span>
        <span class="power-unit">kW</span>
      </div>
      <div class="item-wind">{{ t.wind_speed?.toFixed(1) }}m/s</div>
    </div>
    <div v-if="!turbines.length" class="empty">暂无数据</div>
  </div>
</template>

<script setup>
defineProps({
  turbines: { type: Array, default: () => [] }
})

function statusLabel(s) {
  const map = {
    running: '运行中',
    stopped: '已停机',
    maintenance: '维护中',
    fault: '故障'
  }
  return map[s] || s
}
</script>

<style scoped>
.turbine-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.turbine-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.02);
  border-left: 3px solid transparent;
  transition: all 0.3s;
  font-size: 12px;
}

.turbine-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.turbine-item.status-running { border-left-color: #00ff88; }
.turbine-item.status-stopped { border-left-color: #ffd93d; }
.turbine-item.status-maintenance { border-left-color: #00d4ff; }
.turbine-item.status-fault { border-left-color: #ff6b6b; }

.item-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-running { background: #00ff88; box-shadow: 0 0 6px rgba(0, 255, 136, 0.6); }
.dot-stopped { background: #ffd93d; box-shadow: 0 0 6px rgba(255, 217, 61, 0.6); }
.dot-maintenance { background: #00d4ff; box-shadow: 0 0 6px rgba(0, 212, 255, 0.6); }
.dot-fault { background: #ff6b6b; box-shadow: 0 0 6px rgba(255, 107, 107, 0.6); animation: blink 1s infinite; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.item-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.item-name { font-weight: 600; color: #e0e6ed; }
.item-status { font-size: 10px; color: rgba(255,255,255,0.4); }

.item-power {
  text-align: right;
  font-family: 'Courier New', monospace;
}
.power-val { font-weight: 700; color: #00d4ff; font-size: 13px; }
.power-unit { font-size: 10px; color: rgba(255,255,255,0.3); }

.item-wind {
  width: 48px;
  text-align: right;
  color: rgba(255,255,255,0.5);
  font-family: 'Courier New', monospace;
  font-size: 11px;
}

.empty {
  text-align: center;
  padding: 20px;
  color: rgba(255,255,255,0.3);
}
</style>
