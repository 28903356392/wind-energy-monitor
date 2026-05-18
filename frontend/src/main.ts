/* ============================================================
   应用入口 —— TypeScript + Vue3 + Router + Pinia
   ============================================================ */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 全局注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 状态管理
app.use(createPinia())

// UI 库
app.use(ElementPlus, { size: 'default' })

// 路由
app.use(router)

app.mount('#app')
