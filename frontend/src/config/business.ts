/**
 * 业务模块资源配置
 * ================
 * 集中管理所有业务模块的资源名称和分组信息
 */

/** 单个业务模块配置 */
export interface BusinessModule {
  resource: string      // API 资源名
  label: string         // 中文名称
  group: string         // 所属分组
}

/** 业务模块列表 */
export const BUSINESS_MODULES: BusinessModule[] = [
  // 设备管理
  { resource: 'equipment-types',     label: '设备类型', group: '设备管理' },
  { resource: 'equipment-ledgers',   label: '设备台账', group: '设备管理' },
  { resource: 'maintenance-records', label: '设备维修', group: '设备管理' },
  // 运维管理
  { resource: 'inspection-plans',    label: '巡检计划', group: '运维管理' },
  { resource: 'inspection-records',  label: '巡检记录', group: '运维管理' },
  { resource: 'work-orders',         label: '工单管理', group: '运维管理' },
  { resource: 'spare-parts',         label: '备件管理', group: '运维管理' },
  { resource: 'part-transactions',   label: '备件出入库', group: '运维管理' },
  // 生产管理
  { resource: 'power-targets',       label: '发电量统计', group: '生产管理' },
  { resource: 'energy-settlements',  label: '电量结算',   group: '生产管理' },
  { resource: 'carbon-reductions',   label: '碳减排管理', group: '生产管理' },
  // 安全监控
  { resource: 'safety-inspections',  label: '安全巡检', group: '安全监控' },
  { resource: 'safety-hazards',      label: '安全隐患', group: '安全监控' },
  { resource: 'emergency-plans',     label: '应急预案', group: '安全监控' },
  { resource: 'emergency-drills',    label: '应急演练', group: '安全监控' },
  // 人员管理
  { resource: 'employees',           label: '员工信息',   group: '人员管理' },
  { resource: 'shift-schedules',     label: '排班管理',   group: '人员管理' },
  { resource: 'attendance-records',  label: '考勤记录',   group: '人员管理' },
  // 财务报表
  { resource: 'revenue-items',       label: '收入统计', group: '财务报表' },
  { resource: 'cost-items',          label: '成本分析', group: '财务报表' },
]

/** 业务分组列表 */
export const BUSINESS_GROUPS = [
  '设备管理', '运维管理', '生产管理',
  '安全监控', '人员管理', '财务报表',
] as const

/** 根据资源名获取模块标签 */
export function getModuleLabel(resource: string): string {
  return BUSINESS_MODULES.find(m => m.resource === resource)?.label || resource
}
