/* ============================================================
   应用入口 —— TypeScript + Vue3 + Router + Pinia
   ============================================================ */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 状态管理
app.use(createPinia())

// 路由
app.use(router)

app.mount('#app')
