<template>
  <div class="panel" :class="[size, customClass]" :style="panelStyle">
    <div v-if="title" class="panel-header">
      <span class="panel-dot"></span>
      {{ title }}
      <slot name="header-right" />
    </div>
    <div class="panel-body" :class="{ 'no-scroll': noScroll }">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'full'
  noScroll?: boolean
  customClass?: string
  flex?: number
}>(), {
  size: 'md',
  noScroll: false,
  customClass: '',
  flex: 1,
})

const panelStyle = computed(() => ({
  flex: props.size === 'full' ? 'none' : props.flex,
}))
</script>

<style scoped>
.panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
  transition: border-color var(--transition-fast);
}
.panel:hover {
  border-color: rgba(0, 212, 255, 0.3);
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

.panel-dot {
  width: 8px;
  height: 8px;
  background: var(--color-primary);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.6);
}

.panel-body {
  flex: 1;
  padding: var(--space-md);
  overflow: auto;
  min-height: 0;
}
.panel-body.no-scroll {
  overflow: hidden;
}
</style>
