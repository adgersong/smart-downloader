# 智能测试技能系统

独立可复用的测试技能配置，支持环境守护、E2E 自动化测试和持续修复闭环。

## 目录结构

```
skills/
├── environment-sentinel/    # 环境预检与自愈守护
│   ├── scripts/
│   │   └── env_sentinel.py  # 守护进程脚本
│   ├── config/              # 配置文件
│   ├── reports/             # 检查报告
│   └── logs/                # 日志文件
│
├── e2e-testing/             # 全链路自动化测试
│   ├── scripts/
│   │   └── e2e_master.py    # E2E 测试主程序
│   ├── test-cases/          # 测试用例
│   ├── reports/             # 测试报告
│   └── screenshots/         # 截图证据
│
└── README.md                # 本文档
```

## 技能 1: 环境预检与自愈守护

### 功能特性

- ✅ 端口冲突自动检测与释放 (3 分钟采样率)
- ✅ 依赖完整性校验与自动修复
- ✅ 服务健康检查与自动重启
- ✅ 环境变量自动补偿
- ✅ 实时日志与报告生成

### 使用方式

```bash
# 启动守护进程
python3 skills/environment-sentinel/scripts/env_sentinel.py --start

# 查看状态
python3 skills/environment-sentinel/scripts/env_sentinel.py --status

# 手动检查
python3 skills/environment-sentinel/scripts/env_sentinel.py --check

# 指定项目路径
python3 skills/environment-sentinel/scripts/env_sentinel.py --check --path /path/to/project
```

### 配置项

编辑 `skills/environment-sentinel/scripts/env_sentinel.py`:

```python
CONFIG = {
    "services": {
        "backend": {"port": 8000, "name": "后端 API"},
        "frontend": {"port": 8001, "name": "前端页面"},
    },
    "check_interval": 180,  # 检查间隔 (秒)
}
```

## 技能 2: 全链路自动化测试

### 功能特性

- ✅ 多因子身份鉴权自动化
- ✅ PRD 标准化功能巡检
- ✅ 深度 CRUD 验证
- ✅ 故障溯源与智能分析
- ✅ 截图与日志自动捕获
- ✅ 测试报告自动生成

### 使用方式

```bash
# 完整测试
python3 skills/e2e-testing/scripts/e2e_master.py --full

# 仅测试登录
python3 skills/e2e-testing/scripts/e2e_master.py --login

# 仅 CRUD 测试
python3 skills/e2e-testing/scripts/e2e_master.py --crud

# 查看最新报告
python3 skills/e2e-testing/scripts/e2e_master.py --report
```

### 测试配置

编辑 `skills/e2e-testing/scripts/e2e_master.py`:

```python
TEST_CONFIG = {
    "base_url": "http://localhost:8001",
    "api_url": "http://localhost:8000",
    "credentials": {
        "org_id": 1,
        "username": "admin",
        "password": "admin123"
    },
}
```

## 依赖安装

```bash
# 环境守护依赖
pip3 install playwright

# E2E 测试依赖
pip3 install playwright
playwright install chromium
```

## 报告输出

### 环境守护报告

位置：`skills/environment-sentinel/reports/`

```json
{
  "timestamp": "2026-03-25T00:00:00",
  "services": {
    "backend": {"status": "healthy", "port": 8000}
  },
  "summary": {
    "total": 2,
    "healthy": 2,
    "fixed": 0,
    "failed": 0
  }
}
```

### E2E 测试报告

位置：`skills/e2e-testing/reports/`

包含：
- JSON 格式详细报告
- TXT 格式可读报告
- 测试过程截图

## 持续集成

### 定时任务配置 (crontab)

```bash
# 每 3 分钟执行环境检查
*/3 * * * * python3 /path/to/skills/environment-sentinel/scripts/env_sentinel.py --check

# 每小时执行 E2E 测试
0 * * * * python3 /path/to/skills/e2e-testing/scripts/e2e_master.py --full
```

### Systemd 服务

创建 `/etc/systemd/system/env-sentinel.service`:

```ini
[Unit]
Description=Environment Sentinel Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/skills/environment-sentinel/scripts/env_sentinel.py --start
Restart=always

[Install]
WantedBy=multi-user.target
```

## 跨项目使用

1. 复制 `skills/` 目录到目标项目
2. 修改配置中的端口和路径
3. 安装依赖 `pip3 install playwright`
4. 启动守护或执行测试

## 许可证

MIT License

---

## 技能 2 增强：全类型测试套件

**新增脚本**: `e2e-testing/scripts/test_suite_master.py`

### 测试类型全覆盖

```bash
# 运行所有测试
python3 skills/e2e-testing/scripts/test_suite_master.py --all

# 运行特定类型测试
python3 skills/e2e-testing/scripts/test_suite_master.py --unit         # 单元测试
python3 skills/e2e-testing/scripts/test_suite_master.py --integration  # 集成测试
python3 skills/e2e-testing/scripts/test_suite_master.py --api          # 接口测试
python3 skills/e2e-testing/scripts/test_suite_master.py --system       # 系统测试
python3 skills/e2e-testing/scripts/test_suite_master.py --report       # 查看报告
```

### 测试覆盖矩阵

| 测试类型 | 测试内容 | 状态 |
|---------|---------|------|
| **单元测试** | Python 函数/类测试、JS 组件测试 | ✅ |
| **集成测试** | API 与 DB、前端与后端、认证授权 | ✅ |
| **接口测试** | RESTful API 所有端点测试 | ✅ |
| **系统测试** | PRD 功能模块全覆盖 | ✅ |
| **UI 交互测试** | 导航、表单、按钮、页面切换 | ✅ |
| **CRUD 验证** | 增删改查原子操作闭环 | ✅ |
