#!/bin/bash
# 技能执行监控脚本

SKILLS_PATH="/Users/songyanjie/opentest/00Bank_down/skills"
LOG_FILE="$SKILLS_PATH/logs/monitor.log"
ALERT_FILE="$SKILLS_PATH/logs/alerts.log"

# 检查守护进程
if ! pgrep -f "env_sentinel.py" > /dev/null; then
    echo "$(date) - 警告：环境守护进程未运行！" >> "$LOG_FILE"
    echo "$(date) - 警告：环境守护进程未运行！" >> "$ALERT_FILE"
    
    # 自动重启
    nohup python3 "$SKILLS_PATH/environment-sentinel/scripts/env_sentinel.py" --start >> "$SKILLS_PATH/environment-sentinel/logs/daemon.log" 2>&1 &
    echo "$(date) - 已自动重启环境守护进程" >> "$LOG_FILE"
fi

# 检查全量测试进程（如果超过 5 分钟未执行）
LAST_TEST=$(ls -t "$SKILLS_PATH/e2e-testing/reports/" 2>/dev/null | head -1)
if [ -n "$LAST_TEST" ]; then
    LAST_TIME=$(stat -f %m "$SKILLS_PATH/e2e-testing/reports/$LAST_TEST" 2>/dev/null || stat -c %Y "$SKILLS_PATH/e2e-testing/reports/$LAST_TEST" 2>/dev/null)
    NOW=$(date +%s)
    DIFF=$(( (NOW - LAST_TIME) / 60 ))
    
    if [ "$DIFF" -gt 10 ]; then
        echo "$(date) - 警告：全量测试已超过${DIFF}分钟未执行" >> "$LOG_FILE"
    fi
fi

# 检查 cron 服务
if ! pgrep -f cron > /dev/null; then
    echo "$(date) - 警告：cron 服务未运行！" >> "$LOG_FILE"
    echo "$(date) - 警告：cron 服务未运行！" >> "$ALERT_FILE"
fi

echo "$(date) - 监控检查完成" >> "$LOG_FILE"
