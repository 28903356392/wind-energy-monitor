#!/bin/bash
# ============================================
# 风能监控系统 - 部署脚本
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

# 1. 先构建前端
echo ""
echo "[1/4] 构建前端..."
cd "$LOCAL_PROJECT/frontend"
npm run build 2>/dev/null
echo "  ✅ 前端构建完成"

# 2. 打包项目文件
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
  frontend/dist \
  backend \
  deploy/nginx.conf
echo "  ✅ 打包完成"

# 3. 上传到服务器
echo ""
echo "[3/4] 上传到服务器 ($SSH_HOST)..."
sshpass -p "$SSH_PASS" scp -o StrictHostKeyChecking=no \
  /tmp/wind-energy-deploy.tar.gz \
  "$SSH_USER@$SSH_HOST:/tmp/"
echo "  ✅ 上传完成"

# 4. 在服务器上部署
echo ""
echo "[4/4] 在服务器上部署..."
sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no "$SSH_USER@$SSH_HOST" << 'EOF'
    set -e

    # 解压
    sudo mkdir -p /app/workspace
    sudo tar -xzf /tmp/wind-energy-deploy.tar.gz -C /app/workspace/
    sudo mv /app/workspace/deploy/nginx.conf /etc/nginx/sites-available/wind-energy.conf 2>/dev/null || \
    sudo cp /app/workspace/deploy/nginx.conf /etc/nginx/sites-available/wind-energy.conf

    # 启用 Nginx 配置
    sudo ln -sf /etc/nginx/sites-available/wind-energy.conf /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default

    # 创建 systemd 服务
    sudo tee /etc/systemd/system/wind-energy-backend.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=Wind Energy Monitor Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/app/workspace/backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

    # 安装 Python 依赖和启动服务
    pip3 install -r /app/workspace/backend/requirements.txt -q 2>/dev/null || true

    sudo systemctl daemon-reload
    sudo systemctl enable wind-energy-backend
    sudo systemctl restart wind-energy-backend

    # 测试 Nginx 配置并重启
    sudo nginx -t && sudo systemctl restart nginx

    echo ""
    echo "  ✅ 部署完成！"
    echo "  🌐 前端: http://$SSH_HOST"
    echo "  🔌 API: http://$SSH_HOST/api/overview"
    echo "  📋 API文档: http://$SSH_HOST/docs"
EOF

# 清理临时文件
rm -f /tmp/wind-energy-deploy.tar.gz

echo ""
echo "=========================================="
echo "  🎉 部署成功！"
echo "  访问: http://$SSH_HOST"
echo "=========================================="
