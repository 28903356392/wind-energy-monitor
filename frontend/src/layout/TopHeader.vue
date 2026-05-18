<template>
  <div class="top-header">
    <div class="top-left">
      <span class="logo-icon">&#9889;</span>
      <span class="logo-text">风能管理</span>
    </div>

    <el-menu
      :default-active="activeRoute"
      mode="horizontal"
      :ellipsis="false"
      :router="true"
      background-color="#0a1628"
      text-color="#a3b1cc"
      active-text-color="#00d4ff"
      class="top-menu"
    >
      <template v-for="item in topMenus" :key="item.id">
        <!-- 有子菜单：下拉 -->
        <el-sub-menu v-if="item.children?.length" :index="item.path || item.name">
          <template #title>
            <el-icon v-if="item.icon"><component :is="item.icon" /></el-icon>
            <span>{{ item.name }}</span>
          </template>
          <el-menu-item v-for="child in item.children" :key="child.id" :index="child.path">
            <el-icon v-if="child.icon"><component :is="child.icon" /></el-icon>
            <span>{{ child.name }}</span>
          </el-menu-item>
        </el-sub-menu>
        <!-- 无子菜单：直接显示 -->
        <el-menu-item v-else :index="item.path">
          <el-icon v-if="item.icon"><component :is="item.icon" /></el-icon>
          <span>{{ item.name }}</span>
        </el-menu-item>
      </template>
    </el-menu>

    <div class="top-right">
      <el-tooltip content="切换左侧菜单" placement="bottom">
        <el-button text @click="userStore.toggleLayout()" style="color: #a3b1cc">
          <el-icon :size="18"><Menu /></el-icon>
        </el-button>
      </el-tooltip>
      <span class="time">{{ currentTime }}</span>
      <el-dropdown trigger="click" @command="handleCommand">
        <span class="user-info">
          <el-icon :size="18"><User /></el-icon>
          {{ userStore.username || 'admin' }}
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout" style="color: #ff6b6b">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/user.js'

const props = defineProps({
  menus: { type: Array, default: () => [] },
})
const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const currentTime = ref('')
let timer

const activeRoute = computed(() => route.path)

// 只显示顶级菜单
const topMenus = computed(() => {
  if (!props.menus?.length) return []
  return [...props.menus].sort((a, b) => a.sort - b.sort)
})

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', { hour12: false })
}

function handleCommand(cmd) {
  if (cmd === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})
onBeforeUnmount(() => clearInterval(timer))
</script>

<style scoped>
.top-header {
  display: flex;
  align-items: center;
  height: 48px;
  background: #0a1628;
  border-bottom: 1px solid rgba(0, 212, 255, 0.08);
  padding: 0 12px;
  flex-shrink: 0;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 110px;
  margin-right: 8px;
}
.logo-icon { font-size: 20px; color: #00d4ff; }
.logo-text { font-size: 14px; font-weight: 700; color: #e0e6ed; letter-spacing: 1px; }

.top-menu {
  flex: 1;
  border-bottom: none !important;
  height: 48px;
  overflow: hidden;
}
:deep(.el-menu--horizontal) { border-bottom: none !important; }
:deep(.el-menu--horizontal > .el-menu-item),
:deep(.el-menu--horizontal > .el-sub-menu .el-sub-menu__title) {
  height: 48px;
  line-height: 48px;
}
:deep(.el-menu--horizontal .el-menu-item.is-active) {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.12), transparent) !important;
  border-bottom: 2px solid #00d4ff !important;
}
:deep(.el-menu--horizontal .el-menu-item:hover),
:deep(.el-menu--horizontal .el-sub-menu__title:hover) {
  background: rgba(0, 212, 255, 0.06) !important;
}

.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  margin-left: 8px;
}
.time { font-size: 12px; color: rgba(255,255,255,0.4); font-family: monospace; white-space: nowrap; }
.user-info {
  display: flex; align-items: center; gap: 4px;
  cursor: pointer; color: #a3b1cc; font-size: 13px;
}
.user-info:hover { color: #00d4ff; }

/* 下拉菜单适配深色主题 */
:deep(.el-menu--horizontal .el-menu--popup) {
  background: #0a1628 !important;
  border: 1px solid rgba(0, 212, 255, 0.1);
}
:deep(.el-menu--horizontal .el-menu--popup .el-menu-item) {
  background: transparent !important;
  color: #a3b1cc;
}
:deep(.el-menu--horizontal .el-menu--popup .el-menu-item:hover) {
  background: rgba(0, 212, 255, 0.06) !important;
  color: #00d4ff;
}
</style>
