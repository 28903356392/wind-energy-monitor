/* ============================================================
   业务 API 模块 —— 按领域拆分，类型安全
   ============================================================ */
import { get } from './index'
import type {
  OverviewData,
  Turbine,
  PowerRecord,
  Alarm,
  EnergyStats,
  EventLog,
  ApiResponse,
} from '../types'

/* ---- 总览 ---- */
export function fetchOverview() {
  return get<OverviewData>('/overview')
}

/* ---- 风机 ---- */
export function fetchTurbines(status?: string) {
  const params = status ? { params: { status } } : undefined
  return get<Turbine[]>('/turbines', params)
}

export function fetchTurbineDetail(id: number) {
  return get<Turbine>(`/turbines/${id}`)
}

/* ---- 功率/历史 ---- */
export function fetchPowerHistory(hours = 24) {
  return get<PowerRecord[]>('/power/history', { params: { hours } })
}

/* ---- 告警 ---- */
export function fetchAlarms(params?: { level?: string; acknowledged?: boolean }) {
  return get<Alarm[]>('/alarms', { params })
}

export function fetchAlarmStats() {
  return get<{ total: number; critical: number; warning: number; info: number }>('/alarms/stats')
}

/* ---- 事件日志 ---- */
export function fetchEvents(limit = 50) {
  return get<EventLog[]>('/events', { params: { limit } })
}

/* ---- 风能统计 ---- */
export function fetchEnergyStats() {
  return get<EnergyStats>('/energy/stats')
}

/* ---- 仪表盘聚合数据（批量请求合并） ---- */
export async function fetchDashboardData() {
  const [overview, turbines, history] = await Promise.all([
    fetchOverview(),
    fetchTurbines(),
    fetchPowerHistory(24),
  ])
  return {
    overview: overview.data,
    turbines: turbines.data,
    powerHistory: history.data,
  }
}
