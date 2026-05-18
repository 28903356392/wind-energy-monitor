"""风机监控数据模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SAEnum, Text, Boolean
from datetime import datetime, timezone
from models.base import Base
import enum


class TurbineStatus(str, enum.Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    FAULT = "fault"


class AlarmLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Turbine(Base):
    __tablename__ = "turbines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    status = Column(SAEnum(TurbineStatus), default=TurbineStatus.RUNNING)
    power_output = Column(Float, default=0.0)
    wind_speed = Column(Float, default=0.0)
    wind_direction = Column(Float, default=0.0)
    rotor_speed = Column(Float, default=0.0)
    temperature = Column(Float, default=0.0)
    daily_energy = Column(Float, default=0.0)
    total_energy = Column(Float, default=0.0)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PowerRecord(Base):
    __tablename__ = "power_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    total_power = Column(Float, default=0.0)
    avg_wind_speed = Column(Float, default=0.0)
    energy_hourly = Column(Float, default=0.0)


class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    turbine_id = Column(Integer, nullable=False)
    turbine_name = Column(String(50), default='')
    level = Column(SAEnum(AlarmLevel), default=AlarmLevel.INFO)
    message = Column(String(500), default='')
    value = Column(Float, default=0.0)
    threshold = Column(Float, default=0.0)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), default='system')
    message = Column(String(500), default='')
    detail = Column(Text, default='')
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
