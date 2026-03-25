# 智下载系统 - Developer B 任务清单

**版本**: v1.0  
**创建日期**: 2026-03-24  
**负责人**: Developer B（后端核心 + AI + 运维）  
**开发周期**: 8 周 (40 个工作日)  
**计划开始**: 2026-03-25  
**计划结束**: 2026-05-22

---

## 📋 任务总览

| 维度 | 数量 |
|------|------|
| **总任务数** | 32 个 |
| **P0 任务** | 25 个 |
| **P1 任务** | 7 个 |
| **总工时** | ~40 工作日 |

---

## 🎯 Sprint 0: 基础框架 (Week 1, 03/25 ~ 03/31)

### 本周任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T0-02 | 后端项目初始化 | P0 | 1 天 | - | ☐ |
| T0-03 | 数据库设计与迁移 | P0 | 1 天 | T0-02 | ☐ |
| T0-04-B | 用户认证模块（后端部分） | P0 | 1 天 | T0-03 | ☐ |
| T0-05-B | 组织管理 CRUD（后端部分） | P0 | 1 天 | T0-04-B | ☐ |
| T0-07 | API 网关与中间件 | P0 | 1 天 | T0-02 | ☐ |

### 交付物

- [ ] FastAPI 项目可运行
- [ ] SQLite 数据库初始化
- [ ] 用户认证 API（登录/登出/Token）
- [ ] 组织管理 API（CRUD）
- [ ] API 网关与 CORS 中间件

### 接口契约（需与 Developer A 对齐）

| 接口 | 方法 | 请求体 | 响应体 | 对齐日期 |
|------|------|--------|--------|----------|
| `/api/auth/login` | POST | `{username, password}` | `{token, user}` | Day 1 |
| `/api/auth/logout` | POST | - | `{success}` | Day 1 |
| `/api/organizations` | GET | - | `[{id, name, created_at}]` | Day 1 |
| `/api/organizations` | POST | `{name, description}` | `{id, name}` | Day 1 |
| `/api/organizations/:id` | PUT | `{name, description}` | `{success}` | Day 1 |

---

## 🎯 Sprint 1: 核心功能 (上) (Week 2-3, 04/01 ~ 04/14)

### Week 2 任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T1-05 | 流程 CRUD API | P0 | 2 天 | T0-03 | ☐ |
| T1-06 | YAML 解析与生成 | P0 | 2 天 | T1-05 | ☐ |
| T1-09-B | 业务系统管理（后端） | P0 | 2 天 | T0-05-B | ☐ |

### Week 3 任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T1-07-B | 流程保存与加载（后端） | P0 | 1 天 | T1-06 | ☐ |
| T1-10 | 凭证加密存储 | P0 | 2 天 | T1-09-B | ☐ |

### 交付物

- [ ] 流程管理 API（CRUD）
- [ ] YAML 解析与验证
- [ ] 业务系统管理 API
- [ ] 凭证 AES-256 加密存储

### 接口契约（需与 Developer A 对齐）

| 接口 | 方法 | 请求体 | 响应体 | 对齐日期 |
|------|------|--------|--------|----------|
| `/api/workflows` | GET | - | `[{id, name, yaml, updated_at}]` | Day 8 |
| `/api/workflows` | POST | `{name, yaml, nodes}` | `{id, name}` | Day 8 |
| `/api/workflows/:id` | GET | - | `{id, name, yaml, nodes}` | Day 8 |
| `/api/workflows/:id` | PUT | `{name, yaml, nodes}` | `{success}` | Day 8 |
| `/api/workflows/:id` | DELETE | - | `{success}` | Day 8 |
| `/api/business-systems` | GET | - | `[{id, name, url, type}]` | Day 8 |
| `/api/business-systems` | POST | `{name, url, type, credentials}` | `{id}` | Day 8 |

---

## 🎯 Sprint 2: 核心功能 (下) (Week 4-5, 04/15 ~ 04/28)

### Week 4 任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T2-01 | Playwright 浏览器引擎 | P0 | 3 天 | T0-02 | ☐ |
| T2-02 | 拟人化鼠标模拟 | P0 | 2 天 | T2-01 | ☐ |
| T2-05 | LangGraph 工作流引擎 | P0 | 3 天 | T2-01 | ☐ |

