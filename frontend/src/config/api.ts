/**
 * API 接口路径配置
 * ================
 * 集中管理所有后端 API 端点路径
 */

/** API 基础路径 */
export const API_BASE = '/api'

/** 请求超时时间（毫秒） */
export const REQUEST_TIMEOUT = 15000

/** 认证相关接口 */
export const AUTH = {
  LOGIN:     '/auth/login',
  USERINFO:  '/auth/userinfo',
  MENUS:     '/auth/menus',
}

/** 风电场数据接口 */
export const WIND_FARM = {
  OVERVIEW:    '/overview',
  TURBINES:    '/turbines',
  POWER_HISTORY: '/power/history',
  ALARMS:      '/alarms',
  ALARM_STATS: '/alarms/stats',
  EVENTS:      '/events',
  ENERGY_STATS:'/energy/stats',
}

/** 系统管理接口 */
export const SYSTEM = {
  USERS:         '/system/users',
  ROLES:         '/system/roles',
  MENUS:         '/system/menus',
  DICT_TYPES:    '/system/dict/types',
  DICT_DATA:     '/system/dict/data',
  LOGIN_LOGS:    '/system/logs/login',
  OPERATION_LOGS:'/system/logs/operation',
  MONITOR:       '/system/monitor',
}

/** 业务管理基础路径 */
export const BUSINESS_BASE = '/business'
