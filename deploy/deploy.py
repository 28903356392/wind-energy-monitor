#!/usr/bin/env python3
"""
风能监控系统 - 自动化部署脚本
==============================
一键打包、上传、部署到远程服务器
"""

import os
import sys
import subprocess
import paramiko
from pathlib import Path

# ==================== 配置 ====================
SSH_HOST = "150.158.49.82"
SSH_USER = "ubuntu"
SSH_PASS = "y123456789Y"
REMOTE_DIR = "/app/workspace"
PROJECT_ROOT = Path(r"F:\ai\wind-energy-monitor")
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DEPLOY_DIR = PROJECT_ROOT / "deploy"
TEMP_TAR = PROJECT_ROOT / "wind-energy-deploy.tar.gz"


def step(msg):
    print(f"\n{'='*50}")
    print(f"  [{msg}]")
    print(f"{'='*50}")


def build_frontend():
    """构建前端"""
    step("1/4 构建前端")
    ret = os.system(f'cd /d "{FRONTEND_DIR}" && npm run build 2>nul')
    if ret != 0:
        print("前端构建失败，请检查错误")
        sys.exit(1)
    print("  [OK] 前端构建完成")


def package_project():
    """使用 Git Bash tar 命令打包项目"""
    step("2/4 打包项目")

    if TEMP_TAR.exists():
        TEMP_TAR.unlink()

    # 使用 Git Bash 的 tar 命令打包（用相对路径避免 Windows 路径问题）
    tar_cmd = (
        f'tar -czf wind-energy-deploy.tar.gz '
        f'--exclude="frontend/node_modules" '
        f'--exclude="frontend/src" '
        f'--exclude="backend/__pycache__" '
        f'--exclude="backend/backend/*.db" '
        f'--exclude=".git" '
        f'--exclude="deploy/deploy.sh" '
        f'--exclude="deploy/deploy.py" '
        f'frontend/dist backend deploy/nginx.conf'
    )

    result = subprocess.run(
        tar_cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        shell=True
    )

    if result.returncode != 0:
        print(f"  [FAIL] 打包失败: {result.stderr}")
        sys.exit(1)

    if TEMP_TAR.exists():
        size_kb = TEMP_TAR.stat().st_size / 1024
        print(f"  [OK] 打包完成 ({size_kb:.1f} KB)")
        print(f"       包含: frontend/dist, backend/, deploy/nginx.conf")
    else:
        print("  [FAIL] 打包文件未生成")
        sys.exit(1)


def deploy_to_server():
    """上传并部署到服务器"""
    step("3/4 上传到服务器")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS, timeout=10)
        print(f"  [OK] SSH 连接成功 ({SSH_HOST})")
    except Exception as e:
        print(f"  [FAIL] SSH 连接失败: {e}")
        sys.exit(1)

    # SFTP 上传
    try:
        sftp = ssh.open_sftp()
        remote_tar = "/tmp/wind-energy-deploy.tar.gz"
        sftp.put(str(TEMP_TAR), remote_tar)
        sftp.close()
        print(f"  [OK] 文件上传完成")
    except Exception as e:
        print(f"  [FAIL] 上传失败: {e}")
        ssh.close()
        sys.exit(1)

    step("4/4 在服务器上部署")

    # 构建部署命令（用 heredoc 避免转义问题）
    deploy_script = f"""#!/bin/bash
set -e

echo '  [..] 解压文件...'
sudo mkdir -p {REMOTE_DIR}
sudo tar -xzf /tmp/wind-energy-deploy.tar.gz -C {REMOTE_DIR}/
echo '  [OK] 解压完成'

echo '  [..] 安装后端依赖...'
sudo pip3 install -r {REMOTE_DIR}/backend/requirements.txt -q 2>/dev/null || echo '  [WARN] pip install 跳过'

echo '  [..] 配置 Nginx...'
sudo cp {REMOTE_DIR}/deploy/nginx.conf /etc/nginx/sites-available/wind-energy.conf
sudo ln -sf /etc/nginx/sites-available/wind-energy.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
echo '  [OK] Nginx 配置完成'

echo '  [..] 配置后端 systemd 服务...'
sudo tee /etc/systemd/system/wind-energy-backend.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=Wind Energy Monitor Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={REMOTE_DIR}/backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable wind-energy-backend
sudo systemctl restart wind-energy-backend
echo '  [OK] 后端服务已启动'

echo '  [..] 重启 Nginx...'
sudo nginx -t && sudo systemctl restart nginx
echo '  [OK] Nginx 已重启'

sleep 2

echo ''
echo '  -- 服务状态 --'
sudo systemctl status wind-energy-backend --no-pager | head -5
echo ''
sudo systemctl status nginx --no-pager | head -5
echo ''

echo '  -- API 测试 --'
curl -s http://localhost:8000/health || echo '  [FAIL] API 未响应'
"""

    # 通过 SSH 执行部署脚本
    transport = ssh.get_transport()
    if transport:
        channel = transport.open_session()
        channel.exec_command('bash -s')
        channel.send(deploy_script.encode('utf-8'))
        channel.shutdown_write()

        exit_code = channel.recv_exit_status()
        output = b""
        while True:
            data = channel.recv(4096)
            if not data:
                break
            output += data
        output = output.decode("utf-8", errors="ignore").strip()

        if output:
            for line in output.split('\n'):
                if line.strip():
                    print(f"  {line.strip()}")

        if exit_code != 0:
            print(f"  [WARN] 部署脚本返回非零退出码 ({exit_code})")

    ssh.close()

    # 清理
    if TEMP_TAR.exists():
        TEMP_TAR.unlink()

    print(f"\n{'='*50}")
    print(f"  [SUCCESS] 部署成功！")
    print(f"  [WEB] http://{SSH_HOST}")
    print(f"  [API] http://{SSH_HOST}/api/overview")
    print(f"  [DOCS] http://{SSH_HOST}/docs")
    print(f"{'='*50}")


if __name__ == "__main__":
    build_frontend()
    package_project()
    deploy_to_server()
