"""模拟数据生成器 - 实时更新风机数据"""
import random
import math
import asyncio
from datetime import datetime, timezone
from database import get_session
from models.turbine import Turbine, TurbineStatus, PowerRecord


def _rand_walk(current, step_range, min_val=None, max_val=None):
    """随机游走"""
    delta = random.uniform(-step_range, step_range)
    new_val = current + delta
    if min_val is not None:
        new_val = max(min_val, new_val)
    if max_val is not None:
        new_val = min(max_val, new_val)
    return round(new_val, 1)


async def update_turbines_loop(interval: int = 3):
    """定时更新所有风机数据（后台任务）"""
    while True:
        await asyncio.sleep(interval)
        try:
            session = get_session()
            turbines = session.query(Turbine).all()
            now = datetime.now(timezone.utc)
            total_power = 0.0
            total_wind = 0.0
            running_count = 0

            for t in turbines:
                if t.status == TurbineStatus.RUNNING:
                    t.power_output = _rand_walk(t.power_output, 50, 0, 1600)
                    t.wind_speed = _rand_walk(t.wind_speed, 0.5, 0, 20)
                    t.wind_direction = _rand_walk(t.wind_direction, 5, 0, 360)
                    t.rotor_speed = _rand_walk(t.rotor_speed, 0.3, 0, 20)
                    t.temperature = _rand_walk(t.temperature, 0.3, 10, 45)
                    t.daily_energy = round(t.daily_energy + t.power_output / 1200, 1)
                    total_power += t.power_output
                    total_wind += t.wind_speed
                    running_count += 1
                elif t.status == TurbineStatus.STOPPED:
                    t.power_output = 0
                    t.wind_speed = _rand_walk(t.wind_speed, 0.3, 0, 5)
                elif t.status == TurbineStatus.FAULT:
                    t.power_output = 0
                    t.wind_speed = _rand_walk(t.wind_speed, 0.2, 0, 3)

                t.updated_at = now

            # 每5分钟添加一条功率记录
            if int(now.timestamp()) % 300 < interval:
                avg_wind = round(total_wind / running_count, 1) if running_count > 0 else 0
                record = PowerRecord(
                    timestamp=now,
                    total_power=round(total_power, 1),
                    avg_wind_speed=avg_wind,
                    energy_hourly=round(total_power / 12, 2)
                )
                session.add(record)

            session.commit()
            session.close()
        except Exception as e:
            print(f"[MockData] 更新数据失败: {e}")
