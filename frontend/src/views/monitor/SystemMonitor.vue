<template>
  <div class="monitor-page">
    <el-row :gutter="12">
      <el-col :span="8" v-for="item in infoList" :key="item.label">
        <div class="info-card">
          <div class="info-label">{{ item.label }}</div>
          <div class="info-value">{{ item.value }}</div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="12" style="margin-top:12px">
      <el-col :span="8">
        <div class="panel">
          <div class="panel-title">CPU</div>
          <div class="progress-wrap"><span>{{ cpu?.percent }}%</span><el-progress :percentage="cpu?.percent||0" :stroke-width="12" color="#00d4ff" /></div>
          <div style="margin-top:8px;font-size:12px;color:rgba(255,255,255,.4)">
            <span>核心: {{ cpu?.physical_cores }}({{ cpu?.cores }}线程)</span>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel">
          <div class="panel-title">内存</div>
          <div class="progress-wrap"><span>{{ memory?.percent }}%</span><el-progress :percentage="memory?.percent||0" :stroke-width="12" color="#00ff88" /></div>
          <div style="margin-top:8px;font-size:12px;color:rgba(255,255,255,.4)">
            <span>{{ formatBytes(memory?.used) }} / {{ formatBytes(memory?.total) }}</span>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel">
          <div class="panel-title">磁盘</div>
          <div class="progress-wrap"><span>{{ disk?.percent }}%</span><el-progress :percentage="disk?.percent||0" :stroke-width="12" color="#ffd93d" /></div>
          <div style="margin-top:8px;font-size:12px;color:rgba(255,255,255,.4)">
            <span>{{ formatBytes(disk?.used) }} / {{ formatBytes(disk?.total) }}</span>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request.js'

const cpu = ref({}), memory = ref({}), disk = ref({})
const infoList = ref([])

function formatBytes(bytes) {
  if (!bytes) return '0 B'
  const gb = bytes / (1024**3)
  return gb.toFixed(1) + ' GB'
}

async function loadData() {
  try {
    const res = await request.get('/system/monitor')
    const d = res.data.data
    cpu.value = d.cpu
    memory.value = d.memory
    disk.value = d.disk
    infoList.value = [
      { label: '操作系统', value: d.os },
      { label: '主机名', value: d.hostname },
      { label: 'Python版本', value: d.python_version },
    ]
  } catch { /* ignore */ }
}
onMounted(loadData)
</script>
<style scoped>
.monitor-page { padding:4px; }
.info-card { background:rgba(10,22,40,.6); border:1px solid rgba(0,212,255,.1); border-radius:6px; padding:14px 16px; text-align:center; }
.info-label { font-size:12px; color:rgba(255,255,255,.4); }
.info-value { font-size:16px; color:#e0e6ed; font-weight:600; margin-top:4px; }
.panel { background:rgba(10,22,40,.6); border:1px solid rgba(0,212,255,.1); border-radius:6px; padding:16px; }
.panel-title { color:#00d4ff; font-size:13px; font-weight:600; margin-bottom:12px; }
.progress-wrap { display:flex; align-items:center; gap:8px; }
.progress-wrap span { font-family:monospace; color:#e0e6ed; white-space:nowrap; }
.progress-wrap :deep(.el-progress) { flex:1; }
.progress-wrap :deep(.el-progress-bar__outer) { background:rgba(255,255,255,.05); }
</style>
