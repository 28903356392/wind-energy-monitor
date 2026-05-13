<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as echarts from 'echarts'
import { useECharts } from '../composables/useECharts'
import type { PowerRecord } from '../types'

const props = defineProps<{
  history: PowerRecord[]
  realtimeTotal?: number
}>()

const chartOption = computed<echarts.EChartsOption | null>(() => {
  if (!props.history.length) return null

  const data = props.history.slice(-60)
  const timestamps = data.map((d) => {
    const t = new Date(d.timestamp)
    return `${String(t.getHours()).padStart(2, '0')}:${String(t.getMinutes()).padStart(2, '0')}`
  })
  const powerData = data.map((d) => d.total_power)
  const windData = data.map((d) => d.avg_wind_speed)

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(2, 13, 31, 0.85)',
      borderColor: 'rgba(0, 212, 255, 0.3)',
      textStyle: { color: '#e0e6ed', fontSize: 11 },
    },
    legend: {
      data: ['总功率', '平均风速'],
      textStyle: { color: 'rgba(255,255,255,0.5)', fontSize: 10 },
      top: 0,
      right: 0,
      icon: 'roundRect',
      itemWidth: 12,
      itemHeight: 4,
    },
    grid: { left: 40, right: 20, top: 26, bottom: 20 },
    xAxis: {
      type: 'category',
      data: timestamps,
      axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.15)' } },
      axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 9, interval: 'auto' },
      splitLine: { show: false },
    },
    yAxis: [
      {
        type: 'value',
        name: 'kW',
        nameTextStyle: { color: 'rgba(255,255,255,0.3)', fontSize: 9 },
        axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 9 },
        splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.06)', type: 'dashed' } },
      },
      {
        type: 'value',
        name: 'm/s',
        nameTextStyle: { color: 'rgba(255,255,255,0.3)', fontSize: 9 },
        axisLabel: { color: 'rgba(255,255,255,0.3)', fontSize: 9 },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: '总功率',
        type: 'line',
        data: powerData,
        smooth: true,
        symbol: 'none',
        lineStyle: {
          width: 2,
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: '#00d4ff' },
              { offset: 1, color: '#00ff88' },
            ],
          },
        },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 212, 255, 0.25)' },
              { offset: 1, color: 'rgba(0, 212, 255, 0.02)' },
            ],
          },
        },
      },
      {
        name: '平均风速',
        type: 'line',
        yAxisIndex: 1,
        data: windData,
        smooth: true,
        symbol: 'none',
        lineStyle: { width: 1.5, color: 'rgba(255, 217, 61, 0.6)' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(255, 217, 61, 0.12)' },
              { offset: 1, color: 'rgba(255, 217, 61, 0.01)' },
            ],
          },
        },
      },
    ],
  } as echarts.EChartsOption
})

const { chartRef } = useECharts(chartOption)
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style>
