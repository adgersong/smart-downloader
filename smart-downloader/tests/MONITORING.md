# 智下载系统 - 持续测试监控面板

**状态**: ✅ 运行中
**启动时间**: $(date '+%Y-%m-%d %H:%M:%S')
**执行间隔**: 300 秒 (5 分钟)

---

## 守护进程状态

| 项目 | 状态 |
|------|------|
| 进程 ID | $(cat tests/test_daemon.pid 2>/dev/null || echo "未运行") |
| 进程状态 | $(ps -p $(cat tests/test_daemon.pid 2>/dev/null) > /dev/null && echo "运行中" || echo "已停止") |
| 日志文件 | tests/daemon-test.log |
| 下次执行 | 每 5 分钟 |

---

## 测试执行历史

$(tail -50 tests/daemon-test.log 2>/dev/null | grep -E "(开始执行 | 测试完成|通过 | 失败)" | tail -20 || echo "暂无执行记录")

---

## 最近测试结果

$(tail -100 tests/daemon-test.log 2>/dev/null | grep -E "✓|✗|总计 | 通过率" | tail -10 || echo "暂无测试结果")

---

## 管理命令

### 查看状态
```bash
ps -p $(cat tests/test_daemon.pid)
tail -f tests/daemon-test.log
```

### 重启守护进程
```bash
kill $(cat tests/test_daemon.pid)
nohup python3 tests/test_daemon.py > tests/daemon-test.log 2>&1 &
echo $! > tests/test_daemon.pid
```

### 停止守护进程
```bash
kill $(cat tests/test_daemon.pid)
rm -f tests/test_daemon.pid
```

---

**最后更新**: $(date '+%Y-%m-%d %H:%M:%S')