### Week 5 任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T2-03 | 拟人化键盘输入 | P0 | 2 天 | T2-01 | ☐ |
| T2-04 | 反检测脚本注入 | P0 | 2 天 | T2-01 | ☐ |
| T2-06 | 任务执行 API | P0 | 2 天 | T2-05 | ☐ |
| T2-08-B | WebSocket 实时推送（后端） | P0 | 1 天 | T2-06 | ☐ |
| T2-09 | 任务调度器 (Cron) | P0 | 2 天 | T2-06 | ☐ |
| T2-10 | 执行日志记录 | P0 | 1 天 | T2-06 | ☐ |

### 交付物

- [ ] Playwright 浏览器自动化引擎
- [ ] 拟人化鼠标移动（贝塞尔曲线/加速度）
- [ ] 拟人化键盘输入（随机间隔/拼写纠正）
- [ ] 反检测脚本（移除 webdriver/隐藏特征）
- [ ] LangGraph 状态机工作流引擎
- [ ] 任务执行 API（启动/停止/状态）
- [ ] WebSocket 实时推送
- [ ] Cron 定时调度器
- [ ] 执行日志记录

### 接口契约（需与 Developer A 对齐）

| 接口 | 方法 | 请求体 | 响应体 | 对齐日期 |
|------|------|--------|--------|----------|
| `WS /ws/tasks/:id` | WebSocket | - | `{step, status, log, screenshot}` | Day 20 |
| `/api/tasks/:id/execute` | POST | - | `{task_id, status}` | Day 20 |
| `/api/tasks/:id/stop` | POST | - | `{success}` | Day 20 |
| `/api/tasks/:id/status` | GET | - | `{status, current_step, progress}` | Day 20 |
| `/api/tasks` | GET | `{org_id, status}` | `[{id, name, status, created_at}]` | Day 20 |
| `/api/schedules` | POST | `{task_id, cron_expression}` | `{schedule_id}` | Day 25 |

---

## 🎯 Sprint 3: AI 功能 (Week 6, 04/29 ~ 05/05)

### 本周任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T3-01 | Ollama Qwen VL 部署 | P0 | 1 天 | - | ☐ |
| T3-02 | 文字描述解析 API | P0 | 2 天 | T3-01 | ☐ |
| T3-03 | 文字生成流程转换 | P0 | 2 天 | T3-02 | ☐ |
| T3-04 | 截图上传与分析 API | P0 | 2 天 | T3-01 | ☐ |
| T3-06 | 标注识别与流程生成 | P0 | 2 天 | T3-04 | ☐ |
| T3-08-B | 文件管理与下载（后端） | P0 | 2 天 | T2-06 | ☐ |

### 交付物

- [ ] Ollama Qwen VL 本地部署
- [ ] 文字描述解析 API（NLP）
- [ ] 文字→YAML 流程转换
- [ ] 截图上传与分析 API
- [ ] 标注识别与流程生成
- [ ] 文件存储管理（按组织/日期分类）

### 接口契约（需与 Developer A 对齐）

| 接口 | 方法 | 请求体 | 响应体 | 对齐日期 |
|------|------|--------|--------|----------|
| `/api/ai/generate-from-text` | POST | `{description, context}` | `{yaml, nodes, confidence}` | Day 30 |
| `/api/ai/analyze-screenshot` | POST | `multipart/form-data` | `{elements, suggestions}` | Day 30 |
| `/api/ai/generate-from-annotation` | POST | `{screenshot_id, annotations}` | `{yaml, nodes}` | Day 30 |
| `/api/files` | GET | `{org_id, date, system_id}` | `[{id, name, size, url, created_at}]` | Day 30 |
| `/api/files/:id/download` | GET | - | `file stream` | Day 30 |

---

## 🎯 Sprint 4: 完善优化 (Week 7, 05/06 ~ 05/12)

### 本周任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T4-01 | 通知系统 (邮件/钉钉) | P1 | 2 天 | T2-06 | ☐ |
| T4-02-B | 验证码处理流程（后端） | P1 | 1 天 | T2-06 | ☐ |
| T4-03 | 异常处理与重试 | P0 | 2 天 | T2-06 | ☐ |
| T4-04-B | 性能优化（后端） | P1 | 1 天 | 全部完成 | ☐ |
| T4-05-B | 系统测试（后端） | P0 | 1 天 | 全部完成 | ☐ |
| T4-06-B | Bug 修复（后端） | P0 | 2 天 | T4-05-B | ☐ |

### 交付物

- [ ] 通知系统（邮件/钉钉/企业微信）
- [ ] 验证码人工处理流程
- [ ] 异常处理与自动重试机制
- [ ] 后端性能优化（数据库/缓存）
- [ ] 后端单元测试覆盖率达到 80%
- [ ] 所有 P0/P1 Bug 修复完成

### 接口契约（需与 Developer A 对齐）

