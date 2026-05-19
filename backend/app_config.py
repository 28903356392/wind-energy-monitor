"""
后端应用配置
============
集中管理后端的所有常量配置，各模块从这里导入。
"""

# ==================== 应用元信息 ====================
APP_TITLE = "风能监控系统 API"
APP_DESCRIPTION = "风电场大屏监控后端服务"
APP_VERSION = "1.0.0"

# ==================== JWT 安全配置 ====================
JWT_SECRET_KEY = "ruoyi-secret-key-2026-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 1440  # 24小时

# ==================== 模拟数据配置 ====================
MOCK_UPDATE_INTERVAL = 3       # 数据更新间隔（秒）
TURBINE_COUNT = 20             # 风机数量
MOCK_ALARM_COUNT = 30          # 初始告警数量
MOCK_EVENT_COUNT = 60          # 初始事件数量
MOCK_POWER_RECORDS = 288       # 功率记录数（24小时每5分钟）

# ==================== 种子数据量 ====================
SEED_ALARM_COUNT = 30
SEED_EVENT_COUNT = 60
SEED_POWER_RECORDS = 288

# ==================== 默认管理员 ====================
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_NICKNAME = "超级管理员"
DEFAULT_ADMIN_EMAIL = "admin@windfarm.com"
