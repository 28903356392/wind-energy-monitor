"""数据模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone
import enum


class Base(DeclarativeBase):
    pass


class TurbineStatus(str, enum.Enum):
    RUNNING = "running"        # 运行中
    STOPPED = "stopped"        # 已停机
    MAINTENANCE = "maintenance"  # 维护中
    FAULT = "fault"            # 故障


class Turbine(Base):
    """风电机组"""
    __tablename__ = "turbines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    status = Column(SAEnum(TurbineStatus), default=TurbineStatus.RUNNING)
    power_output = Column(Float, default=0.0)       # 当前功率 (kW)
    wind_speed = Column(Float, default=0.0)         # 风速 (m/s)
    wind_direction = Column(Float, default=0.0)     # 风向 (度)
    rotor_speed = Column(Float, default=0.0)        # 转速 (rpm)
    temperature = Column(Float, default=0.0)        # 温度 (°C)
    daily_energy = Column(Float, default=0.0)       # 日发电量 (kWh)
    total_energy = Column(Float, default=0.0)       # 总发电量 (MWh)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PowerRecord(Base):
    """发电量记录"""
    __tablename__ = "power_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    total_power = Column(Float, default=0.0)         # 总功率 (kW)
    avg_wind_speed = Column(Float, default=0.0)      # 平均风速 (m/s)
    energy_hourly = Column(Float, default=0.0)       # 小时发电量
