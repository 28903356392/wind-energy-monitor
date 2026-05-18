"""风电场 API 路由 —— 含二级功能：告警、事件、能源统计"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from database import get_session
from models.turbine import Turbine, TurbineStatus, PowerRecord, Alarm, AlarmLevel, EventLog
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from typing import Optional
import json
import asyncio
import random

router = APIRouter(prefix="/api", tags=["wind_farm"])


# ==================== REST API ====================

@router.get("/overview")
def get_overview():
    """获取风电场总览数据"""
    session = get_session()
    try:
        total_power = session.query(func.sum(Turbine.power_output)).scalar() or 0
        total_daily = session.query(func.sum(Turbine.daily_energy)).scalar() or 0
        total_energy = session.query(func.sum(Turbine.total_energy)).scalar() or 0

        counts = {}
        for s in TurbineStatus:
            counts[s.value] = session.query(Turbine).filter(Turbine.status == s).count()

        avg_wind = session.query(func.avg(Turbine.wind_speed)).filter(
            Turbine.status == TurbineStatus.RUNNING
        ).scalar() or 0

        return {
            "code": 200,
            "data": {
                "total_power": round(total_power, 1),
                "total_daily_energy": round(total_daily, 1),
                "total_energy": round(total_energy, 1),
                "avg_wind_speed": round(avg_wind, 1),
                "turbine_count": sum(counts.values()),
                "running_count": counts.get("running", 0),
                "stopped_count": counts.get("stopped", 0),
                "maintenance_count": counts.get("maintenance", 0),
                "fault_count": counts.get("fault", 0),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    finally:
        session.close()


@router.get("/turbines")
def get_turbines(status: Optional[str] = None):
    """获取所有风机列表"""
    session = get_session()
    try:
        query = session.query(Turbine)
        if status:
            query = query.filter(Turbine.status == status)
        turbines = query.all()

        return {
            "code": 200,
            "data": [
                {
                    "id": t.id,
                    "name": t.name,
                    "status": t.status.value,
                    "power_output": t.power_output,
                    "wind_speed": t.wind_speed,
                    "wind_direction": t.wind_direction,
                    "rotor_speed": t.rotor_speed,
                    "temperature": t.temperature,
                    "daily_energy": t.daily_energy,
                    "total_energy": t.total_energy,
                    "updated_at": t.updated_at.isoformat()
                }
                for t in turbines
            ]
        }
    finally:
        session.close()


@router.get("/turbines/{turbine_id}")
def get_turbine(turbine_id: int):
    """获取单个风机详情"""
    session = get_session()
    try:
        t = session.query(Turbine).filter(Turbine.id == turbine_id).first()
        if not t:
            return {"code": 404, "message": "风机不存在"}
        return {
            "code": 200,
            "data": {
                "id": t.id,
                "name": t.name,
                "status": t.status.value,
                "power_output": t.power_output,
                "wind_speed": t.wind_speed,
                "wind_direction": t.wind_direction,
                "rotor_speed": t.rotor_speed,
                "temperature": t.temperature,
                "daily_energy": t.daily_energy,
                "total_energy": t.total_energy,
                "updated_at": t.updated_at.isoformat()
            }
        }
    finally:
        session.close()


@router.get("/power/history")
def get_power_history(hours: int = 24):
    """获取历史发电量数据"""
    session = get_session()
    try:
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        records = session.query(PowerRecord).filter(
            PowerRecord.timestamp >= since
        ).order_by(PowerRecord.timestamp).all()

        return {
            "code": 200,
            "data": [
                {
                    "timestamp": r.timestamp.isoformat(),
                    "total_power": r.total_power,
                    "avg_wind_speed": r.avg_wind_speed,
                    "energy_hourly": r.energy_hourly
                }
                for r in records
            ]
        }
    finally:
        session.close()


# ==================== 二级功能：告警 ====================

@router.get("/alarms")
def get_alarms(
    level: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    limit: int = Query(100, le=500)
):
    """获取告警列表（支持按级别/未处理筛选）"""
    session = get_session()
    try:
        query = session.query(Alarm).order_by(Alarm.created_at.desc())
        if level:
            query = query.filter(Alarm.level == level)
        if acknowledged is not None:
            query = query.filter(Alarm.acknowledged == acknowledged)
        alarms = query.limit(limit).all()

        return {
            "code": 200,
            "data": [
                {
                    "id": a.id,
                    "turbine_id": a.turbine_id,
                    "turbine_name": a.turbine_name,
                    "level": a.level.value,
                    "message": a.message,
                    "value": round(a.value, 1),
                    "threshold": a.threshold,
                    "created_at": a.created_at.isoformat(),
                    "acknowledged": a.acknowledged,
                }
                for a in alarms
            ]
        }
    finally:
        session.close()


@router.get("/alarms/stats")
def get_alarm_stats():
    """获取告警统计"""
    session = get_session()
    try:
        total = session.query(func.count(Alarm.id)).scalar() or 0
        critical = session.query(func.count(Alarm.id)).filter(
            Alarm.level == AlarmLevel.CRITICAL
        ).scalar() or 0
        warning = session.query(func.count(Alarm.id)).filter(
            Alarm.level == AlarmLevel.WARNING
        ).scalar() or 0
        info = session.query(func.count(Alarm.id)).filter(
            Alarm.level == AlarmLevel.INFO
        ).scalar() or 0

        return {
            "code": 200,
            "data": {
                "total": total,
                "critical": critical,
                "warning": warning,
                "info": info,
            }
        }
    finally:
        session.close()


# ==================== 二级功能：事件日志 ====================

@router.get("/events")
def get_events(
    event_type: Optional[str] = None,
    limit: int = Query(100, le=500)
):
    """获取事件日志"""
    session = get_session()
    try:
        query = session.query(EventLog).order_by(EventLog.timestamp.desc())
        if event_type:
            query = query.filter(EventLog.type == event_type)
        events = query.limit(limit).all()

        return {
            "code": 200,
            "data": [
                {
                    "id": e.id,
                    "type": e.type,
                    "message": e.message,
                    "detail": e.detail,
                    "timestamp": e.timestamp.isoformat(),
                }
                for e in events
            ]
        }
    finally:
        session.close()


# ==================== 二级功能：能源统计 ====================

@router.get("/energy/stats")
def get_energy_stats():
    """获取能源统计数据"""
    session = get_session()
    try:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)

        # 今日发电 = 今日新增的 daily_energy 总和
        total_today = session.query(func.sum(Turbine.daily_energy)).scalar() or 0

        # 历史总量
        total_all = session.query(func.sum(Turbine.total_energy)).scalar() or 0

        # 模拟昨日/本周/本月数据
        total_yesterday = total_today * random.uniform(0.8, 1.2)
        total_week = total_today * random.uniform(5, 7)
        total_month = total_today * random.uniform(22, 28)
        total_last_month = total_month * random.uniform(0.9, 1.1)

        # 效率：运行中风机 / 总风机
        running = session.query(func.count(Turbine.id)).filter(
            Turbine.status == TurbineStatus.RUNNING
        ).scalar() or 0
        total = session.query(func.count(Turbine.id)).scalar() or 1
        efficiency = round(running / total * 100, 1)

        return {
            "code": 200,
            "data": {
                "today": round(total_today, 1),
                "yesterday": round(total_yesterday, 1),
                "this_week": round(total_week, 1),
                "this_month": round(total_month, 1),
                "last_month": round(total_last_month, 1),
                "total": round(total_all, 1),
                "efficiency": efficiency,
            }
        }
    finally:
        session.close()


# ==================== WebSocket ====================

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead = []
        for conn in self.active_connections:
            try:
                await conn.send_json(message)
            except Exception:
                dead.append(conn)
        for d in dead:
            self.active_connections.remove(d)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 实时推送风机数据 + 告警"""
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                pass

            # 推送最新数据
            session = get_session()
            try:
                turbines = session.query(Turbine).all()
                total_power = sum(t.power_output for t in turbines)
                msg = {
                    "type": "update",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "total_power": round(total_power, 1),
                    "turbines": [
                        {
                            "id": t.id,
                            "name": t.name,
                            "status": t.status.value,
                            "power_output": t.power_output,
                            "wind_speed": t.wind_speed,
                        }
                        for t in turbines
                    ]
                }
                await websocket.send_json(msg)

                # 随机推送告警（模拟实时告警）
                if random.random() < 0.15:
                    t = random.choice(turbines)
                    alarm_msg = {
                        "type": "alarm",
                        "alarm": {
                            "id": random.randint(1000, 9999),
                            "turbine_id": t.id,
                            "turbine_name": t.name,
                            "level": random.choice(["info", "warning", "critical"]),
                            "message": f"{t.name} 异常告警",
                            "value": round(random.uniform(0, 100), 1),
                            "threshold": random.uniform(50, 100),
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "acknowledged": False,
                        }
                    }
                    await websocket.send_json(alarm_msg)
            finally:
                session.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[WebSocket] 连接异常: {e}")
        manager.disconnect(websocket)
