# 定时任务频率更新通知

**更新日期**: 2026-03-25  
**更新状态**: ✅ 已完成

---

## 更新内容

### 原配置
| 任务 | 原频率 | 新频率 |
|------|--------|--------|
| 全量全类型测试 | 每小时 | **每 5 分钟** |
| 汇总报告 | 每天 02:00 | **每 30 分钟** |

---

## 新定时任务配置

```bash
# 每 5 分钟执行全量全类型测试
*/5 * * * * cd /Users/songyanjie/opentest/00Bank_down/skills && \
  /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --all >> \
  e2e-testing/logs/cron.log 2>&1

# 每 30 分钟生成汇总报告
*/30 * * * * cd /Users/songyanjie/opentest/00Bank_down/skills && \
  /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --report >> \
  e2e-testing/logs/hourly_report.log 2>&1

# 每天凌晨 2 点生成每日终期报告
0 2 * * * cd /Users/songyanjie/opentest/00Bank_down/skills && \
  /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --report >> \
  e2e-testing/logs/daily_report.log 2>&1
```

---

## 执行频率汇总

| 任务 | 频率 | 说明 |
|------|------|------|
| **环境检查** | 每 3 分钟 | 端口、依赖、服务健康 |
| **全量测试** | 每 5 分钟 | 单元 + 集成 + 接口 + 系统 + UI + CRUD |
| **汇总报告** | 每 30 分钟 | 测试结果汇总、覆盖率统计 |
| **每日报告** | 每天 02:00 | 终期质量白皮书 |

---

## 下次执行时间

假设当前时间：00:55

| 任务 | 下次执行 |
|------|---------|
| 环境检查 | 00:57 (2 分钟后) |
| 全量测试 | 01:00 (5 分钟后) |
| 汇总报告 | 01:00 (5 分钟后) |
| 每日报告 | 次日 02:00 |

---

## 日志文件位置

| 日志类型 | 文件路径 |
|---------|---------|
| 环境守护日志 | `skills/environment-sentinel/logs/daemon.log` |
| 环境检查日志 | `skills/environment-sentinel/logs/cron.log` |
| 全量测试日志 | `skills/e2e-testing/logs/cron.log` |
| 汇总报告日志 | `skills/e2e-testing/logs/hourly_report.log` |
| 每日报告日志 | `skills/e2e-testing/logs/daily_report.log` |

---

## 查看实时日志

```bash
# 全量测试实时日志
tail -f skills/e2e-testing/logs/cron.log

# 汇总报告实时日志
tail -f skills/e2e-testing/logs/hourly_report.log

# 环境守护实时日志
tail -f skills/environment-sentinel/logs/daemon.log
```

---

## 手动触发测试

```bash
# 手动执行全量测试
python3 skills/e2e-testing/scripts/test_suite_master.py --all

# 手动生成汇总报告
python3 skills/e2e-testing/scripts/test_suite_master.py --report

# 手动执行环境检查
python3 skills/environment-sentinel/scripts/env_sentinel.py --check
```

---

## 系统负载预估

| 指标 | 原配置 | 新配置 | 变化 |
|------|--------|--------|------|
| 测试执行/小时 | 1 次 | 12 次 | +1100% |
| 报告生成/小时 | 0 次 | 2 次 | +∞ |
| CPU 占用 (平均) | <1% | ~5% | +400% |
| 磁盘空间/天 | ~50MB | ~200MB | +300% |
| 日志文件/天 | ~10 个 | ~50 个 | +400% |

**注意**: 频率提高后系统负载会增加，请确保服务器资源充足。

---

## 告警阈值调整

由于测试频率提高，建议调整告警阈值：

| 告警项 | 原阈值 | 新阈值 |
|--------|--------|--------|
| 连续失败次数 | >3 次 | >5 次 |
| 测试覆盖率告警 | <80% | <80% |
| 磁盘空间告警 | >80% | >70% |

---

## 验证命令

```bash
# 查看定时任务配置
crontab -l | grep skills

# 查看守护进程状态
ps aux | grep env_sentinel | grep -v grep

# 查看最新报告
ls -lt skills/e2e-testing/reports/ | head -5
```

---

**更新时间**: 2026-03-25 00:55  
**更新方式**: Crontab 配置更新  
**状态**: ✅ **已生效**

---

## 预期效果

- **问题发现更快**: 从最多 1 小时缩短到最多 5 分钟
- **反馈更及时**: 每 30 分钟生成报告，实时掌握质量状况
- **持续集成优化**: CI/CD 问题"不过夜"升级为"不过半小时"
