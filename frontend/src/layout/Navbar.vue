<template>
  <div class="navbar">
    <div class="navbar-left">
      <el-button text @click="$emit('toggle')" style="color: #a3b1cc">
        <el-icon :size="20"><Fold /></el-icon>
      </el-button>
      <span class="breadcrumb">{{ route.meta?.title }}</span>
    </div>
    <div class="navbar-right">
      <!-- 布局切换 -->
      <el-tooltip :content="userStore.layoutMode === 'left' ? '切换顶部菜单' : '切换左侧菜单'" placement="bottom">
        <el-button text @click="userStore.toggleLayout()" style="color: #a3b1cc">
          <el-icon :size="18">
            <Operation v-if="userStore.layoutMode === 'left'" />
            <Menu v-else />
          </el-icon>
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
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item divided command="logout" style="color: #ff6b6b">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/user.js'

const emit = defineEmits(['toggle'])
const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const currentTime = ref('')
let timer

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
.navbar {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: rgba(10, 22, 40, 0.9);
  border-bottom: 1px solid rgba(0, 212, 255, 0.08);
  flex-shrink: 0;
}
.navbar-left { display: flex; align-items: center; gap: 8px; }
.breadcrumb { font-size: 14px; color: #a3b1cc; }
.navbar-right { display: flex; align-items: center; gap: 16px; }
.time { font-size: 12px; color: rgba(255,255,255,0.4); font-family: monospace; }
.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: #a3b1cc;
  font-size: 13px;
}
.user-info:hover { color: #00d4ff; }
</style>
