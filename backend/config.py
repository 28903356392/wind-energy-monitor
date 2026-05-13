"""应用配置"""
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/wind_farm.db")

# 服务配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# 模拟数据配置
MOCK_UPDATE_INTERVAL = int(os.getenv("MOCK_UPDATE_INTERVAL", "3"))  # 秒
TURBINE_COUNT = int(os.getenv("TURBINE_COUNT", "20"))
