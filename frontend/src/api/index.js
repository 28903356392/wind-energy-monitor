import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

/**
 * 获取风电场总览数据
 */
export function getOverview() {
  return api.get('/overview')
}

/**
 * 获取所有风机列表
 * @param {string} status - 可选筛选状态
 */
export function getTurbines(status) {
  const params = status ? { status } : {}
  return api.get('/turbines', { params })
}

/**
 * 获取单个风机详情
 * @param {number} id - 风机ID
 */
export function getTurbine(id) {
  return api.get(`/turbines/${id}`)
}

/**
 * 获取历史发电量数据
 * @param {number} hours - 过去几小时
 */
export function getPowerHistory(hours = 24) {
  return api.get('/power/history', { params: { hours } })
}

/**
 * 创建 WebSocket 连接
 * @param {function} onMessage - 消息回调
 * @returns {WebSocket}
 */
export function createWebSocket(onMessage) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host
  const ws = new WebSocket(`${protocol}//${host}/api/ws`)

  ws.onopen = () => {
    console.log('[WS] 连接已建立')
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (e) {
      console.warn('[WS] 数据解析失败:', e)
    }
  }

  ws.onerror = (err) => {
    console.error('[WS] 连接错误:', err)
  }

  ws.onclose = () => {
    console.log('[WS] 连接已关闭，3秒后重连...')
    setTimeout(() => {
      createWebSocket(onMessage)
    }, 3000)
  }

  // 心跳保活
  const heartbeat = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send('ping')
    }
  }, 25000)

  // 重写 close 以清理心跳
  const origClose = ws.close.bind(ws)
  ws.close = () => {
    clearInterval(heartbeat)
    origClose()
  }

  return ws
}
