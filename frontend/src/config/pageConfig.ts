/**
 * 页面类型配置
 * ============
 * 集中管理前端页面类型映射和看板列定义
 */

/** 页面类型映射: 资源名 → table | kanban | dashboard */
export const PAGE_TYPE_MAP: Record<string, string> = {
  'work-orders':       'kanban',
  'safety-hazards':    'kanban',
  'power-targets':     'dashboard',
  'revenue-items':     'dashboard',
  'carbon-reductions': 'dashboard',
  'cost-items':        'dashboard',
}

/** 看板列定义 */
export const KANBAN_COLUMNS: Record<string, { status: string; label: string; tag: string }[]> = {
  'work-orders': [
    { status: 'pending',    label: '待处理', tag: 'info' },
    { status: 'processing', label: '处理中', tag: 'warning' },
    { status: 'reviewing',  label: '审核中', tag: 'primary' },
    { status: 'completed',  label: '已完成', tag: 'success' },
    { status: 'closed',     label: '已关闭', tag: '' },
  ],
  'safety-hazards': [
    { status: 'reported',   label: '已上报', tag: 'danger' },
    { status: 'rectifying', label: '整改中', tag: 'warning' },
    { status: 'reviewing',  label: '验收中', tag: 'primary' },
    { status: 'closed',     label: '已闭环', tag: 'success' },
  ],
}

/** 获取页面类型 */
export function getPageType(resource: string): string {
  return PAGE_TYPE_MAP[resource] || 'table'
}

/** 获取看板列定义 */
export function getKanbanColumns(resource: string) {
  return KANBAN_COLUMNS[resource] || []
}
