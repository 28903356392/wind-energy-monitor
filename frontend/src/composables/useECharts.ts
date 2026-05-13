/* ============================================================
   useECharts —— ECharts 图表 composable （高阶封装）
   功能：
   - 自动初始化、销毁
   - 自适应 resize (ResizeObserver)
   - 响应式数据监听更新
   - 暗色主题统一配置
   ============================================================ */
import { ref, onMounted, onBeforeUnmount, watch, type Ref, type WatchSource } from 'vue'
import * as echarts from 'echarts'

export interface UseEChartsOptions {
  /** 图表主题，默认 'dark' */
  theme?: string
  /** 是否自适应 resize，默认 true */
  autoResize?: boolean
}

/**
 * ECharts 组合式封装
 * @param optionRef 响应式图表配置
 * @param options 额外选项
 */
export function useECharts(
  optionRef: WatchSource<echarts.EChartsOption | null | undefined>,
  options: UseEChartsOptions = {}
) {
  const { theme = 'dark', autoResize = true } = options
  const chartRef: Ref<HTMLDivElement | null> = ref(null)
  let chart: echarts.ECharts | null = null
  let observer: ResizeObserver | null = null

  /** 初始化图表 */
  function init() {
    if (!chartRef.value || chart) return
    chart = echarts.init(chartRef.value, theme)
    if (autoResize) {
      observer = new ResizeObserver(() => chart?.resize())
      observer.observe(chartRef.value)
    }
  }

  /** 更新图表配置 */
  function update(option: echarts.EChartsOption | null | undefined) {
    if (!chart || !option) return
    chart.setOption(option, true)
  }

  /** 销毁 */
  function dispose() {
    observer?.disconnect()
    observer = null
    chart?.dispose()
    chart = null
  }

  onMounted(init)
  onBeforeUnmount(dispose)

  // 监听配置变化自动更新
  if (typeof optionRef === 'function') {
    watch(optionRef as () => echarts.EChartsOption | null | undefined, update, { deep: true, immediate: false })
  } else {
    watch(optionRef as Ref<echarts.EChartsOption | null | undefined>, update, { deep: true, immediate: false })
  }

  return { chartRef, chart, init, update, dispose }
}
