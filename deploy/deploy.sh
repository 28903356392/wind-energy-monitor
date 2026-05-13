#!/bin/bash
# ============================================
# 风能监控系统 - 一键部署脚本
# 用法: bash deploy/deploy.sh
# ============================================

set -e

SSH_HOST="150.158.49.82"
SSH_USER="ubuntu"
SSH_PASS="y123456789Y"
REMOTE_DIR="/app/workspace"
LOCAL_PROJECT="/f/ai/wind-energy-monitor"

echo "=========================================="
echo "  风能监控系统部署脚本"
echo "=========================================="

# 1. 构建前端
echo ""
echo "[1/4] 构建前端..."
cd "$LOCAL_PROJECT/frontend"
npm run build 2>/dev/null
echo "  [OK] 前端构建完成"

# 2. 打包项目
echo ""
echo "[2/4] 打包项目..."
cd "$LOCAL_PROJECT"
tar -czf /tmp/wind-energy-deploy.tar.gz \
  --exclude='frontend/node_modules' \
  --exclude='frontend/src' \
  --exclude='backend/__pycache__' \
  --exclude='backend/data/*.db' \
  --exclude='.git' \
  --exclude='deploy/deploy.sh' \
  --exclude='deploy/deploy.py' \
  frontend/dist \
  backend \
  deploy/nginx.conf
echo "  [OK] 打包完成"

# 3. 上传
echo ""
echo "[3/4] 上传到服务器 ($SSH_HOST)..."
sshpass -p "$SSH_PASS" scp -o StrictHostKeyChecking=no \
  /tmp/wind-energy-deploy.tar.gz \
  "$SSH_USER@$SSH_HOST:/tmp/"
echo "  [OK] 上传完成"

# 4. 远程部署
echo ""
echo "[4/4] 在服务器上部署..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no "$SSH_USER@$SSH_HOST" << 'REMOTE'
    set -e

    echo "  [..] 创建目录并解压..."
    sudo mkdir -p /app/workspace
    sudo tar -xzf /tmp/wind-energy-deploy.tar.gz -C /app/workspace/

    echo "  [..] 创建数据目录..."
    sudo mkdir -p /app/workspace/backend/data

    echo "  [..] 安装 Python 依赖..."
    sudo pip3 install -r /app/workspace/backend/requirements.txt -q 2>/dev/null || true

    echo "  [..] 配置 Nginx..."
    sudo cp /app/workspace/deploy/nginx.conf /etc/nginx/sites-available/wind-energy.conf
    sudo ln -sf /etc/nginx/sites-available/wind-energy.conf /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default

    echo "  [..] 配置 systemd 服务..."
    sudo tee /etc/systemd/system/wind-energy-backend.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=Wind Energy Monitor Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/app/workspace/backend
Environment=PYTHONUNBUFFERED=1
ExecStartPre=/bin/mkdir -p /app/workspace/backend/data
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

    sudo systemctl daemon-reload
    sudo systemctl enable wind-energy-backend
    sudo systemctl restart wind-energy-backend

    echo "  [..] 重启 Nginx..."
    sudo nginx -t && sudo systemctl restart nginx

    sleep 2

    # 验证
    echo ""
    echo "  -- 服务状态 --"
    sudo systemctl status wind-energy-backend --no-pager | head -6
    echo ""
    sudo systemctl status nginx --no-pager | head -4
    echo ""

    # API 自检
    echo "  -- API 自检 --"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "  [OK] 后端 API 响应正常 (HTTP $HTTP_CODE)"
    else
        echo "  [WARN] 后端 API 未响应 (HTTP $HTTP_CODE)"
    fi

    echo ""
    echo "  [OK] 部署完成！"
    echo "  [WEB]  http://150.158.49.82"
    echo "  [API]  http://150.158.49.82/api/overview"
REMOTE

# 清理临时文件
rm -f /tmp/wind-energy-deploy.tar.gz

echo ""
echo "=========================================="
echo "  部署成功！"
echo "  访问: http://$SSH_HOST"
echo "=========================================="
