# 智下载后端

基于 FastAPI + LangGraph + Playwright 的浏览器自动化后端服务。

## 技术栈

- **框架**: FastAPI 0.100+
- **ORM**: SQLAlchemy 2.x
- **数据库**: SQLite 3.x (可迁移 PostgreSQL)
- **工作流引擎**: LangGraph
- **浏览器自动化**: Playwright 1.40+
- **AI 模型**: Qwen VL (via Ollama)
- **加密**: cryptography 41.x

## 快速开始

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问 API 文档
# http://localhost:8000/docs
```

## 目录结构

```
app/
├── api/                # API 路由
│   └── v1/
│       ├── auth.py     # 认证
│       ├── org.py      # 组织
│       ├── system.py   # 业务系统
│       ├── workflow.py # 流程
│       ├── task.py     # 任务
│       └── file.py     # 文件
├── services/           # 业务服务
├── core/               # 核心模块
│   ├── engine/
│   │   ├── workflow_engine.py
│   │   ├── browser_engine.py
│   │   ├── vision_engine.py
│   │   ├── human_simulator.py
│   │   └── anti_detection.py
│   └── security/
│       ├── crypto.py
│       └── rbac.py
├── models/             # 数据模型
├── schemas/            # Pydantic 模型
├── db/                 # 数据库
│   ├── database.py
│   └── crud.py
└── main.py             # 应用入口
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/login | 用户登录 |
| GET | /api/v1/organizations | 组织列表 |
| POST | /api/v1/organizations | 创建组织 |
| GET | /api/v1/workflows | 流程列表 |
| POST | /api/v1/workflows/generate | AI 生成流程 |
| POST | /api/v1/tasks/execute | 执行任务 |
| WS | /ws/tasks/{id} | 任务实时推送 |

## 配置

复制 `.env.example` 到 `.env` 并修改配置：

```bash
# 数据库
DATABASE_URL=sqlite:///./data/app.db

# Ollama 服务
OLLAMA_URL=http://localhost:11434

# 加密密钥
SECRET_KEY=your-secret-key-here

# 文件存储
FILE_STORAGE_PATH=./data/files
SCREENSHOT_PATH=./data/screenshots
```

## 开发规范

- 使用 Python 3.10+
- 遵循 PEP 8 规范
- 使用 mypy 进行类型检查
- 使用 pytest 编写测试

## 相关链接

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Playwright](https://playwright.dev/)
- [Ollama](https://ollama.ai/)
- [Qwen VL](https://github.com/QwenLM/Qwen-VL)
