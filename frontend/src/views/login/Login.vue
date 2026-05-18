<template>
  <div class="login-page">
    <div class="login-bg"></div>
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">&#9889;</div>
        <h2>风能管理系统</h2>
        <p>Wind Energy Management Platform</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" @keyup.enter="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" size="large">
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" class="login-btn" @click="handleLogin">
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-footer">
        <span>默认账号: admin / admin123</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../../store/user.js'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({ username: 'admin', password: 'admin123' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    // 错误已在 request 拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: #020d1f;
  overflow: hidden;
}
.login-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(0, 255, 136, 0.04) 0%, transparent 50%);
}
.login-card {
  position: relative;
  width: 400px;
  padding: 40px;
  background: rgba(10, 22, 40, 0.85);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(20px);
}
.login-header { text-align: center; margin-bottom: 32px; }
.login-icon { font-size: 48px; color: #00d4ff; }
.login-header h2 { color: #e0e6ed; font-size: 22px; margin: 8px 0 4px; }
.login-header p { color: rgba(255,255,255,0.3); font-size: 12px; letter-spacing: 2px; }
:deep(.el-input__wrapper) {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(0, 212, 255, 0.1);
  box-shadow: none;
}
:deep(.el-input__inner) { color: #e0e6ed; }
:deep(.el-input__prefix) { color: rgba(255,255,255,0.3); }
.login-btn {
  width: 100%;
  height: 42px;
  font-size: 15px;
  letter-spacing: 4px;
  background: linear-gradient(90deg, #00b4d8, #00d4ff);
  border: none;
}
.login-btn:hover { background: linear-gradient(90deg, #00d4ff, #00ff88); }
.login-footer {
  margin-top: 16px;
  text-align: center;
  font-size: 11px;
  color: rgba(255,255,255,0.25);
}
</style>
