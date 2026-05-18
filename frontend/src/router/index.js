import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue'),
    meta: { title: '登录', noAuth: true },
  },
  {
    path: '/',
    component: () => import('../layout/AdminLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/Dashboard.vue'),
        meta: { title: '风能大屏', icon: 'Monitor' },
      },
      {
        path: 'system/user',
        name: 'UserList',
        component: () => import('../views/system/user/UserList.vue'),
        meta: { title: '用户管理', icon: 'User', permission: 'system:user:list' },
      },
      {
        path: 'system/role',
        name: 'RoleList',
        component: () => import('../views/system/role/RoleList.vue'),
        meta: { title: '角色管理', icon: 'UserFilled', permission: 'system:role:list' },
      },
      {
        path: 'system/menu',
        name: 'MenuList',
        component: () => import('../views/system/menu/MenuList.vue'),
        meta: { title: '菜单管理', icon: 'Menu', permission: 'system:menu:list' },
      },
      {
        path: 'system/dict',
        name: 'DictList',
        component: () => import('../views/system/dict/DictList.vue'),
        meta: { title: '字典管理', icon: 'Reading', permission: 'system:dict:list' },
      },
      {
        path: 'monitor/login-log',
        name: 'LoginLog',
        component: () => import('../views/monitor/LoginLog.vue'),
        meta: { title: '登录日志', icon: 'Lock', permission: 'monitor:login:list' },
      },
      {
        path: 'monitor/operation-log',
        name: 'OperationLog',
        component: () => import('../views/monitor/OperationLog.vue'),
        meta: { title: '操作日志', icon: 'List', permission: 'monitor:operation:list' },
      },
      {
        path: 'monitor/system',
        name: 'SystemMonitor',
        component: () => import('../views/monitor/SystemMonitor.vue'),
        meta: { title: '系统监控', icon: 'DataBoard', permission: 'monitor:system:list' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 风能管理系统` : '风能管理系统'
  if (to.meta.noAuth) {
    next()
  } else {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
