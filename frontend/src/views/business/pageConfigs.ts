/** 业务页面配置（TypeScript 类型约束） */
import type { CrudColumn, CrudField } from './BusinessCrud.vue'
import * as api from '../../api/business'

export interface PageConfig {
  title: string
  api: any
  columns: CrudColumn[]
  formFields: CrudField[]
  searchable?: boolean
  showDetail?: boolean
}

/**
 * 生成状态标签
 */
function statusTag(value: string, map: Record<string, string>): string {
  const colorMap: Record<string, string> = {
    normal: 'success', active: 'success', completed: 'success', passed: 'success',
    pending: 'warning', processing: 'warning', reviewing: 'warning',
    fault: 'danger', urgent: 'danger', critical: 'danger', danger: 'danger',
    scrap: 'info', cancelled: 'info', resigned: 'info',
    draft: 'info', reported: 'warning', rectifying: 'warning',
  }
  return `<el-tag size="small" type="${colorMap[value] || 'info'}">${map[value] || value}</el-tag>`
}

function fmtTag(map: Record<string, string>) {
  return (_row: any, _col: any, val: string) => statusTag(val, map)
}

// ========== 页面配置 ==========

export const PAGE_CONFIGS: Record<string, PageConfig> = {

  // ---- 设备管理 ----
  'equipment-types': {
    title: '设备类型',
    api: api.equipmentTypeApi,
    columns: [
      { prop: 'name', label: '类型名称', width: 150 },
      { prop: 'code', label: '编码', width: 120 },
      { prop: 'category', label: '设备大类', width: 120 },
      { prop: 'status', label: '状态', width: 80, formatter: fmtTag({ True: '启用', False: '停用' }) },
      { prop: 'sort', label: '排序', width: 70 },
      { prop: 'description', label: '描述', minWidth: 200 },
    ],
    formFields: [
      { prop: 'name', label: '类型名称', rules: [{ required: true, message: '必填' }] },
      { prop: 'code', label: '编码', rules: [{ required: true, message: '必填' }] },
      { prop: 'category', label: '设备大类' },
      { prop: 'sort', label: '排序', type: 'number' },
      { prop: 'status', label: '启用', type: 'switch' },
      { prop: 'description', label: '描述', type: 'textarea' },
    ],
  },

  'equipment-ledgers': {
    title: '设备台账',
    api: api.equipmentLedgerApi,
    columns: [
      { prop: 'name', label: '设备名称', width: 150 },
      { prop: 'code', label: '编号', width: 120 },
      { prop: 'type_name', label: '类型', width: 100 },
      { prop: 'turbine_name', label: '关联风机', width: 100 },
      { prop: 'model', label: '型号', width: 120 },
      { prop: 'manufacturer', label: '制造商', width: 130 },
      { prop: 'status', label: '状态', width: 80, formatter: fmtTag({
        normal: '正常', fault: '故障', maintenance: '维护', scrap: '报废'
      }) },
      { prop: 'install_date', label: '安装日期', width: 110 },
    ],
    formFields: [
      { prop: 'name', label: '设备名称', rules: [{ required: true, message: '必填' }] },
      { prop: 'code', label: '编号', rules: [{ required: true, message: '必填' }] },
      { prop: 'type_name', label: '设备类型' },
      { prop: 'turbine_name', label: '关联风机' },
      { prop: 'model', label: '型号' },
      { prop: 'manufacturer', label: '制造商' },
      { prop: 'install_date', label: '安装日期' },
      { prop: 'warranty_expire', label: '保修到期' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '正常', value: 'normal' },
          { label: '故障', value: 'fault' },
          { label: '维护', value: 'maintenance' },
          { label: '报废', value: 'scrap' },
        ],
      },
      { prop: 'description', label: '备注', type: 'textarea' },
    ],
  },

  'maintenance-records': {
    title: '设备维修',
    api: api.maintenanceRecordApi,
    columns: [
      { prop: 'equipment_name', label: '设备名称', width: 130 },
      { prop: 'turbine_name', label: '风机', width: 100 },
      { prop: 'fault_type', label: '故障类型', width: 100 },
      { prop: 'priority', label: '优先级', width: 80, formatter: fmtTag({
        low: '低', medium: '中', high: '高', urgent: '紧急'
      }) },
      { prop: 'repair_person', label: '维修人', width: 90 },
      { prop: 'repair_cost', label: '费用', width: 90 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        pending: '待维修', processing: '维修中', completed: '已完成', cancelled: '已取消'
      }) },
      { prop: 'start_time', label: '开始时间', width: 110 },
    ],
    formFields: [
      { prop: 'equipment_name', label: '设备名称' },
      { prop: 'fault_type', label: '故障类型' },
      {
        prop: 'priority', label: '优先级', type: 'select',
        options: [
          { label: '低', value: 'low' }, { label: '中', value: 'medium' },
          { label: '高', value: 'high' }, { label: '紧急', value: 'urgent' },
        ],
      },
      { prop: 'fault_description', label: '故障描述', type: 'textarea' },
      { prop: 'repair_content', label: '维修内容', type: 'textarea' },
      { prop: 'repair_person', label: '维修人' },
      { prop: 'repair_cost', label: '维修费用', type: 'number' },
      { prop: 'start_time', label: '开始时间' },
      { prop: 'end_time', label: '结束时间' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '待维修', value: 'pending' },
          { label: '维修中', value: 'processing' },
          { label: '已完成', value: 'completed' },
          { label: '已取消', value: 'cancelled' },
        ],
      },
    ],
  },

  // ---- 运维管理 ----
  'inspection-plans': {
    title: '巡检计划',
    api: api.inspectionPlanApi,
    columns: [
      { prop: 'name', label: '计划名称', width: 180 },
      { prop: 'cycle', label: '周期', width: 80, formatter: fmtTag({
        daily: '每日', weekly: '每周', monthly: '每月', quarterly: '每季', yearly: '每年'
      }) },
      { prop: 'responsible_person', label: '负责人', width: 90 },
      { prop: 'start_date', label: '开始日期', width: 110 },
      { prop: 'end_date', label: '结束日期', width: 110 },
      { prop: 'status', label: '启用', width: 70, formatter: fmtTag({ True: '是', False: '否' }) },
    ],
    formFields: [
      { prop: 'name', label: '计划名称', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'cycle', label: '周期', type: 'select',
        options: [
          { label: '每日', value: 'daily' }, { label: '每周', value: 'weekly' },
          { label: '每月', value: 'monthly' }, { label: '每季', value: 'quarterly' },
          { label: '每年', value: 'yearly' },
        ],
      },
      { prop: 'responsible_person', label: '负责人' },
      { prop: 'start_date', label: '开始日期' },
      { prop: 'end_date', label: '结束日期' },
      { prop: 'content', label: '巡检内容', type: 'textarea' },
      { prop: 'status', label: '启用', type: 'switch' },
    ],
  },

  'inspection-records': {
    title: '巡检记录',
    api: api.inspectionRecordApi,
    columns: [
      { prop: 'plan_name', label: '计划', width: 140 },
      { prop: 'turbine_name', label: '风机', width: 100 },
      { prop: 'inspector', label: '巡检人', width: 90 },
      { prop: 'check_time', label: '巡检时间', width: 110 },
      { prop: 'result', label: '结果', width: 80, formatter: fmtTag({
        normal: '正常', abnormal: '异常', fault: '故障'
      }) },
    ],
    formFields: [
      { prop: 'plan_name', label: '计划名称' },
      { prop: 'turbine_name', label: '风机' },
      { prop: 'inspector', label: '巡检人' },
      { prop: 'check_time', label: '巡检时间' },
      {
        prop: 'result', label: '结果', type: 'select',
        options: [
          { label: '正常', value: 'normal' },
          { label: '异常', value: 'abnormal' },
          { label: '故障', value: 'fault' },
        ],
      },
      { prop: 'description', label: '说明', type: 'textarea' },
    ],
  },

  'work-orders': {
    title: '工单管理',
    api: api.workOrderApi,
    columns: [
      { prop: 'order_no', label: '工单编号', width: 140 },
      { prop: 'title', label: '标题', minWidth: 160 },
      { prop: 'turbine_name', label: '风机', width: 100 },
      { prop: 'type', label: '类型', width: 80, formatter: fmtTag({
        repair: '维修', inspection: '巡检', install: '安装', other: '其他'
      }) },
      { prop: 'priority', label: '优先级', width: 80, formatter: fmtTag({
        low: '低', medium: '中', high: '高', urgent: '紧急'
      }) },
      { prop: 'assignee', label: '指派人', width: 90 },
      { prop: 'progress', label: '进度', width: 80 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        pending: '待处理', processing: '处理中', reviewing: '审核中',
        completed: '已完成', closed: '已关闭'
      }) },
    ],
    formFields: [
      { prop: 'order_no', label: '工单编号' },
      { prop: 'title', label: '标题', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'type', label: '类型', type: 'select',
        options: [
          { label: '维修', value: 'repair' }, { label: '巡检', value: 'inspection' },
          { label: '安装', value: 'install' }, { label: '其他', value: 'other' },
        ],
      },
      {
        prop: 'priority', label: '优先级', type: 'select',
        options: [
          { label: '低', value: 'low' }, { label: '中', value: 'medium' },
          { label: '高', value: 'high' }, { label: '紧急', value: 'urgent' },
        ],
      },
      { prop: 'assignee', label: '指派人' },
      { prop: 'deadline', label: '截止日期' },
      { prop: 'description', label: '描述', type: 'textarea' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '待处理', value: 'pending' }, { label: '处理中', value: 'processing' },
          { label: '审核中', value: 'reviewing' }, { label: '已完成', value: 'completed' },
          { label: '已关闭', value: 'closed' },
        ],
      },
      { prop: 'progress', label: '进度(0-100)', type: 'number' },
    ],
  },

  'spare-parts': {
    title: '备件管理',
    api: api.sparePartApi,
    columns: [
      { prop: 'name', label: '备件名称', width: 140 },
      { prop: 'code', label: '编码', width: 110 },
      { prop: 'model', label: '型号', width: 120 },
      { prop: 'category', label: '分类', width: 100 },
      { prop: 'stock', label: '库存', width: 80 },
      { prop: 'min_stock', label: '最低库存', width: 90 },
      { prop: 'price', label: '单价', width: 90 },
      { prop: 'unit', label: '单位', width: 60 },
      { prop: 'location', label: '位置', width: 120 },
    ],
    formFields: [
      { prop: 'name', label: '备件名称', rules: [{ required: true, message: '必填' }] },
      { prop: 'code', label: '编码', rules: [{ required: true, message: '必填' }] },
      { prop: 'model', label: '型号' },
      { prop: 'category', label: '分类' },
      { prop: 'manufacturer', label: '制造商' },
      { prop: 'unit', label: '单位' },
      { prop: 'price', label: '单价', type: 'number' },
      { prop: 'stock', label: '库存数量', type: 'number' },
      { prop: 'min_stock', label: '最低库存', type: 'number' },
      { prop: 'max_stock', label: '最高库存', type: 'number' },
      { prop: 'location', label: '存放位置' },
      { prop: 'status', label: '启用', type: 'switch' },
    ],
  },

  'part-transactions': {
    title: '备件出入库',
    api: api.partTransactionApi,
    columns: [
      { prop: 'part_name', label: '备件名称', width: 130 },
      { prop: 'type', label: '类型', width: 80, formatter: fmtTag({ in: '入库', out: '出库' }) },
      { prop: 'quantity', label: '数量', width: 70 },
      { prop: 'before_stock', label: '操作前库存', width: 100 },
      { prop: 'after_stock', label: '操作后库存', width: 100 },
      { prop: 'operator', label: '操作人', width: 90 },
      { prop: 'source', label: '来源/去向', minWidth: 120 },
    ],
    formFields: [
      { prop: 'part_name', label: '备件名称', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'type', label: '类型', type: 'select',
        options: [
          { label: '入库', value: 'in' },
          { label: '出库', value: 'out' },
        ],
      },
      { prop: 'quantity', label: '数量', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'operator', label: '操作人' },
      { prop: 'source', label: '来源/去向' },
      { prop: 'remark', label: '备注', type: 'textarea' },
    ],
  },

  // ---- 生产管理 ----
  'power-targets': {
    title: '发电指标',
    api: api.powerTargetApi,
    columns: [
      { prop: 'year', label: '年份', width: 70 },
      { prop: 'month', label: '月份', width: 70 },
      { prop: 'target_kwh', label: '目标电量', width: 110 },
      { prop: 'actual_kwh', label: '实际电量', width: 110 },
      { prop: 'completion_rate', label: '完成率', width: 90, formatter: (r, c, v) => v ? (v * 100).toFixed(1) + '%' : '0%' },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        pending: '待完成', completed: '已完成', exceeded: '超额', failed: '未达标'
      }) },
    ],
    formFields: [
      { prop: 'year', label: '年份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'month', label: '月份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'target_kwh', label: '目标电量', type: 'number' },
      { prop: 'actual_kwh', label: '实际电量', type: 'number' },
    ],
  },

  'energy-settlements': {
    title: '电量结算',
    api: api.energySettlementApi,
    columns: [
      { prop: 'settlement_no', label: '结算单号', width: 150 },
      { prop: 'period', label: '结算周期', width: 110 },
      { prop: 'total_kwh', label: '总电量', width: 100 },
      { prop: 'price_per_kwh', label: '单价', width: 90 },
      { prop: 'final_amount', label: '实付金额', width: 110 },
      { prop: 'customer', label: '客户', width: 120 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        draft: '草稿', confirmed: '已确认', paid: '已付款', cancelled: '已取消'
      }) },
    ],
    formFields: [
      { prop: 'settlement_no', label: '结算单号', rules: [{ required: true, message: '必填' }] },
      { prop: 'period', label: '结算周期', rules: [{ required: true, message: '必填' }] },
      { prop: 'total_kwh', label: '总电量', type: 'number' },
      { prop: 'price_per_kwh', label: '单价', type: 'number' },
      { prop: 'final_amount', label: '实付金额', type: 'number' },
      { prop: 'customer', label: '客户' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '草稿', value: 'draft' }, { label: '已确认', value: 'confirmed' },
          { label: '已付款', value: 'paid' }, { label: '已取消', value: 'cancelled' },
        ],
      },
    ],
  },

  'carbon-reductions': {
    title: '碳减排管理',
    api: api.carbonReductionApi,
    columns: [
      { prop: 'year', label: '年份', width: 70 },
      { prop: 'month', label: '月份', width: 70 },
      { prop: 'energy_kwh', label: '发电量(kWh)', width: 110 },
      { prop: 'reduction_co2', label: 'CO₂减排(kg)', width: 120 },
      { prop: 'standard_coal_saved', label: '节约标准煤(kg)', width: 130 },
      { prop: 'trees_equivalent', label: '等效植树(棵)', width: 110 },
    ],
    formFields: [
      { prop: 'year', label: '年份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'month', label: '月份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'energy_kwh', label: '发电量', type: 'number' },
      { prop: 'reduction_co2', label: 'CO₂减排', type: 'number' },
      { prop: 'standard_coal_saved', label: '节约标准煤', type: 'number' },
    ],
  },

  // ---- 安全监控 ----
  'safety-inspections': {
    title: '安全巡检',
    api: api.safetyInspectionApi,
    columns: [
      { prop: 'title', label: '巡查标题', width: 180 },
      { prop: 'area', label: '区域', width: 100 },
      { prop: 'inspector', label: '巡查人', width: 90 },
      { prop: 'check_time', label: '巡查时间', width: 110 },
      { prop: 'result', label: '结果', width: 80, formatter: fmtTag({
        normal: '正常', abnormal: '异常', danger: '危险'
      }) },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        pending: '待整改', processing: '整改中', completed: '已完成'
      }) },
    ],
    formFields: [
      { prop: 'title', label: '巡查标题', rules: [{ required: true, message: '必填' }] },
      { prop: 'area', label: '巡查区域' },
      { prop: 'inspector', label: '巡查人' },
      { prop: 'check_time', label: '巡查时间' },
      {
        prop: 'result', label: '结果', type: 'select',
        options: [
          { label: '正常', value: 'normal' },
          { label: '异常', value: 'abnormal' },
          { label: '危险', value: 'danger' },
        ],
      },
      { prop: 'description', label: '情况说明', type: 'textarea' },
      { prop: 'rectification', label: '整改措施', type: 'textarea' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '待整改', value: 'pending' },
          { label: '整改中', value: 'processing' },
          { label: '已完成', value: 'completed' },
        ],
      },
    ],
  },

  'safety-hazards': {
    title: '安全隐患',
    api: api.safetyHazardApi,
    columns: [
      { prop: 'title', label: '隐患标题', width: 180 },
      { prop: 'level', label: '等级', width: 80, formatter: fmtTag({
        low: '低', medium: '中', high: '高', critical: '重大'
      }) },
      { prop: 'area', label: '区域', width: 100 },
      { prop: 'responsible_person', label: '责任人', width: 90 },
      { prop: 'deadline', label: '整改期限', width: 110 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        reported: '已上报', rectifying: '整改中', reviewing: '验收中', closed: '已闭环'
      }) },
    ],
    formFields: [
      { prop: 'title', label: '隐患标题', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'level', label: '等级', type: 'select',
        options: [
          { label: '低', value: 'low' }, { label: '中', value: 'medium' },
          { label: '高', value: 'high' }, { label: '重大', value: 'critical' },
        ],
      },
      { prop: 'area', label: '所在区域' },
      { prop: 'source', label: '隐患来源' },
      { prop: 'description', label: '隐患描述', type: 'textarea' },
      { prop: 'measures', label: '整改措施', type: 'textarea' },
      { prop: 'responsible_person', label: '责任人' },
      { prop: 'deadline', label: '整改期限' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '已上报', value: 'reported' },
          { label: '整改中', value: 'rectifying' },
          { label: '验收中', value: 'reviewing' },
          { label: '已闭环', value: 'closed' },
        ],
      },
    ],
  },

  'emergency-plans': {
    title: '应急预案',
    api: api.emergencyPlanApi,
    columns: [
      { prop: 'name', label: '预案名称', width: 200 },
      { prop: 'type', label: '类型', width: 100, formatter: fmtTag({
        fire: '火灾', typhoon: '台风', earthquake: '地震',
        equipment: '设备', power_outage: '断电', other: '其他'
      }) },
      { prop: 'level', label: '级别', width: 90, formatter: fmtTag({
        company: '公司级', department: '部门级', team: '班组级'
      }) },
      { prop: 'responsible_person', label: '负责人', width: 90 },
      { prop: 'status', label: '启用', width: 70, formatter: fmtTag({ True: '是', False: '否' }) },
    ],
    formFields: [
      { prop: 'name', label: '预案名称', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'type', label: '类型', type: 'select',
        options: [
          { label: '火灾', value: 'fire' }, { label: '台风', value: 'typhoon' },
          { label: '地震', value: 'earthquake' }, { label: '设备故障', value: 'equipment' },
          { label: '断电', value: 'power_outage' }, { label: '其他', value: 'other' },
        ],
      },
      {
        prop: 'level', label: '级别', type: 'select',
        options: [
          { label: '公司级', value: 'company' },
          { label: '部门级', value: 'department' },
          { label: '班组级', value: 'team' },
        ],
      },
      { prop: 'responsible_person', label: '负责人' },
      { prop: 'content', label: '预案内容', type: 'textarea' },
      { prop: 'procedures', label: '处置流程', type: 'textarea' },
      { prop: 'status', label: '启用', type: 'switch' },
    ],
  },

  'emergency-drills': {
    title: '应急演练',
    api: api.emergencyDrillApi,
    columns: [
      { prop: 'name', label: '演练名称', width: 180 },
      { prop: 'plan_name', label: '关联预案', width: 150 },
      { prop: 'drill_time', label: '演练时间', width: 110 },
      { prop: 'location', label: '地点', width: 110 },
      { prop: 'participants', label: '参与人数', width: 90 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        planned: '待演练', completed: '已完成', cancelled: '已取消'
      }) },
    ],
    formFields: [
      { prop: 'name', label: '演练名称', rules: [{ required: true, message: '必填' }] },
      { prop: 'plan_name', label: '关联预案' },
      { prop: 'drill_time', label: '演练时间' },
      { prop: 'location', label: '地点' },
      { prop: 'participants', label: '参与人数', type: 'number' },
      { prop: 'content', label: '演练内容', type: 'textarea' },
      { prop: 'evaluation', label: '评估总结', type: 'textarea' },
      { prop: 'problems', label: '存在问题', type: 'textarea' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '待演练', value: 'planned' },
          { label: '已完成', value: 'completed' },
          { label: '已取消', value: 'cancelled' },
        ],
      },
    ],
  },

  // ---- 人员管理 ----
  'employees': {
    title: '员工信息',
    api: api.employeeApi,
    columns: [
      { prop: 'employee_no', label: '工号', width: 100 },
      { prop: 'name', label: '姓名', width: 100 },
      { prop: 'gender', label: '性别', width: 60 },
      { prop: 'phone', label: '手机', width: 120 },
      { prop: 'department', label: '部门', width: 120 },
      { prop: 'position', label: '岗位', width: 120 },
      { prop: 'entry_date', label: '入职日期', width: 110 },
      { prop: 'status', label: '状态', width: 80, formatter: fmtTag({
        active: '在职', leave: '离职', resigned: '已离职'
      }) },
    ],
    formFields: [
      { prop: 'employee_no', label: '工号', rules: [{ required: true, message: '必填' }] },
      { prop: 'name', label: '姓名', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'gender', label: '性别', type: 'select',
        options: [{ label: '男', value: 'male' }, { label: '女', value: 'female' }],
      },
      { prop: 'phone', label: '手机' },
      { prop: 'email', label: '邮箱' },
      { prop: 'department', label: '部门' },
      { prop: 'position', label: '岗位' },
      { prop: 'entry_date', label: '入职日期' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '在职', value: 'active' },
          { label: '离职', value: 'leave' },
          { label: '已离职', value: 'resigned' },
        ],
      },
      { prop: 'remark', label: '备注', type: 'textarea' },
    ],
  },

  'shift-schedules': {
    title: '排班管理',
    api: api.shiftScheduleApi,
    columns: [
      { prop: 'employee_name', label: '员工', width: 100 },
      { prop: 'date', label: '日期', width: 110 },
      { prop: 'shift_type', label: '班次', width: 80, formatter: fmtTag({
        day: '白班', night: '夜班', off: '休息', oncall: '值班'
      }) },
      { prop: 'start_time', label: '开始', width: 80 },
      { prop: 'end_time', label: '结束', width: 80 },
    ],
    formFields: [
      { prop: 'employee_name', label: '员工姓名' },
      { prop: 'date', label: '日期', rules: [{ required: true, message: '必填' }] },
      {
        prop: 'shift_type', label: '班次', type: 'select',
        options: [
          { label: '白班', value: 'day' }, { label: '夜班', value: 'night' },
          { label: '休息', value: 'off' }, { label: '值班', value: 'oncall' },
        ],
      },
      { prop: 'start_time', label: '开始时间' },
      { prop: 'end_time', label: '结束时间' },
      { prop: 'remark', label: '备注', type: 'textarea' },
    ],
  },

  'attendance-records': {
    title: '考勤记录',
    api: api.attendanceRecordApi,
    columns: [
      { prop: 'employee_name', label: '员工', width: 100 },
      { prop: 'date', label: '日期', width: 110 },
      { prop: 'check_in', label: '签到', width: 90 },
      { prop: 'check_out', label: '签退', width: 90 },
      { prop: 'status', label: '状态', width: 90, formatter: fmtTag({
        normal: '正常', late: '迟到', early: '早退', absent: '缺勤', overtime: '加班'
      }) },
      { prop: 'work_hours', label: '工时', width: 70 },
      { prop: 'overtime_hours', label: '加班', width: 70 },
    ],
    formFields: [
      { prop: 'employee_name', label: '员工姓名' },
      { prop: 'date', label: '日期', rules: [{ required: true, message: '必填' }] },
      { prop: 'check_in', label: '签到时间' },
      { prop: 'check_out', label: '签退时间' },
      {
        prop: 'status', label: '状态', type: 'select',
        options: [
          { label: '正常', value: 'normal' }, { label: '迟到', value: 'late' },
          { label: '早退', value: 'early' }, { label: '缺勤', value: 'absent' },
          { label: '加班', value: 'overtime' },
        ],
      },
      { prop: 'work_hours', label: '工时', type: 'number' },
      { prop: 'overtime_hours', label: '加班工时', type: 'number' },
    ],
  },

  // ---- 财务报表 ----
  'revenue-items': {
    title: '收入统计',
    api: api.revenueItemApi,
    columns: [
      { prop: 'year', label: '年份', width: 70 },
      { prop: 'month', label: '月份', width: 70 },
      { prop: 'energy_revenue', label: '电费收入', width: 110 },
      { prop: 'subsidy_revenue', label: '补贴收入', width: 110 },
      { prop: 'carbon_revenue', label: '碳交易收入', width: 110 },
      { prop: 'total_revenue', label: '总收入', width: 110 },
    ],
    formFields: [
      { prop: 'year', label: '年份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'month', label: '月份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'energy_revenue', label: '电费收入', type: 'number' },
      { prop: 'subsidy_revenue', label: '补贴收入', type: 'number' },
      { prop: 'carbon_revenue', label: '碳交易收入', type: 'number' },
      { prop: 'other_revenue', label: '其他收入', type: 'number' },
    ],
  },

  'cost-items': {
    title: '成本分析',
    api: api.costItemApi,
    columns: [
      { prop: 'year', label: '年份', width: 70 },
      { prop: 'month', label: '月份', width: 70 },
      { prop: 'category', label: '成本类别', width: 120 },
      { prop: 'amount', label: '金额', width: 110 },
      { prop: 'description', label: '说明', minWidth: 200 },
    ],
    formFields: [
      { prop: 'year', label: '年份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'month', label: '月份', type: 'number', rules: [{ required: true, message: '必填' }] },
      { prop: 'category', label: '成本类别', rules: [{ required: true, message: '必填' }] },
      { prop: 'amount', label: '金额', type: 'number' },
      { prop: 'description', label: '说明', type: 'textarea' },
    ],
  },
}
