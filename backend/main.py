"""FastAPI 应用入口"""
import sys
import os
import asyncio

# 确保可以导入同级模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from config import HOST, PORT, CORS_ORIGINS, DATABASE_URL
from app_config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, MOCK_UPDATE_INTERVAL
from database import init_db, seed_mock_data, seed_admin
from mock_data import update_turbines_loop
from routers.wind_farm import router as wind_farm_router
from routers.auth import router as auth_router
from routers.system import router as system_router
from routers.business import router as business_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("[WindMonitor] 风能监控系统启动中...")
    db_path = DATABASE_URL.replace('sqlite:///', '', 1)
    if os.path.exists(db_path):
        print(f"[SKIP] 数据库已存在 ({db_path})，跳过初始化")
    else:
        init_db()
        seed_mock_data()
        seed_admin()
    # 启动后台数据更新任务
    task = asyncio.create_task(update_turbines_loop(MOCK_UPDATE_INTERVAL))
    print(f"[WindMonitor] 服务已启动 | 数据更新间隔: {MOCK_UPDATE_INTERVAL}s")
    yield
    # 关闭时
    task.cancel()
    print("[WindMonitor] 服务已关闭")


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(",") if CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(wind_farm_router)
app.include_router(auth_router)
app.include_router(system_router)
app.include_router(business_router)


@app.get("/api/doc.html", include_in_schema=False)
async def doc_redirect():
    return RedirectResponse(url="/api/docs")


@app.get("/")
def root():
    return {
        "service": APP_TITLE,
        "version": APP_VERSION,
        "docs": "/api/docs",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
