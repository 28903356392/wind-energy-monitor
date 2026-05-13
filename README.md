# 风电场智能监控平台

> Wind Energy Monitoring System — 大屏数据可视化 + 实时监控 + 告警管理

基于 **Vue 3 + TypeScript + FastAPI + ECharts** 的全栈风电场监控系统，支持大屏总览、实时数据推送、告警管理、风机详情、能源分析等功能。

---

## 目录

- [技术栈](#技术栈)
- [功能总览](#功能总览)
- [快速启动](#快速启动)
- [项目结构](#项目结构)
- [样式适配方案](#样式适配方案)
- [前后端高阶封装](#前后端高阶封装)
- [API 文档](#api-文档)
- [部署指南](#部署指南)

---

## 技术栈

### 前端

| 技术 | 用途 |
|------|------|
| **Vue 3** (Composition API + `<script setup>`) | 前端框架 |
| **TypeScript** | 类型安全 |
| **Vite 6** | 构建工具 |
| **Vue Router 4** | 路由管理（Hash 模式） |
| **Pinia** | 状态管理 |
| **Axios** | HTTP 请求（泛型封装） |
| **ECharts 5** | 图表可视化 |
| **CSS 自定义属性 + clamp()** | 大屏样式适配 |

### 后端

| 技术 | 用途 |
|------|------|
| **FastAPI** | RESTful + WebSocket |
| **SQLAlchemy 2.0** | ORM |
| **SQLite** | 数据库 |
| **Uvicorn** | ASGI 服务器 |
| **WebSocket** | 实时数据推送 |

---

## 功能总览

### 一级大屏 —— 总览仪表盘 `/`

- 核心 KPI 卡片：总功率、日发电量、平均风速、风机统计
- 风机状态列表（点击跳转详情）
- 功率趋势折线图（含风速双 Y 轴）
- 实时风速仪表盘 + 风机状态占比环图
- WebSocket 实时推送数据更新
- 告警未读数角标

### 二级功能页面

| 页面 | 路由 | 功能 |
|------|------|------|
| **告警中心** | `/#/alarms` | 告警统计（严重/警告/提示）、级别筛选、告警事件列表 |
| **风机详情** | `/#/turbine/:id` | 单台风机运行参数、功率柱状图历史趋势 |
| **能源报告** | `/#/energy` | 今日/昨日/本周/本月发电量、功率趋势图、风速-功率散点图、效率指标 |

---

## 快速启动

### 前置条件

- **Node.js** >= 18（推荐 20 LTS）
- **Python** >= 3.10
- **npm** 或 **pnpm**

### 1. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务（监听 8000 端口）
python main.py
```

首次启动会自动创建 SQLite 数据库并填充模拟数据（20 台风机、288 条功率记录、30 条告警、60 条事件日志）。

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（监听 3000 端口，自动代理 /api 到后端）
npm run dev
```

### 3. 访问

| 地址 | 说明 |
|------|------|
| http://localhost:3000 | 大屏首页 |
| http://localhost:3000/#/alarms | 告警中心 |
| http://localhost:3000/#/energy | 能源报告 |
| http://localhost:3000/#/turbine/1 | 风机详情 |
| http://localhost:8000/docs | API 文档（Swagger） |

---

## 项目结构

```
wind-energy-monitor/
├── frontend/                     # Vue 3 前端
│   ├── src/
│   │   ├── main.ts              # 入口（Pinia + Router）
│   │   ├── App.vue              # 根组件（router-view + 全局样式）
│   │   ├── env.d.ts             # TypeScript 声明
│   │   ├── types/
│   │   │   └── index.ts         # 泛型类型、枚举、工具类型
│   │   ├── api/
│   │   │   ├── index.ts         # Axios 泛型封装 + WebSocket 管理器
│   │   │   └── modules.ts       # 按领域拆分的业务 API
│   │   ├── composables/
│   │   │   ├── useClock.ts      # 响应式时钟
│   │   │   ├── useECharts.ts    # ECharts 生命周期 + ResizeObserver
│   │   │   └── useWebSocket.ts  # WebSocket 自动连接/重连
│   │   ├── router/
│   │   │   └── index.ts         # 4 条路由（懒加载）
│   │   ├── components/
│   │   │   ├── StatsCards.vue   # 核心指标卡片
│   │   │   ├── TurbineStatus.vue # 风机状态列表
│   │   │   ├── PowerChart.vue   # 功率趋势图
│   │   │   ├── WindInfo.vue     # 风况信息 + 仪表盘 + 环图
│   │   │   └── common/
│   │   │       └── PanelContainer.vue  # 通用面板容器
│   │   ├── views/
│   │   │   ├── Dashboard.vue    # 总览大屏
│   │   │   ├── AlarmCenter.vue  # 告警中心（二级）
│   │   │   ├── TurbineDetail.vue # 风机详情（二级）
│   │   │   └── EnergyReport.vue # 能源报告（二级）
│   │   └── styles/
│   │       └── variables.css    # CSS 变量（颜色/间距/字号/动画）
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                      # FastAPI 后端
│   ├── main.py                  # 应用入口
│   ├── config.py                # 环境配置
│   ├── database.py              # 数据库初始化 + 种子数据
│   ├── models.py                # ORM 模型
│   ├── mock_data.py             # 实时数据更新任务
│   ├── routers/
│   │   └── wind_farm.py         # API 路由（含 WebSocket）
│   └── requirements.txt
│
├── deploy/                       # 部署脚本
│   ├── deploy.py                # 一键部署脚本（环境检查 + 构建 + 上传 + 部署）
│   ├── deploy.sh                # Bash 部署脚本（备选）
│   └── nginx.conf               # Nginx 反向代理配置
│
└── README.md
```

---

## 样式适配方案

本项目采用 **vw/vh + clamp() + CSS Grid + CSS 自定义属性** 的流式适配方案，专为大屏数据可视化场景设计。

### 核心原则

| 技术 | 说明 |
|------|------|
| `clamp(min, 视口值, max)` | 字号/间距自动缩放，防过小或过大 |
| `vw` / `vh` | 面板尺寸基于视口等比缩放 |
| CSS Grid `fr` 单位 | 面板自动弹性伸缩，无需固定宽高 |
| CSS 自定义属性 (`variables.css`) | 颜色/间距/字号/动画统一管理 |
| `ResizeObserver` | ECharts 图表自适应容器变化 |

### 实现文件

- **`frontend/src/styles/variables.css`** — CSS 变量定义
- **`frontend/src/App.vue`** — 全局样式 + 适配方案说明

> 不依赖媒体查询，基于视口等比缩放，适配各种分辨率的大屏。

---

## 前后端高阶封装

### 前端高级用法

| 模式 | 说明 |
|------|------|
| **泛型 API** `ApiResponse<T>` | 所有接口返回类型安全，编译期就能发现字段错误 |
| **Composables** | `useClock()`、`useECharts()`、`useWebSocket()` 抽取可复用逻辑 |
| **WebSocket 类封装** | `WebSocketManager` 类，自动重连 + 心跳保活 + 事件驱动 |
| **ECharts 组合式封装** | `useECharts(optionRef)`，响应式数据驱动图表更新，`ResizeObserver` 自适应 |
| **defineProps 泛型** | 组件 Props 全类型约束，IDE 智能提示 |
| **TypeScript 枚举 + 映射** | `TurbineStatusEnum` 带中文标签映射表 |
| **路由懒加载** | `() => import(...)` 路由级别代码分割 |

### 后端高级用法

| 模式 | 说明 |
|------|------|
| **lifespan 上下文** | 应用启动/关闭生命周期管理 |
| **WebSocket 连接管理器** | 广播推送 + 断线清理 |
| **SQLAlchemy 2.0 ORM** | 声明式模型 + 类型安全查询 |
| **模拟数据生成器** | 随机游走算法模拟真实传感器数据 |
| **统一响应格式** | `{ code, data, message }` 标准封装 |

---

## API 文档

启动后端后访问 `http://localhost:8000/docs` 查看 Swagger 文档。

### 主要端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/overview` | 风电场总览数据 |
| GET | `/api/turbines` | 风机列表（支持 `?status=` 筛选） |
| GET | `/api/turbines/{id}` | 单台风机详情 |
| GET | `/api/power/history?hours=24` | 功率历史数据 |
| GET | `/api/alarms` | 告警列表（支持 `?level=&acknowledged=`） |
| GET | `/api/alarms/stats` | 告警统计 |
| GET | `/api/events` | 事件日志 |
| GET | `/api/energy/stats` | 能源统计 |
| WS | `/api/ws` | WebSocket 实时推送 |

---

## 部署指南

### 一键部署

```bash
cd /f/ai/wind-energy-monitor
python deploy/deploy.py
```

脚本自动完成：

```
步骤 0/6：本地环境检查（Node/npm/Python/paramiko）
   ├── 缺失则通过 winget/choco 自动安装
步骤 1/6：远程环境检查（Python3/pip3/Nginx/systemctl）
   ├── 缺失则通过 apt-get 自动安装
步骤 2/6：npm run build → 构建前端
步骤 3/6：tar → 打包项目
步骤 4/6：scp → 上传到服务器
步骤 5/6：解压 → 安装依赖 → 配置 Nginx → 配置 systemd 服务
步骤 6/6：API 自检 → 部署完成
```

### 手动部署

```bash
# 1. 构建前端
cd frontend && npm run build

# 2. 上传到服务器
scp -r frontend/dist ubuntu@your-server:/app/workspace/frontend/
scp -r backend ubuntu@your-server:/app/workspace/
scp deploy/nginx.conf ubuntu@your-server:/tmp/

# 3. 服务器端配置（参考 deploy/deploy.py 中的远程部署脚本）
```

### 生产环境访问

| 服务 | 地址 |
|------|------|
| **生产环境** | http://150.158.49.82 |
| **API 文档** | http://150.158.49.82/docs |

### 服务器架构

```
客户端 → Nginx (80端口)
               ├── / → frontend/dist/ (静态文件)
               ├── /api/* → proxy_pass → uvicorn (8000端口)
               └── /api/ws → proxy_pass (WebSocket Upgrade)

systemd: wind-energy-backend.service
         └── uvicorn main:app --port 8000 --workers 1
```

---

## 模拟数据

系统启动时自动生成模拟数据，无需真实风电场传感器：

| 数据 | 数量 | 说明 |
|------|------|------|
| 风机 | 20 台 | 15 运行 + 2 停机 + 2 维护 + 1 故障 |
| 功率记录 | 288 条 | 过去 24 小时，每 5 分钟一个点 |
| 告警记录 | 30 条 | 含 info / warning / critical 级别 |
| 事件日志 | 60 条 | operation / system / alarm 类型 |

实时数据通过随机游走算法模拟传感器波动，WebSocket 每 30 秒推送一次更新，并有 15% 概率推送随机告警。

---

## License

MIT
