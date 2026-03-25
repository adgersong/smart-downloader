# 每 5 分钟全量测试执行记录说明

**更新日期**: 2026-03-25

---

## 执行记录方式

### 1. Cron 日志记录 ✅

**文件位置**: `skills/e2e-testing/logs/cron.log`

**记录内容**:
- 每次测试的标准输出
- 错误信息
- 测试结果汇总

**查看方式**:
```bash
tail -f skills/e2e-testing/logs/cron.log
```

---

### 2. 执行历史追踪 ✅

**文件位置**: `skills/logs/execution_history.json`

**记录内容**:
- 执行时间戳
- 测试类型
- 执行状态
- 详细信息

**JSON 格式**:
```json
{
  "executions": [
    {
      "timestamp": "2026-03-25T01:05:00",
      "test_type": "automated_test",
      "status": "success",
      "details": {
        "total": 44,
        "passed": 43,
        "failed": 1,
        "coverage": 97.7
      }
    }
  ]
}
```

**查看方式**:
```bash
python3 skills/execution_tracker.py --history
```

---

### 3. 测试报告文件 ✅

**文件位置**: `skills/e2e-testing/reports/`

**命名格式**: `test_suite_report_YYYYMMDD_HHMMSS.json`

**每次测试生成**:
- JSON 格式详细报告
- TXT 格式可读报告
- 截图文件

**查看最新报告**:
```bash
ls -lt skills/e2e-testing/reports/ | head -5
```

---

### 4. 监控日志 ✅

**文件位置**: `skills/logs/monitor.log`

**记录内容**:
- 每分钟监控检查
- 守护进程状态
- 异常检测

**查看方式**:
```bash
tail -f skills/logs/monitor.log
```

---

## 执行记录验证

### 方法 1: 检查日志文件
```bash
# 查看最新的测试日志
tail -20 skills/e2e-testing/logs/cron.log
```

### 方法 2: 查看执行历史
```bash
python3 skills/execution_tracker.py --history
```

### 方法 3: 检查报告文件
```bash
ls -lt skills/e2e-testing/reports/ | head -10
```

### 方法 4: 查看 crontab 配置
```bash
crontab -l | grep test_suite
```

---

## 执行时间线

假设当前时间：01:00

| 时间 | 事件 | 记录文件 |
|------|------|---------|
| 01:00 | 全量测试 | cron.log + execution_history.json |
| 01:00 | 生成报告 | reports/test_suite_report_010000.json |
| 01:03 | 环境检查 | environment-sentinel/logs/cron.log |
| 01:05 | 全量测试 | cron.log + execution_history.json |
| 01:05 | 生成报告 | reports/test_suite_report_010500.json |
| 01:30 | 汇总报告 | hourly_report.log |

---

## 日志轮转

### 自动清理策略

| 日志类型 | 保留策略 |
|---------|---------|
| cron.log | 最新 10MB |
| execution_history.json | 最近 1000 条 |
| test_suite_report_*.json | 最近 100 个报告 |
| monitor.log | 最近 7 天 |

---

## 执行频率确认

| 任务 | 配置 | 实际执行 | 记录验证 |
|------|------|---------|---------|
| 全量测试 | */5 * * * * | 每 5 分钟 | cron.log ✅ |
| 汇总报告 | */30 * * * * | 每 30 分钟 | hourly_report.log ✅ |
| 环境检查 | */3 * * * * | 每 3 分钟 | sentinel/cron.log ✅ |
| 执行追踪 | */5 * * * * | 每 5 分钟 | execution_history.json ✅ |

---

## 验证示例

### 当前执行记录

```bash
# 1. 查看 crontab 配置
$ crontab -l | grep test_suite
*/5 * * * * cd /Users/songyanjie/opentest/00Bank_down/skills && \
  /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --all >> \
  e2e-testing/logs/cron.log 2>&1

# 2. 查看执行历史
$ python3 skills/execution_tracker.py --history
======================================================================
技能执行历史
======================================================================
✅ 2026-03-25T01:05:00 - automated_test
✅ 2026-03-25T01:00:00 - automated_test
======================================================================
总记录数：2

# 3. 查看最新报告
$ ls -lt skills/e2e-testing/reports/ | head -3
test_suite_report_20260325_010500.json
test_suite_report_20260325_010000.json
```

---

## 实时监

```bash
# 实时监控测试执行
tail -f skills/e2e-testing/logs/cron.log

# 实时监控报告生成
watch -n 5 'ls -lt skills/e2e-testing/reports/ | head -3'
```

---

**记录状态**: ✅ **完整记录每次执行**  
**记录方式**: 4 重记录保障  
**下次执行**: 5 分钟后
