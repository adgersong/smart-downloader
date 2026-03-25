# 智下载 SmartDownloader

智能浏览器自动化下载系统

## 🚀 快速启动

```bash
# 启动所有服务
cd /Users/songyanjie/opentest/00Bank_down/smart-downloader

# 后端服务
cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 前端服务
cd frontend && npm run dev &

# 测试守护进程
cd .. && python3 tests/test_daemon.py &
```

## 📁 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:8001 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/api/docs |

## 🧪 测试系统

测试守护进程每 5 分钟自动执行一次完整测试：

- ✅ 后端单元测试
- ✅ API 接口测试
- ✅ 集成测试
- ✅ 交互测试

### 查看测试日志

```bash
tail -f tests/daemon-test.log
```

### 重启测试守护

```bash
pkill -f test_daemon.py
nohup python3 tests/test_daemon.py > tests/daemon-test.log 2>&1 &
```

## 📊 项目结构

```
smart-downloader/
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/    # API 路由
│   │   ├── models/    # 数据模型
│   │   └── main.py    # 应用入口
│   └── requirements.txt
├── frontend/          # Umi + Ant Design Pro 前端
│   └── src/
│       ├── pages/     # 页面组件
│       └── layouts/   # 布局组件
└── tests/             # 测试脚本
    ├── run_all_tests.sh
    ├── test_daemon.py
    ├── test_backend_unit.py
    ├── test_api.py
    ├── test_integration.py
    └── test_interactive.py
```

## 🛠️ 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Umi 4 + Ant Design Pro 5 + React 18
- **测试**: Python unittest + Playwright
- **自动化**: Playwright + LangGraph

---

**状态**: ✅ 运行中
**最后更新**: $(date '+%Y-%m-%d %H:%M:%S')
