<template>
  <!-- 左侧菜单模式 -->
  <div v-if="userStore.layoutMode === 'left'" class="admin-layout">
    <Sidebar :menus="menus" :collapsed="collapsed" />
    <div class="main-area" :class="{ expanded: collapsed }">
      <Navbar :menus="menus" :layout-mode="'left'" @toggle="collapsed = !collapsed" />
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>

  <!-- 顶部菜单模式 -->
  <div v-else class="top-layout">
    <TopHeader :menus="menus" />
    <div class="top-main">
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../store/user.js'
import Sidebar from './Sidebar.vue'
import Navbar from './Navbar.vue'
import TopHeader from './TopHeader.vue'

const userStore = useUserStore()
const collapsed = ref(false)
const menus = ref([])

onMounted(async () => {
  try {
    await userStore.fetchUserInfo()
    await userStore.fetchMenus()
    menus.value = userStore.menus
  } catch (e) {
    console.error('加载菜单失败:', e)
  }
})
</script>

<style scoped>
/* 左侧模式 */
.admin-layout {
  display: flex;
  height: 100vh;
  background: #0a1628;
  color: #e0e6ed;
}
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 220px;
  transition: margin-left 0.3s;
  overflow: hidden;
}
.main-area.expanded {
  margin-left: 64px;
}

/* 顶部模式 */
.top-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0d1b36;
  color: #e0e6ed;
}
.top-main {
  flex: 1;
  overflow: auto;
  padding-top: 0;
}

/* 公共 */
.content {
  flex: 1;
  padding: 16px;
  overflow: auto;
  background: #0d1b36;
}
</style>
