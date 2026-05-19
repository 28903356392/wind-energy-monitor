"""
菜单数据结构文件
==============
所有菜单定义集中管理，按模块分组。
每条记录: (parent_name, name, path, component, icon, type, sort, permission, active)
  - parent_name: 父菜单名称(None=顶级)
  - active: True=启用 False=禁用
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class MenuItem:
    """菜单项数据结构"""
    parent_name: Optional[str]       # 父菜单名称（None=顶级目录）
    name: str                        # 菜单名称
    path: str                        # 路由路径
    component: str                   # Vue 组件路径
    icon: str                        # 图标名
    type: str                        # menu/directory/button
    sort: int                        # 排序号
    permission: str                  # 权限标识
    active: bool = True              # 启用状态


# ==================== 顶级导航 ====================

TOP_MENUS = [
    MenuItem(None, "风能大屏", "/dashboard", "views/dashboard/Index.vue", "Monitor", "menu", 1, "", True),
]

# ==================== 设备管理 ====================

EQUIPMENT_MENUS = [
    MenuItem(None, "设备管理", "", "", "Tools", "directory", 5, "", True),
    MenuItem("设备管理", "设备类型", "/business/equipment-types", "views/business/EquipmentTypes.vue", "Collection", "menu", 1, "business:equipment-types:list", True),
    MenuItem("设备管理", "设备台账", "/business/equipment-ledgers", "views/business/EquipmentLedgers.vue", "Document", "menu", 2, "business:equipment-ledgers:list", True),
    MenuItem("设备管理", "设备维修", "/business/maintenance-records", "views/business/MaintenanceRecords.vue", "Wrench", "menu", 3, "business:maintenance-records:list", True),
]

# ==================== 运维管理 ====================

OPERATION_MENUS = [
    MenuItem(None, "运维管理", "", "", "Operation", "directory", 6, "", True),
    MenuItem("运维管理", "巡检计划", "/business/inspection-plans", "views/business/InspectionPlans.vue", "Calendar", "menu", 1, "business:inspection-plans:list", True),
    MenuItem("运维管理", "巡检记录", "/business/inspection-records", "views/business/InspectionRecords.vue", "Checked", "menu", 2, "business:inspection-records:list", True),
    MenuItem("运维管理", "工单管理", "/business/work-orders", "views/business/WorkOrders.vue", "Tickets", "menu", 3, "business:work-orders:list", True),
    MenuItem("运维管理", "备件管理", "/business/spare-parts", "views/business/SpareParts.vue", "Box", "menu", 4, "business:spare-parts:list", True),
    MenuItem("运维管理", "备件出入库", "/business/part-transactions", "views/business/PartTransactions.vue", "RefreshRight", "menu", 5, "business:part-transactions:list", True),
]

# ==================== 生产管理 ====================

PRODUCTION_MENUS = [
    MenuItem(None, "生产管理", "", "", "TrendCharts", "directory", 7, "", True),
    MenuItem("生产管理", "发电量统计", "/business/power-targets", "views/business/PowerTargets.vue", "DataLine", "menu", 1, "business:power-targets:list", True),
    MenuItem("生产管理", "电量结算", "/business/energy-settlements", "views/business/EnergySettlements.vue", "Money", "menu", 2, "business:energy-settlements:list", True),
    MenuItem("生产管理", "碳减排管理", "/business/carbon-reductions", "views/business/CarbonReductions.vue", "Leaf", "menu", 3, "business:carbon-reductions:list", True),
]

# ==================== 安全监控 ====================

SAFETY_MENUS = [
    MenuItem(None, "安全监控", "", "", "WarningFilled", "directory", 8, "", True),
    MenuItem("安全监控", "安全巡检", "/business/safety-inspections", "views/business/SafetyInspections.vue", "Search", "menu", 1, "business:safety-inspections:list", True),
    MenuItem("安全监控", "安全隐患", "/business/safety-hazards", "views/business/SafetyHazards.vue", "Warning", "menu", 2, "business:safety-hazards:list", True),
    MenuItem("安全监控", "应急预案", "/business/emergency-plans", "views/business/EmergencyPlans.vue", "Files", "menu", 3, "business:emergency-plans:list", True),
    MenuItem("安全监控", "应急演练", "/business/emergency-drills", "views/business/EmergencyDrills.vue", "VideoPlay", "menu", 4, "business:emergency-drills:list", True),
]

# ==================== 人员管理 ====================

HR_MENUS = [
    MenuItem(None, "人员管理", "", "", "UserFilled", "directory", 9, "", True),
    MenuItem("人员管理", "员工信息", "/business/employees", "views/business/Employees.vue", "User", "menu", 1, "business:employees:list", True),
    MenuItem("人员管理", "排班管理", "/business/shift-schedules", "views/business/ShiftSchedules.vue", "Timer", "menu", 2, "business:shift-schedules:list", True),
    MenuItem("人员管理", "考勤记录", "/business/attendance-records", "views/business/AttendanceRecords.vue", "Stamp", "menu", 3, "business:attendance-records:list", True),
]

# ==================== 财务报表 ====================

FINANCE_MENUS = [
    MenuItem(None, "财务报表", "", "", "PieChart", "directory", 10, "", True),
    MenuItem("财务报表", "收入统计", "/business/revenue-items", "views/business/RevenueItems.vue", "Coin", "menu", 1, "business:revenue-items:list", True),
    MenuItem("财务报表", "成本分析", "/business/cost-items", "views/business/CostItems.vue", "Histogram", "menu", 2, "business:cost-items:list", True),
]

# ==================== 若依管理模块 ====================

RUOYI_MENUS = [
    MenuItem(None, "系统管理", "", "", "Setting", "directory", 2, "", True),
    MenuItem("系统管理", "用户管理", "/system/user", "views/system/user/UserList.vue", "User", "menu", 1, "system:user:list", True),
    MenuItem("系统管理", "角色管理", "/system/role", "views/system/role/RoleList.vue", "UserFilled", "menu", 2, "system:role:list", True),
    MenuItem("系统管理", "菜单管理", "/system/menu", "views/system/menu/MenuList.vue", "Menu", "menu", 3, "system:menu:list", True),
    MenuItem("系统管理", "字典管理", "/system/dict", "views/system/dict/DictList.vue", "Reading", "menu", 4, "system:dict:list", True),
    MenuItem(None, "日志管理", "", "", "Document", "directory", 3, "", True),
    MenuItem("日志管理", "操作日志", "/monitor/operation-log", "views/monitor/OperationLog.vue", "List", "menu", 1, "monitor:operation:list", True),
    MenuItem("日志管理", "登录日志", "/monitor/login-log", "views/monitor/LoginLog.vue", "Lock", "menu", 2, "monitor:login:list", True),
    MenuItem(None, "系统监控", "/monitor/system", "views/monitor/SystemMonitor.vue", "DataBoard", "menu", 4, "monitor:system:list", True),
]

# ==================== 全量菜单合并 ====================

ALL_MENUS = (
    TOP_MENUS +
    RUOYI_MENUS +
    EQUIPMENT_MENUS +
    OPERATION_MENUS +
    PRODUCTION_MENUS +
    SAFETY_MENUS +
    HR_MENUS +
    FINANCE_MENUS
)


def get_active_menus() -> list:
    """返回所有启用状态的菜单列表"""
    return [m for m in ALL_MENUS if m.active]


def get_menu_tuple_list(menus: list = None) -> list:
    """转换为 database.py 需要的 tuple 格式"""
    items = menus or ALL_MENUS
    return [
        (m.parent_name, m.name, m.path, m.component, m.icon, m.type, m.sort, m.permission)
        for m in items
    ]
