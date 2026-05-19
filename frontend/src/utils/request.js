import axios from 'axios'
import { ElMessage } from 'element-plus'
import { API_BASE, REQUEST_TIMEOUT } from '../config/api'
import { STORAGE_KEYS } from '../config/app'

const request = axios.create({
  baseURL: API_BASE,
  timeout: REQUEST_TIMEOUT,
})

// 请求拦截：添加 Token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截：统一错误处理
request.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        localStorage.removeItem(STORAGE_KEYS.TOKEN)
        localStorage.removeItem(STORAGE_KEYS.USER)
        window.location.hash = '#/login'
        ElMessage.error('登录已过期，请重新登录')
      } else if (status === 403) {
        ElMessage.error('权限不足')
      } else {
        ElMessage.error(data?.detail || '请求失败')
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default request
