/* ============================================================
   TypeScript 类型定义 —— 高阶泛型 + 枚举 + 工具类型
   ============================================================ */

/* ---------- 通用 API 响应泛型 ---------- */
export interface ApiResponse<T = unknown> {
  code: number
  message?: string
  data: T
}

/* ---------- 分页泛型 ---------- */
export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

/* ---------- 风机状态枚举 ---------- */
export enum TurbineStatusEnum {
  RUNNING = 'running',
  STOPPED = 'stopped',
  MAINTENANCE = 'maintenance',
  FAULT = 'fault',
}

export const TurbineStatusLabel: Record<TurbineStatusEnum, string> = {
  [TurbineStatusEnum.RUNNING]: '运行中',
  [TurbineStatusEnum.STOPPED]: '已停机',
  [TurbineStatusEnum.MAINTENANCE]: '维护中',
  [TurbineStatusEnum.FAULT]: '故障',
}

/* ---------- 风机组数据类型 ---------- */
export interface Turbine {
  id: number
  name: string
  status: TurbineStatusEnum
  power_output: number
  wind_speed: number
  wind_direction: number
  rotor_speed: number
  temperature: number
  daily_energy: number
  total_energy: number
  updated_at: string
  /** 前端扩展：纬度 */
  latitude?: number
  /** 前端扩展：经度 */
  longitude?: number
}

/* ---------- 总览数据类型 ---------- */
export interface OverviewData {
  total_power: number
  total_daily_energy: number
  total_energy: number
  avg_wind_speed: number
  turbine_count: number
  running_count: number
  stopped_count: number
  maintenance_count: number
  fault_count: number
  updated_at: string
}

/* ---------- 功率历史记录 ---------- */
export interface PowerRecord {
  timestamp: string
  total_power: number
  avg_wind_speed: number
  energy_hourly: number
}

/* ---------- 告警级别枚举 ---------- */
export enum AlarmLevel {
  INFO = 'info',
  WARNING = 'warning',
  CRITICAL = 'critical',
}

export const AlarmLevelLabel: Record<AlarmLevel, string> = {
  [AlarmLevel.INFO]: '提示',
  [AlarmLevel.WARNING]: '警告',
  [AlarmLevel.CRITICAL]: '严重',
}

export const AlarmLevelColor: Record<AlarmLevel, string> = {
  [AlarmLevel.INFO]: 'var(--color-primary)',
  [AlarmLevel.WARNING]: 'var(--color-warning)',
  [AlarmLevel.CRITICAL]: 'var(--color-danger)',
}

/* ---------- 告警数据类型 ---------- */
export interface Alarm {
  id: number
  turbine_id: number
  turbine_name: string
  level: AlarmLevel
  message: string
  value: number
  threshold: number
  created_at: string
  acknowledged: boolean
}

/* ---------- 事件日志 ---------- */
export interface EventLog {
  id: number
  type: 'operation' | 'system' | 'alarm'
  message: string
  timestamp: string
  detail?: string
}

/* ---------- 风能统计 ---------- */
export interface EnergyStats {
  today: number
  yesterday: number
  this_week: number
  this_month: number
  last_month: number
  total: number
  efficiency: number
}

/* ---------- WebSocket 推送消息类型 ---------- */
export interface WsUpdateMessage {
  type: 'update'
  timestamp: string
  total_power: number
  turbines: Pick<Turbine, 'id' | 'name' | 'status' | 'power_output' | 'wind_speed'>[]
}

export interface WsAlarmMessage {
  type: 'alarm'
  alarm: Alarm
}

export type WsMessage = WsUpdateMessage | WsAlarmMessage

/* ---------- 工具类型：提取 Promise 返回值 ---------- */
export type PromiseReturnType<T extends (...args: any) => Promise<any>> =
  T extends (...args: any) => Promise<infer R> ? R : never