| 接口 | 方法 | 请求体 | 响应体 | 对齐日期 |
|------|------|--------|--------|----------|
| `/api/tasks/:id/captcha` | POST | `{task_id, captcha_code}` | `{success, continued}` | Day 35 |
| `/api/notifications` | POST | `{type, recipient, message}` | `{notification_id}` | Day 35 |

---

## 🎯 Sprint 5: 部署上线 (Week 8, 05/13 ~ 05/22)

### 本周任务

| 任务 ID | 任务名称 | 优先级 | 工时 | 依赖 | 状态 |
|:--------|----------|--------|------|------|------|
| T5-01 | Docker 镜像构建 | P0 | 1 天 | 全部完成 | ☐ |
| T5-02 | Docker Compose 配置 | P0 | 1 天 | T5-01 | ☐ |
| T5-03 | 生产环境部署 | P0 | 2 天 | T5-02 | ☐ |
| T5-04 | 数据迁移脚本 | P0 | 1 天 | T5-03 | ☐ |
| T5-06-B | 上线支持（后端） | P0 | 1 天 | T5-05 | ☐ |
| T5-07 | 项目复盘 | P1 | 1 天 | T5-06 | ☐ |

### 交付物

- [ ] Docker 镜像（前端 + 后端）
- [ ] Docker Compose 配置文件
- [ ] 生产环境部署完成
- [ ] 数据迁移脚本
- [ ] 上线问题响应与修复
- [ ] 项目复盘报告（后端部分）

---

## 📊 每日站会检查清单

### 每日同步（9:30，15 分钟）

- [ ] 昨日完成内容
- [ ] 今日计划内容
- [ ] 是否有阻塞问题
- [ ] 接口是否需要变更

### 接口变更通知

如需变更已对齐的接口，必须：
1. 提前通知 Developer A
2. 更新本文档的接口契约部分
3. 确认对方已适配后再提交代码

---

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.109+ |
| 数据库 | SQLite | 3.x |
| ORM | SQLAlchemy | 2.x |
| 浏览器自动化 | Playwright | 1.40+ |
| 工作流引擎 | LangGraph | 0.1+ |
| AI 模型 | Qwen VL (Ollama) | 最新 |
| WebSocket | Starlette WebSocket | - |
| 任务调度 | APScheduler | 3.x |
| 加密 | cryptography | 41.x |
| 容器化 | Docker | 最新 |

---

## 📁 代码目录结构

```
smart-downloader/backend/
├── app/
│   ├── api/               # API 路由
│   │   ├── auth.py        # 认证接口
│   │   ├── organizations.py # 组织接口
│   │   ├── workflows.py   # 流程接口
│   │   ├── tasks.py       # 任务接口
│   │   ├── files.py       # 文件接口
│   │   └── ai.py          # AI 接口
│   ├── core/              # 核心模块
│   │   ├── config.py      # 配置管理
│   │   ├── security.py    # 安全认证
│   │   └── encryption.py  # 加密模块
│   ├── db/                # 数据库
│   │   ├── models.py      # 数据模型
│   │   ├── schemas.py     # 数据 Schema
│   │   └── migrations/    # 迁移脚本
│   ├── engines/           # 引擎模块
│   │   ├── playwright_engine.py # 浏览器引擎
│   │   ├── langgraph_engine.py # 工作流引擎
│   │   └── human_behavior.py   # 拟人化行为
│   ├── ai/                # AI 模块
│   │   ├── qwen_vl.py     # Qwen VL 集成
│   │   ├── text_parser.py # 文字解析
│   │   └── image_analyzer.py # 图像分析
│   ├── services/          # 服务层
│   │   ├── task_service.py # 任务服务
│   │   ├── file_service.py # 文件服务
│   │   └── notify_service.py # 通知服务
│   └── utils/             # 工具函数
├── tests/                 # 测试文件
├── docker/                # Docker 配置
└── docs/                  # 后端文档
```

---

## ✅ 完成定义 (DoD)

每个任务完成前必须满足：

- [ ] 代码通过 mypy 类型检查
- [ ] 代码通过 Pylint 检查（>9 分）
- [ ] 单元测试通过（覆盖率>80%）
- [ ] API 测试通过
- [ ] 功能在本地验证
- [ ] 代码审查通过

---

## 📞 联系方式

| 角色 | 负责人 | 联系方式 |
|------|--------|----------|
| Developer A | TBD | TBD |
| Developer B | TBD | TBD |
| 产品经理 | TBD | TBD |
| 技术负责人 | TBD | TBD |

---

**文档结束**
