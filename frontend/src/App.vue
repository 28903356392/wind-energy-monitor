<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup lang="ts">
// App 根组件 —— 使用 router-view 驱动页面切换
</script>

<style>
/* ============================================================
   样式适配方案说明：
   本项目使用 vw/vh + clamp() + CSS Grid + CSS 自定义属性
   实现大屏数据可视化场景的流式适配。

   适配策略：
   1. 尺寸单位：使用 clamp(最小值, 视口比例, 最大值) 实现流体排版
   2. 布局方式：CSS Grid 的 fr 单位 + 固定列宽 clamp() 组合
   3. 主题管理：CSS 自定义属性 (variables.css) 统一管理颜色/间距/字号
   4. 图表适配：ECharts 配合 ResizeObserver 自动 resize
   5. 无需媒体查询，基于视口等比缩放
   ============================================================ */

@import './styles/variables.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  height: 100%;
}

/* 过渡动画已在 variables.css 中定义 (.fade-, .slide-fade-) */
</style>
