"""
部署配置
========
集中管理部署相关的服务器信息，被 deploy.py 和 deploy.sh 引用。
"""

# ==================== 服务器连接 ====================
SSH_HOST = "150.158.49.82"
SSH_USER = "ubuntu"
SSH_PASS = "y123456789Y"

# ==================== 远程路径 ====================
REMOTE_DIR = "/app/workspace"
REMOTE_BACKEND = f"{REMOTE_DIR}/backend"
REMOTE_FRONTEND = f"{REMOTE_DIR}/frontend/dist"
REMOTE_NGINX_CONF = f"{REMOTE_DIR}/deploy/nginx.conf"

# ==================== 本地路径 ====================
LOCAL_PROJECT = "/f/ai/wind-energy-monitor"
LOCAL_BACKEND = f"{LOCAL_PROJECT}/backend"
LOCAL_FRONTEND = f"{LOCAL_PROJECT}/frontend"
LOCAL_DEPLOY = f"{LOCAL_PROJECT}/deploy"
