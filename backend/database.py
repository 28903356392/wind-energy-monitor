"""数据库初始化"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DATABASE_URL
from models import Base
from models.turbine import Turbine, PowerRecord, TurbineStatus, Alarm, AlarmLevel, EventLog
from models.user import User, Role, Menu
from models.system import DictType, DictData, Config
from security import hash_password
from datetime import datetime, timezone, timedelta
import random
import math

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """获取数据库会话"""
    return Session(engine)


def seed_mock_data():
    """填充模拟数据"""
    session = get_session()
    if session.query(Turbine).count() > 0:
        session.close()
        return

    # ---- 风机坐标 ----
    coordinates = [
        (40.12, 116.30), (40.13, 116.32), (40.14, 116.28), (40.11, 116.35),
        (40.15, 116.31), (40.12, 116.33), (40.13, 116.29), (40.14, 116.34),
        (40.11, 116.27), (40.15, 116.36), (40.12, 116.28), (40.13, 116.31),
        (40.14, 116.33), (40.11, 116.29), (40.15, 116.30), (40.12, 116.34),
        (40.13, 116.27), (40.14, 116.32), (40.11, 116.36), (40.15, 116.35),
    ]

    statuses = [TurbineStatus.RUNNING] * 15 + [TurbineStatus.STOPPED] * 2 + \
               [TurbineStatus.MAINTENANCE] * 2 + [TurbineStatus.FAULT] * 1
    random.shuffle(statuses)

    for i, (lat, lon) in enumerate(coordinates):
        status = statuses[i]
        power = random.uniform(800, 1500) if status == TurbineStatus.RUNNING else 0
        wind_spd = random.uniform(5, 12) if status == TurbineStatus.RUNNING else random.uniform(0, 3)

        turbine = Turbine(
            name=f"WTG-{i + 1:03d}",
            status=status,
            power_output=round(power, 1),
            wind_speed=round(wind_spd, 1),
            wind_direction=round(random.uniform(0, 360), 1),
            rotor_speed=round(power / 100 * 0.8 + random.uniform(-0.5, 0.5), 1),
            temperature=round(random.uniform(15, 35), 1),
            daily_energy=round(power * random.uniform(0.1, 0.5), 1),
            total_energy=round(random.uniform(500, 5000), 1),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(turbine)

    # ---- 发电量历史 ----
    now = datetime.now(timezone.utc)
    for i in range(288):
        t = now - timedelta(minutes=5 * (288 - i))
        base_power = 12000 + 3000 * math.sin(i * math.pi / 48) + random.uniform(-500, 500)
        record = PowerRecord(
            timestamp=t,
            total_power=round(base_power, 1),
            avg_wind_speed=round(8 + 3 * math.sin(i * math.pi / 48) + random.uniform(-1, 1), 1),
            energy_hourly=round(base_power / 12, 2)
        )
        session.add(record)

    # ---- 告警数据 ----
    alarm_templates = [
        (AlarmLevel.INFO, "{name} 功率波动轻微异常", 100, 200),
        (AlarmLevel.WARNING, "{name} 温度偏高，建议检查冷却系统", 42, 40),
        (AlarmLevel.WARNING, "{name} 风速超过安全阈值", 28, 25),
        (AlarmLevel.CRITICAL, "{name} 震动异常，紧急停机", 0, 0),
        (AlarmLevel.INFO, "{name} 维护计划即将到期", 0, 0),
        (AlarmLevel.CRITICAL, "{name} 电网连接中断", 0, 0),
        (AlarmLevel.WARNING, "{name} 发电效率低于预期", 680, 750),
        (AlarmLevel.INFO, "{name} 已完成例行检查", 0, 0),
    ]

    turbines_list = session.query(Turbine).all()
    for _ in range(30):
        tmpl = random.choice(alarm_templates)
        t = random.choice(turbines_list)
        alarm = Alarm(
            turbine_id=t.id,
            turbine_name=t.name,
            level=tmpl[0],
            message=tmpl[1].format(name=t.name),
            value=tmpl[2] + random.uniform(-10, 10),
            threshold=tmpl[3],
            created_at=now - timedelta(
                hours=random.randint(0, 48),
                minutes=random.randint(0, 59)
            ),
            acknowledged=random.random() < 0.6,
        )
        session.add(alarm)

    # ---- 事件日志 ----
    event_types = ["operation", "system", "alarm"]
    event_messages = [
        ("operation", "风机 {name} 启动成功"),
        ("operation", "风机 {name} 停机"),
        ("system", "系统状态检查完成"),
        ("system", "数据同步任务执行成功"),
        ("alarm", "告警规则已触发: {name}"),
        ("operation", "运维人员登录系统"),
        ("system", "数据库备份完成"),
        ("operation", "参数配置已更新: {name}"),
    ]

    for _ in range(60):
        tmpl = random.choice(event_messages)
        t = random.choice(turbines_list)
        event = EventLog(
            type=tmpl[0],
            message=tmpl[1].format(name=t.name),
            detail=f"ID: {t.id}, 时间: {now - timedelta(minutes=random.randint(0, 1440))}",
            timestamp=now - timedelta(
                hours=random.randint(0, 72),
                minutes=random.randint(0, 59)
            ),
        )
        session.add(event)

    session.commit()
    session.close()
    print("[OK] 模拟数据已初始化（含告警、事件）")


def seed_admin():
    """初始化默认管理员和基础菜单"""
    session = get_session()
    if session.query(User).filter(User.username == "admin").count() > 0:
        session.close()
        return

    # 创建超管用户
    admin = User(
        username="admin",
        password=hash_password("admin123"),
        nickname="超级管理员",
        email="admin@windfarm.com",
        status=True,
        is_admin=True,
        remark="系统超管",
    )
    session.add(admin)

    # 创建默认角色
    role_admin = Role(name="超管角色", code="admin", status=True, sort=1, remark="系统管理员")
    role_user = Role(name="普通用户", code="user", status=True, sort=2, remark="普通用户")
    session.add_all([role_admin, role_user])

    # 创建基础菜单（用 name 查找 parent_id，避免硬编码数字）
    menus = []
    menu_items = [
        # (parent_name, name, path, component, icon, type, sort, permission)
        (None, "风能大屏", "/dashboard", "views/dashboard/Index.vue", "Monitor", "menu", 1, ""),
        (None, "系统管理", "", "", "Setting", "directory", 2, ""),
        ("系统管理", "用户管理", "/system/user", "views/system/user/UserList.vue", "User", "menu", 1, "system:user:list"),
        ("系统管理", "角色管理", "/system/role", "views/system/role/RoleList.vue", "UserFilled", "menu", 2, "system:role:list"),
        ("系统管理", "菜单管理", "/system/menu", "views/system/menu/MenuList.vue", "Menu", "menu", 3, "system:menu:list"),
        ("系统管理", "字典管理", "/system/dict", "views/system/dict/DictList.vue", "Reading", "menu", 4, "system:dict:list"),
        (None, "日志管理", "", "", "Document", "directory", 3, ""),
        ("日志管理", "操作日志", "/monitor/operation-log", "views/monitor/OperationLog.vue", "List", "menu", 1, "monitor:operation:list"),
        ("日志管理", "登录日志", "/monitor/login-log", "views/monitor/LoginLog.vue", "Lock", "menu", 2, "monitor:login:list"),
        (None, "系统监控", "/monitor/system", "views/monitor/SystemMonitor.vue", "DataBoard", "menu", 4, "monitor:system:list"),
    ]

    name_id_map = {}
    for parent_name, name, path, comp, icon, mtype, sort, perm in menu_items:
        parent_id = name_id_map.get(parent_name, 0) if parent_name else 0
        menu = Menu(
            parent_id=parent_id, name=name, path=path, component=comp,
            icon=icon, type=mtype, sort=sort, permission=perm, status=True,
        )
        session.add(menu)
        session.flush()
        name_id_map[name] = menu.id
        menus.append(menu)

    # 超管角色关联所有菜单
    role_admin.menus = menus

    # 创建默认字典
    dict_types = [
        DictType(name="用户状态", code="sys_user_status", status=True, remark="用户状态"),
        DictType(name="系统开关", code="sys_yes_no", status=True, remark="系统开关"),
    ]
    session.add_all(dict_types)
    session.flush()

    dict_data = [
        DictData(dict_code="sys_user_status", label="正常", value="1", sort=1, tag_type="success", status=True),
        DictData(dict_code="sys_user_status", label="停用", value="0", sort=2, tag_type="danger", status=True),
        DictData(dict_code="sys_yes_no", label="是", value="Y", sort=1, tag_type="primary", status=True),
        DictData(dict_code="sys_yes_no", label="否", value="N", sort=2, tag_type="info", status=True),
    ]
    session.add_all(dict_data)

    session.commit()
    session.close()
    print("[OK] 默认管理员 (admin/admin123) 和菜单已初始化")
