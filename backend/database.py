"""数据库初始化"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DATABASE_URL
from models import Base, Turbine, PowerRecord, TurbineStatus
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
    # 如果已有数据则跳过
    if session.query(Turbine).count() > 0:
        session.close()
        return

    # 风机经纬度坐标（模拟一个风电场布局）
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

    # 生成历史发电量数据（过去24小时，每5分钟一个点）
    now = datetime.now(timezone.utc)
    for i in range(288):  # 24h * 12
        t = now - timedelta(minutes=5 * (288 - i))
        base_power = 12000 + 3000 * math.sin(i * math.pi / 48) + random.uniform(-500, 500)
        record = PowerRecord(
            timestamp=t,
            total_power=round(base_power, 1),
            avg_wind_speed=round(8 + 3 * math.sin(i * math.pi / 48) + random.uniform(-1, 1), 1),
            energy_hourly=round(base_power / 12, 2)
        )
        session.add(record)

    session.commit()
    session.close()
    print("✅ 模拟数据已初始化")
