/**
 * 应用全局配置
 * ============
 * 集中管理前端应用级别的常量和配置项
 */

/** 应用信息 */
export const APP = {
  NAME: '风能监控系统',
  SHORT_NAME: 'WindMonitor',
  VERSION: '1.0.0',
}

/** localStorage 存储键名 */
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
  LAYOUT_MODE: 'layoutMode',
}

/** 默认布局模式 */
export const DEFAULT_LAYOUT_MODE = 'left' as const

/** 布局模式选项 */
export const LAYOUT_MODES = {
  LEFT: 'left',
  TOP: 'top',
} as const

/** 登录页路由 */
export const LOGIN_PATH = '/login'

/** 默认首页路由 */
export const DEFAULT_HOME = '/dashboard'
