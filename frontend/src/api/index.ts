/* ============================================================
   API 封装层 —— 高阶用法：
   1. Axios 实例 + 请求/响应拦截器
   2. 泛型约束确保类型安全
   3. WebSocket 管理器封装
   4. 自动重连 + 心跳保活
   ============================================================ */
import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import type { ApiResponse, WsMessage } from '../types'

/* ---------- Axios 实例 ---------- */
const api: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

/* 响应拦截器：统一解包 code/data */
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err.response?.data?.message || err.message || '网络错误'
    console.error(`[API Error] ${msg}`)
    return Promise.reject(err)
  }
)

/* ---------- 泛型请求方法 ---------- */
export async function get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  const res = await api.get<ApiResponse<T>>(url, config)
  return res.data
}

export async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  const res = await api.post<ApiResponse<T>>(url, data, config)
  return res.data
}

export async function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  const res = await api.put<ApiResponse<T>>(url, data, config)
  return res.data
}

export async function del<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  const res = await api.delete<ApiResponse<T>>(url, config)
  return res.data
}

export default api

/* ---------- WebSocket 管理器（类封装 + 事件驱动） ---------- */
export type WsCallback = (data: WsMessage) => void

export class WebSocketManager {
  private ws: WebSocket | null = null
  private url: string
  private onMessage: WsCallback
  private onStatusChange?: (connected: boolean) => void
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private destroyed = false

  constructor(options: {
    onMessage: WsCallback
    onStatusChange?: (connected: boolean) => void
  }) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    this.url = `${protocol}//${window.location.host}/api/ws`
    this.onMessage = options.onMessage
    this.onStatusChange = options.onStatusChange
    this.connect()
  }

  private connect() {
    if (this.destroyed) return
    this.ws = new WebSocket(this.url)

    this.ws.onopen = () => {
      console.log('[WS] 连接已建立')
      this.onStatusChange?.(true)
      this.startHeartbeat()
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WsMessage
        this.onMessage(data)
      } catch (e) {
        console.warn('[WS] 数据解析失败:', e)
      }
    }

    this.ws.onerror = () => {
      this.onStatusChange?.(false)
    }

    this.ws.onclose = () => {
      this.onStatusChange?.(false)
      this.stopHeartbeat()
      if (!this.destroyed) {
        console.log('[WS] 连接已关闭，3秒后重连...')
        this.reconnectTimer = setTimeout(() => this.connect(), 3000)
      }
    }
  }

  private startHeartbeat() {
    this.stopHeartbeat()
    this.heartbeatTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send('ping')
      }
    }, 25000)
  }

  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }

  destroy() {
    this.destroyed = true
    this.stopHeartbeat()
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    this.ws?.close()
    this.ws = null
  }
}
