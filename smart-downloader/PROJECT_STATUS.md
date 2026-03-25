# 智下载系统 - 项目运行状态

**启动时间**: $(date '+%Y-%m-%d %H:%M:%S')  
**状态**: ✅ 运行中

---

## 服务状态

| 服务 | 状态 | 端口 | 访问地址 |
|------|------|------|----------|
| 后端 API | ✅ 运行中 | 8000 | http://localhost:8000 |
| 前端页面 | ✅ 运行中 | 8000 | http://localhost:8000 |
| API 文档 | ✅ 可用 | 8000 | http://localhost:8000/api/docs |
| 测试守护进程 | ✅ 运行中 | - | 每 5 分钟执行 |

---

## 进程信息

- **后端 PID**: $(pgrep -f "uvicorn.*app.main" | head -1)
- **前端 PID**: $(pgrep -f "umi.*dev" | head -1)
- **测试守护 PID**: $(cat tests/test_daemon.pid 2>/dev/null || echo "未运行")

---

## 测试执行计划

守护进程每 5 分钟自动执行一次完整测试：

1. ✅ 后端单元测试 (模型/数据库)
2. ✅ API 接口测试 (REST API)
3. ✅ 集成测试 (前后端集成)
4. ✅ 交互测试 (完整用户流程)
5. ✅ E2E 测试 (Playwright 有头浏览器)

---

## 监控命令

```bash
# 查看测试日志
tail -f /Users/songyanjie/opentest/00Bank_down/smart-downloader/tests/daemon-test.log

# 查看后端日志
tail -f /tmp/backend.log

# 查看前端日志
tail -f /tmp/frontend.log

# 查看测试守护进程状态
ps -p $(cat tests/test_daemon.pid)

# 停止测试守护
kill $(cat tests/test_daemon.pid)

# 重启测试守护
pkill -f test_daemon.py
nohup python3 tests/test_daemon.py > tests/daemon-test.log 2>&1 &
```

---

## 停止服务

```bash
# 停止所有服务
pkill -f "uvicorn.*app.main"
pkill -f "umi.*dev"
pkill -f test_daemon.py

echo "✅ 所有服务已停止"
```

---

**最后更新**: $(date '+%Y-%m-%d %H:%M:%S')
