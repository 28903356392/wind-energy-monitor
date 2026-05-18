<template>
  <div class="sidebar" :class="{ collapsed }">
    <div class="logo">
      <span class="logo-icon">&#9889;</span>
      <span v-show="!collapsed" class="logo-text">风能管理</span>
    </div>
    <el-scrollbar class="menu-scroll">
      <el-menu
        :default-active="activeRoute"
        :collapse="collapsed"
        :router="true"
        background-color="#0a1628"
        text-color="#a3b1cc"
        active-text-color="#00d4ff"
        unique-opened
      >
        <template v-for="item in menuTree" :key="item.id">
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
          <el-menu-item v-else :index="item.path">
            <el-icon v-if="item.icon"><component :is="item.icon" /></el-icon>
            <span>{{ item.name }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  menus: { type: Array, default: () => [] },
  collapsed: { type: Boolean, default: false },
})
const route = useRoute()
const activeRoute = computed(() => route.path)

const menuTree = computed(() => {
  // API 已返回树形结构，直接用
  return sortTree(props.menus)
})

function sortTree(items) {
  if (!items || !items.length) return []
  return [...items]
    .sort((a, b) => a.sort - b.sort)
    .map((m) => ({
      ...m,
      children: m.children ? sortTree(m.children) : [],
    }))
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  background: #0a1628;
  border-right: 1px solid rgba(0, 212, 255, 0.08);
  transition: width 0.3s;
  z-index: 100;
  overflow: hidden;
}
.sidebar.collapsed {
  width: 64px;
}
.logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-bottom: 1px solid rgba(0, 212, 255, 0.08);
}
.logo-icon { font-size: 24px; color: #00d4ff; }
.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: #e0e6ed;
  letter-spacing: 2px;
}
.menu-scroll {
  height: calc(100vh - 56px);
}
:deep(.el-menu) { border-right: none; }
:deep(.el-sub-menu__title:hover),
:deep(.el-menu-item:hover) { background-color: rgba(0, 212, 255, 0.06); }
:deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(0, 212, 255, 0.12), transparent);
  border-right: 3px solid #00d4ff;
}
</style>
