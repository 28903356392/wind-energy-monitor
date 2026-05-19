"""
种子数据模板
============
集中管理所有模拟数据的模板定义。
"""
from models.turbine import AlarmLevel

# ============================================================
# 告警模板: (级别, 消息模板, 值, 阈值)
# ============================================================
ALARM_TEMPLATES = [
    (AlarmLevel.INFO,     "{name} 功率波动轻微异常",             100, 200),
    (AlarmLevel.WARNING,  "{name} 温度偏高，建议检查冷却系统",    42,  40),
    (AlarmLevel.WARNING,  "{name} 风速超过安全阈值",             28,  25),
    (AlarmLevel.CRITICAL, "{name} 震动异常，紧急停机",            0,   0),
    (AlarmLevel.INFO,     "{name} 维护计划即将到期",              0,   0),
    (AlarmLevel.CRITICAL, "{name} 电网连接中断",                 0,   0),
    (AlarmLevel.WARNING,  "{name} 发电效率低于预期",            680, 750),
    (AlarmLevel.INFO,     "{name} 已完成例行检查",               0,   0),
]

# ============================================================
# 事件日志模板: (类型, 消息模板)
# ============================================================
EVENT_MESSAGES = [
    ("operation", "风机 {name} 启动成功"),
    ("operation", "风机 {name} 停机"),
    ("system",    "系统状态检查完成"),
    ("system",    "数据同步任务执行成功"),
    ("alarm",     "告警规则已触发: {name}"),
    ("operation", "运维人员登录系统"),
    ("system",    "数据库备份完成"),
    ("operation", "参数配置已更新: {name}"),
]

# ============================================================
# 风机状态分布: (状态, 数量)
# ============================================================
TURBINE_STATUS_DISTRIBUTION = [
    ('running',     15),
    ('stopped',     2),
    ('maintenance', 2),
    ('fault',       1),
]

# ============================================================
# 字典默认数据
# ============================================================
DEFAULT_DICT_TYPES = [
    {"name": "用户状态", "code": "sys_user_status", "remark": "用户状态"},
    {"name": "系统开关", "code": "sys_yes_no",      "remark": "系统开关"},
]

DEFAULT_DICT_DATA = [
    {"dict_code": "sys_user_status", "label": "正常", "value": "1", "sort": 1, "tag_type": "success"},
    {"dict_code": "sys_user_status", "label": "停用", "value": "0", "sort": 2, "tag_type": "danger"},
    {"dict_code": "sys_yes_no",      "label": "是",   "value": "Y", "sort": 1, "tag_type": "primary"},
    {"dict_code": "sys_yes_no",      "label": "否",   "value": "N", "sort": 2, "tag_type": "info"},
]

# ============================================================
# 默认管理员账号
# ============================================================
DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123",
    "nickname": "超级管理员",
    "email":    "admin@windfarm.com",
}
