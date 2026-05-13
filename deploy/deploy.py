#!/usr/bin/env python3
"""
风能监控系统 - 自动化部署脚本
==============================
功能:
  1. 检查本地开发环境（Node/npm/Python），缺失则自动安装
  2. 检查远程服务器环境（Python3/Nginx/systemd），缺失则自动安装
  3. 构建前端 → 打包 → 上传 → 远程部署
"""
import os
import sys
import subprocess
import paramiko
import shutil
import platform
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


# ==================== 工具函数 ====================

def color(msg, status):
    """带状态图标的消息"""
    icon = {"OK": "[OK]", "FAIL": "[FAIL]", "WARN": "[WARN]", "..": "[..]"}
    return f"  {icon.get(status, status)} {msg}"


def step(msg):
    print(f"\n{'='*50}")
    print(f"  [{msg}]")
    print(f"{'='*50}")


def run_cmd(cmd, cwd=None, check=True, capture=True):
    """执行系统命令"""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else cmd,
        cwd=cwd,
        capture_output=capture,
        text=True,
        shell=isinstance(cmd, str)
    )
    if check and result.returncode != 0:
        print(f"    {color('命令失败: ' + (result.stderr.strip() or '未知错误'), 'FAIL')}")
        return None
    return result


def check_exe(name, install_hint=None):
    """检查可执行文件是否存在"""
    path = shutil.which(name)
    if path:
        return path
    if install_hint:
        print(f"    {color(f'{name} 未找到', 'WARN')}")
        print(f"    {color(f'尝试安装: {install_hint}', '..')}")
    return None


# ==================== 本地环境检查与安装 ====================

LOCAL_ENV_OK = True

def check_local_env():
    """检查本机构建环境"""
    global LOCAL_ENV_OK
    step("0/5 检查本地开发环境")

    # ---- Node.js ----
    node_path = check_exe("node", "winget install OpenJS.NodeJS 或 https://nodejs.org")
    if node_path:
        ver = subprocess.run([node_path, "--version"], capture_output=True, text=True).stdout.strip()
        print(f"    {color(f'Node.js: {ver}', 'OK')}")
    else:
        LOCAL_ENV_OK = False
        _install_nodejs()

    # ---- npm ----
    npm_path = check_exe("npm")
    if npm_path:
        ver = subprocess.run([npm_path, "--version"], capture_output=True, text=True).stdout.strip()
        print(f"    {color(f'npm: {ver}', 'OK')}")
        # 确保前端依赖已安装
        node_modules = FRONTEND_DIR / "node_modules"
        if not node_modules.exists():
            print(f"    {color('安装前端依赖 npm install...', '..')}")
            run_cmd("npm install", cwd=str(FRONTEND_DIR))
            print(f"    {color('前端依赖安装完成', 'OK')}")
    else:
        LOCAL_ENV_OK = False
        print(f"    {color('npm 未找到（Node.js 安装后应自带）', 'FAIL')}")

    # ---- Python ----
    python_cmd = _get_python_cmd()
    if python_cmd:
        ver = subprocess.run([python_cmd, "--version"], capture_output=True, text=True).stdout.strip()
        print(f"    {color(f'Python: {ver}', 'OK')}")
    else:
        LOCAL_ENV_OK = False
        _install_python()

    # ---- pip / paramiko ----
    try:
        import paramiko
        print(f"    {color('paramiko: 已安装', 'OK')}")
    except ImportError:
        print(f"    {color('paramiko 未安装，正在安装...', '..')}")
        ret = run_cmd(f"{_get_python_cmd()} -m pip install paramiko -q", check=False)
        if ret and ret.returncode == 0:
            print(f"    {color('paramiko 安装完成', 'OK')}")
        else:
            print(f"    {color('paramiko 安装失败，请手动执行: pip install paramiko', 'FAIL')}")
            sys.exit(1)

    if LOCAL_ENV_OK:
        print(f"\n    {color('本地开发环境就绪', 'OK')}")


def _get_python_cmd():
    """获取可用的 Python 命令"""
    for cmd in ["python3", "python"]:
        if check_exe(cmd):
            return cmd
    return None


