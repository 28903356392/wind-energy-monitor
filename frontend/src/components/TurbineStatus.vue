<template>
  <div class="turbine-list">
    <div
      v-for="t in turbines"
      :key="t.id"
      class="turbine-item"
      :class="'status-' + t.status"
      @click="$router.push(`/turbine/${t.id}`)"
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

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Turbine, TurbineStatusEnum } from '../types'
import { TurbineStatusLabel } from '../types'

const props = defineProps<{
  turbines: Turbine[]
}>()

const $router = useRouter()

function statusLabel(s: TurbineStatusEnum): string {
  return TurbineStatusLabel[s] || s
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
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.02);
  border-left: 3px solid transparent;
  transition: all var(--transition-fast);
  font-size: var(--text-xs);
  cursor: pointer;
}
.turbine-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-left-width: 5px;
}
.turbine-item.status-running { border-left-color: var(--color-success); }
.turbine-item.status-stopped { border-left-color: var(--color-warning); }
.turbine-item.status-maintenance { border-left-color: var(--color-primary); }
.turbine-item.status-fault { border-left-color: var(--color-danger); }

.item-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-running { background: var(--color-success); box-shadow: 0 0 6px rgba(0, 255, 136, 0.6); }
.dot-stopped { background: var(--color-warning); box-shadow: 0 0 6px rgba(255, 217, 61, 0.6); }
.dot-maintenance { background: var(--color-primary); box-shadow: 0 0 6px rgba(0, 212, 255, 0.6); }
.dot-fault { background: var(--color-danger); box-shadow: 0 0 6px rgba(255, 107, 107, 0.6); animation: blink 1s infinite; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.item-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.item-name { font-weight: 600; color: var(--text-primary); }
.item-status { font-size: 10px; color: var(--text-secondary); }

.item-power { text-align: right; font-family: 'Courier New', monospace; }
.power-val { font-weight: 700; color: var(--color-primary); font-size: var(--text-sm); }
.power-unit { font-size: 10px; color: var(--text-muted); }

.item-wind {
  width: 48px;
  text-align: right;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
  font-size: 11px;
}

.empty { text-align: center; padding: 20px; color: var(--text-muted); }
</style>
