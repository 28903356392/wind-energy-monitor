/** 业务模块 API（TypeScript 类型安全） */
import request from '../utils/request.js'
import type { ApiResponse, PageResponse } from '../types/business'

const BASE = '/business'

/** 通用 CRUD API 工厂 */
export function createBusinessApi<T = any>(resource: string) {
  const url = `${BASE}/${resource}`

  return {
    /** 列表查询（支持关键词搜索 + 多字段筛选） */
    async list(params: {
      page?: number
      size?: number
      keyword?: string
      turbine_id?: number
      type_id?: number
      employee_id?: number
      plan_id?: number
      part_id?: number
      equipment_id?: number
      year?: number
      month?: number
      status?: string
      level?: string
      priority?: string
      result?: string
      category?: string
      sort_field?: string
      sort_order?: string
    } = {}): Promise<PageResponse<T>> {
      const res = await request.get(`${url}`, { params })
      return res.data.data
    },

    /** 获取详情 */
    async get(id: number): Promise<T> {
      const res = await request.get(`${url}/${id}`)
      return res.data.data
    },

    /** 新增 */
    async create(data: Partial<T>): Promise<{ id: number }> {
      const res = await request.post(`${url}`, data)
      return res.data.data
    },

    /** 更新 */
    async update(id: number, data: Partial<T>): Promise<void> {
      await request.put(`${url}/${id}`, data)
    },

    /** 删除 */
    async del(id: number): Promise<void> {
      await request.delete(`${url}/${id}`)
    },

    /** 按风机筛选 */
    async listByTurbine(turbine_id: number, params: { page?: number; size?: number } = {}): Promise<PageResponse<T>> {
      const res = await request.get(`${BASE}/by-turbine/${resource}`, { params: { ...params, turbine_id } })
      return res.data.data
    },

    /** 按员工筛选 */
    async listByEmployee(employee_id: number, params: { page?: number; size?: number } = {}): Promise<PageResponse<T>> {
      const res = await request.get(`${BASE}/by-employee/${resource}`, { params: { ...params, employee_id } })
      return res.data.data
    },

    /** 获取统计 */
    async stats(): Promise<Record<string, any>> {
      const res = await request.get(`${url}/stats`)
      return res.data.data
    },
  }
}

// ========== 导出所有业务模块 API ==========

export const equipmentTypeApi = createBusinessApi('equipment-types')
export const equipmentLedgerApi = createBusinessApi('equipment-ledgers')
export const maintenanceRecordApi = createBusinessApi('maintenance-records')
export const inspectionPlanApi = createBusinessApi('inspection-plans')
export const inspectionRecordApi = createBusinessApi('inspection-records')
export const workOrderApi = createBusinessApi('work-orders')
export const sparePartApi = createBusinessApi('spare-parts')
export const partTransactionApi = createBusinessApi('part-transactions')
export const powerTargetApi = createBusinessApi('power-targets')
export const energySettlementApi = createBusinessApi('energy-settlements')
export const carbonReductionApi = createBusinessApi('carbon-reductions')
export const safetyInspectionApi = createBusinessApi('safety-inspections')
export const safetyHazardApi = createBusinessApi('safety-hazards')
export const emergencyPlanApi = createBusinessApi('emergency-plans')
export const emergencyDrillApi = createBusinessApi('emergency-drills')
export const employeeApi = createBusinessApi('employees')
export const shiftScheduleApi = createBusinessApi('shift-schedules')
export const attendanceRecordApi = createBusinessApi('attendance-records')
export const revenueItemApi = createBusinessApi('revenue-items')
export const costItemApi = createBusinessApi('cost-items')