def _install_nodejs():
    """在 Windows 上安装 Node.js"""
    system = platform.system()
    print(f"    {color(f'系统: {system}，尝试自动安装 Node.js...', '..')}")

    if system == "Windows":
        # 尝试 winget
        winget = check_exe("winget")
        if winget:
            ret = run_cmd("winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements", check=False, capture=False)
            if ret and ret.returncode == 0:
                print(f"    {color('Node.js 安装成功（需重新打开终端）', 'OK')}")
                return
        # 尝试 choco
        choco = check_exe("choco")
        if choco:
            ret = run_cmd("choco install nodejs-lts -y", check=False, capture=False)
            if ret and ret.returncode == 0:
                print(f"    {color('Node.js 安装成功（需重新打开终端）', 'OK')}")
                return
        print(f"    {color('自动安装失败，请手动下载安装: https://nodejs.org', 'FAIL')}")
    elif system == "Linux":
        run_cmd("curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs", capture=False)
    elif system == "Darwin":
        run_cmd("brew install node", capture=False)

    # 重新检查
    if not check_exe("node"):
        print(f"    {color('Node.js 安装后仍需手动确认 PATH', 'WARN')}")
        sys.exit(1)


def _install_python():
    """安装 Python（Windows 下）"""
    system = platform.system()
    if system == "Windows":
        # 尝试从官网下载安装
        print(f"    {color('尝试安装 Python 3...', '..')}")
        ret = run_cmd(
            'winget install -e --id Python.Python.3.13 --accept-source-agreements --accept-package-agreements',
            check=False, capture=False
        )
        if ret and ret.returncode == 0:
            print(f"    {color('Python 安装完成（需重新打开终端）', 'OK')}")
            return
        print(f"    {color('自动安装失败，请手动下载: https://python.org', 'FAIL')}")
        sys.exit(1)


# ==================== 远程环境检查与安装 ====================

def check_remote_env(ssh):
    """通过 SSH 检查远程服务器环境"""
    step("1/6 检查远程服务器环境")

    checks = [
        ("Python3", "command -v python3", "请手动安装: sudo apt install -y python3 python3-pip"),
        ("pip3", "command -v pip3", "请手动安装: sudo apt install -y python3-pip"),
        ("Nginx", "command -v nginx", "sudo apt install -y nginx"),
        ("systemctl", "command -v systemctl", "系统缺少 systemd"),
    ]

    missing = []
    for name, cmd, hint in checks:
        stdin, stdout, stderr = ssh.exec_command(f"bash -c '{cmd}'")
        exit_code = stdout.channel.recv_exit_status()
        if exit_code == 0:
            ver = stdout.read().decode().strip()
            print(f"    {color(f'{name}: {ver}', 'OK')}")
        else:
            print(f"    {color(f'{name} 未安装', 'WARN')}")
            missing.append((name, hint))

    # 尝试自动安装缺失的软件
    if missing:
        print(f"\n    {color('尝试自动安装缺失组件...', '..')}")
        install_cmds = []
        for name, hint in missing:
            if name == "Python3":
                install_cmds.append("sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-pip python3-venv")
            elif name == "pip3":
                install_cmds.append("sudo apt-get install -y -qq python3-pip")
            elif name == "Nginx":
                install_cmds.append("sudo apt-get install -y -qq nginx")
            elif name == "systemctl":
                print(f"    {color('systemd 不可用，请检查服务器系统', 'FAIL')}")
                return False

        if install_cmds:
            for cmd in install_cmds:
                print(f"    {color(f'执行: {cmd}', '..')}")
                stdin, stdout, stderr = ssh.exec_command(cmd)
                exit_code = stdout.channel.recv_exit_status()
                if exit_code == 0:
                    print(f"    {color('安装成功', 'OK')}")
                else:
                    err = stderr.read().decode().strip()[:200]
                    print(f"    {color(f'安装失败: {err}', 'FAIL')}")
                    return False

    # 验证
    stdin, stdout, stderr = ssh.exec_command("python3 --version && pip3 --version && nginx -v 2>&1 | head -1")
    all_ver = stdout.read().decode().strip()
    if "Python" in all_ver and "pip" in all_ver and "nginx" in all_ver:
        print(f"\n    {color('远程环境就绪', 'OK')}")
        return True
    return False


# ==================== 构建 ====================

def build_frontend():
    """构建前端"""
    step("2/6 构建前端")
    ret = os.system(f'cd /d "{FRONTEND_DIR}" && npm run build 2>nul')
    if ret != 0:
        print(f"    {color('前端构建失败', 'FAIL')}")
        sys.exit(1)
    print(f"    {color('前端构建完成', 'OK')}")


