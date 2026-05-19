/** 业务模块 - TypeScript 类型定义 */

// ========== 设备管理 ==========

/** 设备类型 */
export interface EquipmentType {
  id: number
  name: string
  code: string
  category: string
  description: string
  status: boolean
  sort: number
  created_at: string
}

/** 设备台账 */
export interface EquipmentLedger {
  id: number
  name: string
  code: string
  type_id: number
  type_name: string
  turbine_id: number
  turbine_name: string
  model: string
  manufacturer: string
  install_date: string
  warranty_expire: string
  status: 'normal' | 'fault' | 'maintenance' | 'scrap'
  description: string
  created_at: string
}

/** 设备维修记录 */
export interface MaintenanceRecord {
  id: number
  equipment_id: number
  equipment_name: string
  turbine_id: number
  turbine_name: string
  fault_description: string
  fault_type: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  repair_content: string
  repair_person: string
  repair_cost: number
  start_time: string
  end_time: string
  status: 'pending' | 'processing' | 'completed' | 'cancelled'
  created_at: string
}

// ========== 运维管理 ==========

/** 巡检计划 */
export interface InspectionPlan {
  id: number
  name: string
  turbine_ids: number[]
  turbine_names: string[]
  cycle: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly'
  content: string
  responsible_person: string
  start_date: string
  end_date: string
  status: boolean
  created_at: string
}

/** 巡检记录 */
export interface InspectionRecord {
  id: number
  plan_id: number
  plan_name: string
  turbine_id: number
  turbine_name: string
  inspector: string
  check_time: string
  items: string
  result: 'normal' | 'abnormal' | 'fault'
  description: string
  attachments: string
  created_at: string
}

/** 工单 */
export interface WorkOrder {
  id: number
  order_no: string
  title: string
  type: 'repair' | 'inspection' | 'install' | 'other'
  turbine_id: number
  turbine_name: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  description: string
  assignee: string
  deadline: string
  progress: number
  status: 'pending' | 'processing' | 'reviewing' | 'completed' | 'closed'
  result: string
  created_at: string
}

/** 备件 */
export interface SparePart {
  id: number
  name: string
  code: string
  model: string
  category: string
  manufacturer: string
  unit: string
  price: number
  stock: number
  min_stock: number
  max_stock: number
  location: string
  status: boolean
  created_at: string
}

/** 备件出入库 */
export interface PartTransaction {
  id: number
  part_id: number
  part_name: string
  type: 'in' | 'out'
  quantity: number
  before_stock: number
  after_stock: number
  operator: string
  source: string
  remark: string
  created_at: string
}

// ========== 生产管理 ==========

/** 发电指标 */
export interface PowerTarget {
  id: number
  year: number
  month: number
  target_kwh: number
  actual_kwh: number
  completion_rate: number
  status: 'pending' | 'completed' | 'exceeded' | 'failed'
  remark: string
  created_at: string
}

/** 电量结算 */
export interface EnergySettlement {
  id: number
  settlement_no: string
  period: string
  total_kwh: number
  price_per_kwh: number
  total_amount: number
  tax_rate: number
  tax_amount: number
  final_amount: number
  customer: string
  status: 'draft' | 'confirmed' | 'paid' | 'cancelled'
  remark: string
  created_at: string
}

/** 碳减排管理 */
export interface CarbonReduction {
  id: number
  year: number
  month: number
  energy_kwh: number
  reduction_co2: number
  reduction_so2: number
  reduction_nox: number
  reduction_dust: number
  standard_coal_saved: number
  trees_equivalent: number
  remark: string
  created_at: string
}

// ========== 安全监控 ==========

/** 安全巡检 */
export interface SafetyInspection {
  id: number
  title: string
  area: string
  inspector: string
  check_time: string
  items: string
  result: 'normal' | 'abnormal' | 'danger'
  description: string
  rectification: string
  status: 'pending' | 'processing' | 'completed'
  created_at: string
}

/** 安全隐患 */
export interface SafetyHazard {
  id: number
  title: string
  level: 'low' | 'medium' | 'high' | 'critical'
  area: string
  source: string
  description: string
  measures: string
  responsible_person: string
  deadline: string
  status: 'reported' | 'rectifying' | 'reviewing' | 'closed'
  rectification_result: string
  reviewer: string
  review_time: string
  created_at: string
}

/** 应急预案 */
export interface EmergencyPlan {
  id: number
  name: string
  type: 'fire' | 'typhoon' | 'earthquake' | 'equipment' | 'power_outage' | 'other'
  level: 'company' | 'department' | 'team'
  content: string
  procedures: string
  responsible_person: string
  team_members: string
  drill_cycle: string
  status: boolean
  created_at: string
}

/** 应急演练 */
export interface EmergencyDrill {
  id: number
  plan_id: number
  plan_name: string
  name: string
  drill_time: string
  location: string
  participants: number
  content: string
  evaluation: string
  problems: string
  improvements: string
  status: 'planned' | 'completed' | 'cancelled'
  created_at: string
}

// ========== 人员管理 ==========

/** 员工信息 */
export interface Employee {
  id: number
  employee_no: string
  name: string
  gender: 'male' | 'female'
  phone: string
  email: string
  department: string
  position: string
  entry_date: string
  status: 'active' | 'leave' | 'resigned'
  remark: string
  created_at: string
}

/** 排班管理 */
export interface ShiftSchedule {
  id: number
  employee_id: number
  employee_name: string
  date: string
  shift_type: 'day' | 'night' | 'off' | 'oncall'
  start_time: string
  end_time: string
  remark: string
  created_at: string
}

/** 考勤记录 */
export interface AttendanceRecord {
  id: number
  employee_id: number
  employee_name: string
  date: string
  check_in: string
  check_out: string
  status: 'normal' | 'late' | 'early' | 'absent' | 'overtime'
  work_hours: number
  overtime_hours: number
  remark: string
  created_at: string
}

// ========== 财务报表 ==========

/** 收入统计行 */
export interface RevenueItem {
  id: number
  year: number
  month: number
  energy_revenue: number
  subsidy_revenue: number
  carbon_revenue: number
  other_revenue: number
  total_revenue: number
  created_at: string
}

/** 成本分析行 */
export interface CostItem {
  id: number
  year: number
  month: number
  category: string
  amount: number
  description: string
  created_at: string
}

// ========== 通用分页响应 ==========

export interface PageResponse<T> {
  total: number
  list: T[]
}

export interface ApiResponse<T> {
  code: number
  data: T
  message?: string
}
