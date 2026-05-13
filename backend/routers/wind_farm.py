"""风电场 API 路由"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database import get_session
from models import Turbine, TurbineStatus, PowerRecord
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from typing import Optional
import json
import asyncio

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


# ==================== WebSocket ====================

class ConnectionManager:
    """WebSocket 连接管理器"""

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
    """WebSocket 实时推送风机数据"""
    await manager.connect(websocket)
    try:
        while True:
            # 等待客户端消息（或保持连接）
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
            finally:
                session.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[WebSocket] 连接异常: {e}")
        manager.disconnect(websocket)
