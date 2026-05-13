/* ============================================================
   Vue Router 配置 —— 一级主屏 + 二级功能页面
   ============================================================ */
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '总览大屏', icon: '📊' },
  },
  {
    path: '/alarms',
    name: 'AlarmCenter',
    component: () => import('../views/AlarmCenter.vue'),
    meta: { title: '告警中心', icon: '🔔' },
  },
  {
    path: '/turbine/:id',
    name: 'TurbineDetail',
    component: () => import('../views/TurbineDetail.vue'),
    meta: { title: '风机详情', icon: '🏭' },
    props: true,
  },
  {
    path: '/energy',
    name: 'EnergyReport',
    component: () => import('../views/EnergyReport.vue'),
    meta: { title: '能源报告', icon: '📈' },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
