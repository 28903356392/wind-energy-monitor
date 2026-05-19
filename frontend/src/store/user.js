import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '../utils/request.js'
import { STORAGE_KEYS, DEFAULT_LAYOUT_MODE } from '../config/app'
import { AUTH } from '../config/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem(STORAGE_KEYS.TOKEN) || '')
  const userInfo = ref(JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || '{}'))
  const permissions = ref([])
  const menus = ref([])

  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.nickname || userInfo.value?.username || '')

  // 布局模式: 'left' | 'top'
  const layoutMode = ref(localStorage.getItem(STORAGE_KEYS.LAYOUT_MODE) || DEFAULT_LAYOUT_MODE)
  function toggleLayout() {
    layoutMode.value = layoutMode.value === 'left' ? 'top' : 'left'
    localStorage.setItem(STORAGE_KEYS.LAYOUT_MODE, layoutMode.value)
  }

  async function login(loginData) {
    const res = await request.post(AUTH.LOGIN, loginData)
    const data = res.data.data
    token.value = data.token
    userInfo.value = data.user
    localStorage.setItem(STORAGE_KEYS.TOKEN, data.token)
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(data.user))
    return data
  }

  async function fetchUserInfo() {
    const res = await request.get(AUTH.USERINFO)
    userInfo.value = res.data.data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(res.data.data))
  }

  async function fetchMenus() {
    const res = await request.get(AUTH.MENUS)
    menus.value = res.data.data
  }

  function logout() {
    token.value = ''
    userInfo.value = {}
    permissions.value = []
    menus.value = []
    localStorage.removeItem(STORAGE_KEYS.TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
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