def package_project():
    """打包项目"""
    step("3/6 打包项目")

    if TEMP_TAR.exists():
        TEMP_TAR.unlink()

    tar_cmd = (
        f'tar -czf wind-energy-deploy.tar.gz '
        f'--exclude="frontend/node_modules" '
        f'--exclude="frontend/src" '
        f'--exclude="backend/__pycache__" '
        f'--exclude="backend/data/*.db" '
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
        print(f"    {color(f'打包失败: {result.stderr}', 'FAIL')}")
        sys.exit(1)

    if TEMP_TAR.exists():
        size_kb = TEMP_TAR.stat().st_size / 1024
        print(f"    {color(f'打包完成 ({size_kb:.1f} KB)', 'OK')}")
        print(f"      包含: frontend/dist, backend/, deploy/nginx.conf")
    else:
        print(f"    {color('打包文件未生成', 'FAIL')}")
        sys.exit(1)


# ==================== 部署 ====================

def deploy_to_server():
    """上传并部署到服务器"""
    step("4/6 上传到服务器")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS, timeout=10)
        print(f"    {color(f'SSH 连接成功 ({SSH_HOST})', 'OK')}")
    except Exception as e:
        print(f"    {color(f'SSH 连接失败: {e}', 'FAIL')}")
        sys.exit(1)

    # 先检查远程环境
    if not check_remote_env(ssh):
        print(f"    {color('远程环境检查未通过，继续部署（可能部分功能不可用）', 'WARN')}")

    step("5/6 上传部署包")

    try:
        sftp = ssh.open_sftp()
        remote_tar = "/tmp/wind-energy-deploy.tar.gz"
        sftp.put(str(TEMP_TAR), remote_tar)
        sftp.close()
        print(f"    {color('文件上传完成', 'OK')}")
    except Exception as e:
        print(f"    {color(f'上传失败: {e}', 'FAIL')}")
        ssh.close()
        sys.exit(1)

    step("6/6 远程部署")

    deploy_script = f"""#!/bin/bash
set -e

echo '  [..] 创建目录并解压...'
sudo mkdir -p {REMOTE_DIR}
sudo tar -xzf /tmp/wind-energy-deploy.tar.gz -C {REMOTE_DIR}/
echo '  [OK] 解压完成'

echo '  [..] 创建数据目录...'
sudo mkdir -p {REMOTE_DIR}/backend/data

echo '  [..] 安装后端 Python 依赖...'
sudo pip3 install -r {REMOTE_DIR}/backend/requirements.txt -q 2>/dev/null || echo '  [WARN] pip install 跳过'

echo '  [..] 配置 Nginx...'
sudo cp {REMOTE_DIR}/deploy/nginx.conf /etc/nginx/sites-available/wind-energy.conf
sudo ln -sf /etc/nginx/sites-available/wind-energy.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo '  [..] 配置 systemd 服务...'
sudo tee /etc/systemd/system/wind-energy-backend.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=Wind Energy Monitor Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={REMOTE_DIR}/backend
Environment=PYTHONUNBUFFERED=1
ExecStartPre=/bin/mkdir -p {REMOTE_DIR}/backend/data
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
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
sudo systemctl status wind-energy-backend --no-pager | head -6
echo ''
sudo systemctl status nginx --no-pager | head -4
echo ''

echo '  -- API 自检 --'
HTTP_CODE=$(curl -s -o /dev/null -w "%{{http_code}}" http://localhost:8000/health 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo '  [OK] 后端 API 响应正常 (HTTP '$HTTP_CODE')'
else
    echo '  [WARN] 后端 API 未响应 (HTTP '$HTTP_CODE')'
fi

echo ''
echo '  [OK] 部署完成！'
echo '  [WEB]  http://{SSH_HOST}'
echo '  [API]  http://{SSH_HOST}/api/overview'
"""

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
            print(f"    {color(f'部署脚本返回非零退出码 ({exit_code})', 'WARN')}")

    ssh.close()

    # 清理本地临时文件
    if TEMP_TAR.exists():
        TEMP_TAR.unlink()

    print(f"\n{'='*50}")
    print(f"  [SUCCESS] 部署成功！")
    print(f"  [WEB]  http://{SSH_HOST}")
    print(f"  [API]  http://{SSH_HOST}/api/overview")
    print(f"  [DOCS] http://{SSH_HOST}/docs")
    print(f"{'='*50}")


# ==================== 主入口 ====================

if __name__ == "__main__":
    print("")
    print("╔═══════════════════════════════════════════╗")
    print("║     风能监控系统 - 一键部署脚本           ║")
    print("╚═══════════════════════════════════════════╝")
    print(f"  目标服务器: {SSH_HOST}")
    print(f"  项目路径:   {PROJECT_ROOT}")

    check_local_env()
    build_frontend()
    package_project()
    deploy_to_server()
