/* ============================================================
   useClock —— 时钟 composable
   高阶用法：ref + interval 自动清理 + 自定义格式化
   ============================================================ */
import { ref, onMounted, onBeforeUnmount } from 'vue'

export interface UseClockOptions {
  /** 日期时间格式，默认 'full' */
  format?: 'full' | 'time' | 'date'
  /** 更新间隔（毫秒），默认 1000 */
  interval?: number
}

/**
 * 响应式时钟 composable
 * @example const { time } = useClock({ format: 'time' })
 */
export function useClock(options: UseClockOptions = {}) {
  const { format = 'full', interval = 1000 } = options
  const time = ref('')

  function update() {
    const now = new Date()
    const locale = 'zh-CN'

    switch (format) {
      case 'time':
        time.value = now.toLocaleTimeString(locale, {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
        })
        break
      case 'date':
        time.value = now.toLocaleDateString(locale, {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
        })
        break
      default:
        time.value = now.toLocaleString(locale, {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
        })
    }
  }

  let timer: ReturnType<typeof setInterval> | null = null

  function start() {
    update()
    timer = setInterval(update, interval)
  }

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onMounted(start)
  onBeforeUnmount(stop)

  return { time, start, stop }
}
