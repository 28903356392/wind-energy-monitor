"""
业务模块配置数据
================
集中管理所有业务模块的关联映射配置。
"""
import models.business as m

# ============================================================
# MODEL_MAP: 资源名 → (模型类, 可搜索字段列表)
# 用于通用 CRUD 路由的模型查找和关键词搜索
# ============================================================
MODEL_MAP = {
    # 设备管理
    'equipment-types':     (m.EquipmentType, ['name', 'code', 'category']),
    'equipment-ledgers':   (m.EquipmentLedger, ['name', 'code', 'model']),
    'maintenance-records': (m.MaintenanceRecord, ['fault_description', 'fault_type']),
    # 运维管理
    'inspection-plans':    (m.InspectionPlan, ['name']),
    'inspection-records':  (m.InspectionRecord, ['inspector']),
    'work-orders':         (m.WorkOrder, ['title', 'order_no']),
    'spare-parts':         (m.SparePart, ['name', 'code', 'model']),
    'part-transactions':   (m.PartTransaction, ['part_name', 'remark']),
    # 生产管理
    'power-targets':       (m.PowerTarget, []),
    'energy-settlements':  (m.EnergySettlement, ['settlement_no', 'customer']),
    'carbon-reductions':   (m.CarbonReduction, []),
    # 安全监控
    'safety-inspections':  (m.SafetyInspection, ['title', 'inspector', 'area']),
    'safety-hazards':      (m.SafetyHazard, ['title', 'area']),
    'emergency-plans':     (m.EmergencyPlan, ['name', 'type']),
    'emergency-drills':    (m.EmergencyDrill, ['name']),
    # 人员管理
    'employees':           (m.Employee, ['name', 'employee_no', 'department']),
    'shift-schedules':     (m.ShiftSchedule, []),
    'attendance-records':  (m.AttendanceRecord, []),
    # 财务报表
    'revenue-items':       (m.RevenueItem, []),
    'cost-items':          (m.CostItem, []),
}

# ============================================================
# LOG_MAP: 资源名 → (模块名称, 操作名称)
# 用于操作日志记录
# ============================================================
LOG_MAP = {
    'equipment-types':     ('设备管理', '设备类型'),
    'equipment-ledgers':   ('设备管理', '设备台账'),
    'maintenance-records': ('设备管理', '维修记录'),
    'inspection-plans':    ('运维管理', '巡检计划'),
    'inspection-records':  ('运维管理', '巡检记录'),
    'work-orders':         ('运维管理', '工单管理'),
    'spare-parts':         ('运维管理', '备件管理'),
    'part-transactions':   ('运维管理', '备件出入库'),
    'power-targets':       ('生产管理', '发电指标'),
    'energy-settlements':  ('生产管理', '电量结算'),
    'carbon-reductions':   ('生产管理', '碳减排'),
    'safety-inspections':  ('安全监控', '安全巡检'),
    'safety-hazards':      ('安全监控', '安全隐患'),
    'emergency-plans':     ('安全监控', '应急预案'),
    'emergency-drills':    ('安全监控', '应急演练'),
    'employees':           ('人员管理', '员工信息'),
    'shift-schedules':     ('人员管理', '排班管理'),
    'attendance-records':  ('人员管理', '考勤记录'),
    'revenue-items':       ('财务报表', '收入统计'),
    'cost-items':          ('财务报表', '成本分析'),
}

# ============================================================
# PAGE_TYPE_MAP: 资源名 → 前端页面类型
# table=表格CRUD  kanban=看板  dashboard=仪表盘
# ============================================================
PAGE_TYPE_MAP = {
    'work-orders':       'kanban',
    'safety-hazards':    'kanban',
    'power-targets':     'dashboard',
    'revenue-items':     'dashboard',
    'carbon-reductions': 'dashboard',
    'cost-items':        'dashboard',
}

# ============================================================
# KANBAN_COLUMNS: 看板视图的列定义
# ============================================================
KANBAN_COLUMNS = {
    'work-orders': [
        {'status': 'pending',    'label': '待处理', 'tag': 'info'},
        {'status': 'processing', 'label': '处理中', 'tag': 'warning'},
        {'status': 'reviewing',  'label': '审核中', 'tag': 'primary'},
        {'status': 'completed',  'label': '已完成', 'tag': 'success'},
        {'status': 'closed',     'label': '已关闭', 'tag': ''},
    ],
    'safety-hazards': [
        {'status': 'reported',   'label': '已上报', 'tag': 'danger'},
        {'status': 'rectifying', 'label': '整改中', 'tag': 'warning'},
        {'status': 'reviewing',  'label': '验收中', 'tag': 'primary'},
        {'status': 'closed',     'label': '已闭环', 'tag': 'success'},
    ],
}

# ============================================================
# 辅助函数
# ============================================================
def get_model(resource: str):
    """根据资源名获取模型类"""
    from fastapi import HTTPException
    info = MODEL_MAP.get(resource)
    if not info:
        raise HTTPException(404, detail=f"资源不存在: {resource}")
    return info[0]

def get_search_fields(resource: str):
    """获取可搜索字段列表"""
    info = MODEL_MAP.get(resource)
    return info[1] if info else []

def get_log_info(resource: str):
    """获取日志模块/操作名"""
    return LOG_MAP.get(resource, ('业务管理', resource))

def get_page_type(resource: str):
    """获取前端页面类型"""
    return PAGE_TYPE_MAP.get(resource, 'table')

def get_kanban_columns(resource: str):
    """获取看板列配置"""
    return KANBAN_COLUMNS.get(resource, [])
