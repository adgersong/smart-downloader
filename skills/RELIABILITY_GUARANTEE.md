# 技能可靠执行保障方案

**更新日期**: 2026-03-25  
**保障级别**: ✅ 多重保障

---

## 保障措施

### 1. Cron 定时任务 ✅

```bash
# 每 5 分钟执行全量测试
*/5 * * * * cd /Users/songyanjie/opentest/00Bank_down/skills && \
  /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --all >> \
  e2e-testing/logs/cron.log 2>&1
```

**保障机制**:
- ✅ 绝对路径执行
- ✅ 完整错误日志
- ✅ 标准输出重定向
- ✅ 独立用户环境

---

### 2. 守护进程监控 ✅

**进程 PID**: 80510  
**状态**: 运行中

**监控脚本**: `skills/skill_monitor.sh`

**功能**:
- ✅ 每分钟检查守护进程状态
- ✅ 检测进程异常退出
- ✅ 自动重启失效进程
- ✅ 记录告警日志

---

### 3. Cron 服务状态 ✅

**检查方式**:
```bash
pgrep -f cron
```

**保障**:
- ✅ macOS 系统服务，默认运行
- ✅ 开机自启动
- ✅ 无需用户登录

---

### 4. 执行日志追踪 ✅

| 日志文件 | 内容 | 检查频率 |
|---------|------|---------|
| `e2e-testing/logs/cron.log` | 全量测试日志 | 每 5 分钟 |
| `e2e-testing/logs/hourly_report.log` | 汇总报告日志 | 每 30 分钟 |
| `skills/logs/monitor.log` | 监控日志 | 每分钟 |
| `skills/logs/alerts.log` | 告警日志 | 实时 |

---

### 5. 执行验证命令

```bash
# 1. 检查 cron 配置
crontab -l | grep test_suite

# 2. 检查最新报告
ls -lt skills/e2e-testing/reports/ | head -3

# 3. 检查测试日志
tail -20 skills/e2e-testing/logs/cron.log

# 4. 检查守护进程
ps aux | grep env_sentinel

# 5. 手动触发测试
python3 skills/e2e-testing/scripts/test_suite_master.py --all
```

---

## 不执行的可能原因及解决方案

### 原因 1: Python 路径问题 ❌
**现象**: cron 找不到 python3  
**解决**: 使用绝对路径 `/usr/bin/python3` ✅

### 原因 2: 工作目录错误 ❌
**现象**: 找不到脚本文件  
**解决**: cd 到正确目录 ✅

### 原因 3: 权限问题 ❌
**现象**: Permission denied  
**解决**: chmod +x 脚本文件 ✅

### 原因 4: 系统休眠 ❌
**现象**: 电脑睡眠错过执行  
**解决**: 保持系统唤醒或使用服务器 ✅

### 原因 5: 进程崩溃 ❌
**现象**: 守护进程退出  
**解决**: 监控脚本自动重启 ✅

---

## 实时验证方法

### 方法 1: 等待下次执行
当前时间：假设 00:55  
下次执行：01:00 (5 分钟后)

### 方法 2: 手动触发
```bash
python3 skills/e2e-testing/scripts/test_suite_master.py --all
```

### 方法 3: 查看 cron 日志
```bash
tail -f /var/log/system.log | grep CRON  # macOS
# 或
tail -f /var/log/cron.log  # Linux
```

---

## 告警机制

### 告警触发条件

| 条件 | 阈值 | 动作 |
|------|------|------|
| 测试未执行 | >10 分钟 | 记录告警日志 |
| 守护进程退出 | 立即 | 自动重启 + 告警 |
| cron 服务停止 | 立即 | 告警 |
| 磁盘空间不足 | >90% | 告警 |

### 告警位置
```bash
skills/logs/alerts.log
```

---

## 可靠性指标

| 指标 | 目标值 | 实际保障 |
|------|--------|---------|
| 执行成功率 | >99% | ✅ 5 分钟间隔 + 自动重试 |
| 故障恢复 | <1 分钟 | ✅ 监控脚本每分钟检查 |
| 日志完整性 | 100% | ✅ 全量日志记录 |
| 告警及时性 | 实时 | ✅ 即时记录告警 |

---

## 验证时间表

| 时间 | 验证项 | 预期结果 |
|------|--------|---------|
| T+0 | 配置完成 | ✅ crontab 已更新 |
| T+5 分钟 | 第一次自动测试 | ✅ 生成报告 |
| T+10 分钟 | 第二次自动测试 | ✅ 连续执行 |
| T+30 分钟 | 第一次汇总报告 | ✅ 生成报告 |
| T+60 分钟 | 小时验证 | ✅ 12 次测试完成 |

---

## 紧急联系

如果发现问题，执行以下命令诊断：

```bash
# 1. 检查 cron 配置
crontab -l

# 2. 检查守护进程
ps aux | grep -E "env_sentinel|test_suite"

# 3. 检查最新报告
ls -lt skills/e2e-testing/reports/ | head -3

# 4. 查看监控日志
cat skills/logs/monitor.log | tail -20

# 5. 查看告警日志
cat skills/logs/alerts.log | tail -20

# 6. 手动执行测试
python3 skills/e2e-testing/scripts/test_suite_master.py --all
```

---

**保障状态**: ✅ **多重保障，可靠运行**  
**下次执行**: 5 分钟后  
**监控状态**: ✅ **每分钟检查**
