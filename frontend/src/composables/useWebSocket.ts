/* ============================================================
   useWebSocket —— WebSocket composable
   高阶用法：基于 WebSocketManager 的响应式封装
   - 自动连接/重连
   - 响应式连接状态
   - 组件卸载自动销毁
   ============================================================ */
import { ref, onBeforeUnmount } from 'vue'
import { WebSocketManager, type WsCallback } from '../api'
import type { WsMessage } from '../types'

/**
 * WebSocket 响应式封装
 * @param onMessage 消息回调
 */
export function useWebSocket(onMessage?: WsCallback) {
  const connected = ref(false)
  let manager: WebSocketManager | null = null

  function connect(callback?: WsCallback) {
    manager = new WebSocketManager({
      onMessage: (data: WsMessage) => {
        callback?.(data)
        onMessage?.(data)
      },
      onStatusChange: (status) => {
        connected.value = status
      },
    })
  }

  function disconnect() {
    manager?.destroy()
    manager = null
    connected.value = false
  }

  onBeforeUnmount(() => {
    disconnect()
  })

  return { connected, connect, disconnect }
}
