import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '../utils/request.js'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
  const permissions = ref([])
  const menus = ref([])

  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.nickname || userInfo.value?.username || '')

  // 布局模式: 'left' | 'top'
  const layoutMode = ref(localStorage.getItem('layoutMode') || 'left')
  function toggleLayout() {
    layoutMode.value = layoutMode.value === 'left' ? 'top' : 'left'
    localStorage.setItem('layoutMode', layoutMode.value)
  }

  async function login(loginData) {
    const res = await request.post('/auth/login', loginData)
    const data = res.data.data
    token.value = data.token
    userInfo.value = data.user
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    return data
  }

  async function fetchUserInfo() {
    const res = await request.get('/auth/userinfo')
    userInfo.value = res.data.data
    localStorage.setItem('user', JSON.stringify(res.data.data))
  }

  async function fetchMenus() {
    const res = await request.get('/auth/menus')
    menus.value = res.data.data
  }

  function logout() {
    token.value = ''
    userInfo.value = {}
    permissions.value = []
    menus.value = []
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 按钮级权限检查
  function hasPermission(perm) {
    if (userInfo.value?.is_admin) return true
    return (userInfo.value?.permissions || []).includes(perm)
  }

  return {
    token, userInfo, permissions, menus,
    isLoggedIn, username, layoutMode,
    login, fetchUserInfo, fetchMenus, logout, hasPermission, toggleLayout,
  }
})
