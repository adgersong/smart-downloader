# 智下载前端 - 依赖问题解决方案

## 问题分析

### 当前遇到的问题

1. **Umi 配置错误**
   - `@umijs/max` 与 `umi` 版本不匹配
   - 配置文件使用了 `@umijs/max` 但缺少对应依赖

2. **Ant Design 组件缺失**
   - `antd` 未安装导致 UI 组件不可用
   - `@ant-design/pro-components` 缺失

3. **路由配置不完整**
   - Dashboard 路由未定义
   - 缺少布局组件配置

4. **MFSU 编译错误**
   - 模块热更新导致缓存问题
   - 端口冲突

---

## 解决方案

### 方案一：最小化配置（推荐）

使用简化的 Umi 配置，减少依赖：

#### 1. 修改 `.umirc.ts`

```typescript
import { defineConfig } from 'umi';

export default defineConfig({
  routes: [
    { path: '/login', component: './Login' },
    { path: '/dashboard', component: './Dashboard' },
    { path: '/', redirect: '/dashboard' },
  ],
  npmClient: 'npm',
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
});
```

#### 2. 安装最小依赖

```bash
cd frontend
npm install umi react react-dom --save
```

#### 3. 清理缓存

```bash
rm -rf src/.umi node_modules/.cache
```

---

### 方案二：完整 Ant Design Pro 配置

使用完整的 Ant Design Pro 功能：

#### 1. 修改 `.umirc.ts`

```typescript
import { defineConfig } from '@umijs/max';

export default defineConfig({
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  layout: {
    title: '智下载 SmartDownloader',
    theme: 'dark',
  },
  routes: [
    { path: '/login', component: './Login' },
    { 
      path: '/', 
      component: './layouts/SecurityLayout',
      routes: [
        { path: '/', redirect: '/dashboard' },
        { path: '/dashboard', component: './Dashboard' },
        { path: '/organization', component: './Organization' },
        { path: '/system', component: './System' },
        { path: '/task', component: './Task' },
        { path: '/file', component: './File' },
      ]
    },
  ],
  npmClient: 'npm',
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
});
```

#### 2. 安装完整依赖

```bash
cd frontend

# 安装核心框架
npm install @umijs/max umi --save

# 安装 Ant Design 组件
npm install antd @ant-design/icons @ant-design/pro-components --save

# 安装状态管理
npm install zustand --save
```

#### 3. 清理并重启

```bash
# 停止所有服务
pkill -f "umi dev"
pkill -f uvicorn

# 清理缓存
rm -rf src/.umi node_modules/.cache dist

# 重启后端
cd ../backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 重启前端
cd ../frontend
npm run dev
```

---

## 端口管理

### 常见问题

端口被占用导致服务无法启动。

### 解决方案

#### 1. 查看端口占用

```bash
# 查看指定端口
lsof -i :8000 -i :8001 -i :3000

# 查看所有 Node 进程
ps aux | grep node
```

#### 2. 关闭占用进程

```bash
# 关闭特定进程
kill -9 <PID>

# 或关闭所有相关进程
pkill -9 -f "umi dev"
pkill -9 -f uvicorn
pkill -9 -f "node.*frontend"
```

#### 3. 指定端口启动

```bash
# 前端指定端口
PORT=3000 npm run dev

# 后端指定端口
python3 -m uvicorn app.main:app --port 8000
```

---

## 依赖管理最佳实践

### 1. 锁定依赖版本

在 `package.json` 中指定确切版本：

```json
{
  "dependencies": {
    "umi": "^4.0.0",
    "@umijs/max": "^4.0.0",
    "antd": "^5.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "zustand": "^4.0.0"
  }
}
```

### 2. 使用 package-lock.json

```bash
# 提交 lock 文件到 git
git add package-lock.json
git commit -m "chore: add package lock file"
```

### 3. 安装依赖时

```bash
# 使用 ci 命令（推荐）
npm ci

# 或 clean install
npm clean-install
```

---

## 快速启动脚本

创建 `start.sh`：

```bash
#!/bin/bash

# 智下载 - 快速启动脚本
set -e

echo "🚀 智下载 SmartDownloader - 启动中..."

# 清理旧进程
pkill -f "umi dev" 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true
sleep 2

# 清理缓存
cd frontend
rm -rf src/.umi node_modules/.cache 2>/dev/null || true

# 启动后端
cd ../backend
echo "启动后端..."
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
sleep 3

# 检查后端
curl -s http://localhost:8000/health > /dev/null && echo "✅ 后端启动成功" || echo "❌ 后端启动失败"

# 启动前端
cd ../frontend
echo "启动前端..."
nohup npm run dev > /tmp/frontend.log 2>&1 &
sleep 30

# 检查前端
curl -s http://localhost:8001 > /dev/null && echo "✅ 前端启动成功" || echo "⚠️ 前端启动中..."

echo ""
echo "====================================="
echo "服务已启动:"
echo "  后端：http://localhost:8000"
echo "  前端：http://localhost:8001"
echo "  API 文档：http://localhost:8000/api/docs"
echo "====================================="
```

使用：

```bash
chmod +x start.sh
./start.sh
```

---

## 故障排查清单

### 前端无法启动

- [ ] 检查 Node.js 版本（推荐 18+）
- [ ] 清理缓存 `rm -rf node_modules/.cache`
- [ ] 重新安装依赖 `npm install`
- [ ] 检查端口占用 `lsof -i :8001`

### 后端无法启动

- [ ] 检查 Python 版本（推荐 3.10+）
- [ ] 安装依赖 `pip install -r requirements.txt`
- [ ] 检查端口占用 `lsof -i :8000`
- [ ] 查看日志 `tail /tmp/backend.log`

### 页面空白

- [ ] 清空浏览器缓存（Cmd+Shift+R）
- [ ] 检查浏览器控制台错误
- [ ] 确认后端服务运行
- [ ] 检查代理配置

### 路由不匹配

- [ ] 检查 `.umirc.ts` 路由配置
- [ ] 清理 Umi 缓存 `rm -rf src/.umi`
- [ ] 重启开发服务器

---

## 推荐的开发环境配置

### 系统要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Node.js | 18.x+ | 前端运行时 |
| Python | 3.10+ | 后端运行时 |
| npm | 9.x+ | 包管理器 |

### VS Code 插件推荐

- ESLint
- Prettier
- Ant Design Vue helper
- Python
- Thunder Client（API 测试）

### 浏览器推荐

- Chrome（开发首选）
- Firefox
- Edge

---

## 总结

### 避免依赖问题的关键

1. **锁定版本** - 使用确切版本号
2. **清理缓存** - 定期清理 `.umi` 和 `node_modules/.cache`
3. **端口管理** - 启动前检查端口占用
4. **配置文件一致** - 确保 `.umirc.ts` 与安装的依赖匹配
5. **使用脚本** - 用启动脚本统一管理流程

### 快速参考

```bash
# 完整重启流程
pkill -f "umi dev"; pkill -f uvicorn
cd frontend && rm -rf src/.umi node_modules/.cache
cd ../backend && python3 -m uvicorn app.main:app --port 8000 &
cd ../frontend && npm run dev
```

---

**文档版本**: v1.0  
**更新日期**: 2026-03-24
