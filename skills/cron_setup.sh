#!/bin/bash
# 技能定时任务配置脚本

echo "======================================"
echo "配置技能定时任务"
echo "======================================"

SKILLS_PATH="/Users/songyanjie/opentest/00Bank_down/skills"

# 备份现有 crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null

# 添加到 crontab
(crontab -l 2>/dev/null | grep -v "env_sentinel\|test_suite_master"; echo "
# 智下载 - 技能定时任务
# 每 3 分钟执行环境检查
*/3 * * * * cd $SKILLS_PATH && /usr/bin/python3 environment-sentinel/scripts/env_sentinel.py --check >> environment-sentinel/logs/cron.log 2>&1

# 每小时执行全类型测试
0 * * * * cd $SKILLS_PATH && /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --all >> e2e-testing/logs/cron.log 2>&1

# 每天凌晨生成汇总报告
0 2 * * * cd $SKILLS_PATH && /usr/bin/python3 e2e-testing/scripts/test_suite_master.py --report >> e2e-testing/logs/daily_report.log 2>&1
") | crontab -

echo "✅ 定时任务已配置"
echo ""
echo "当前 crontab 配置:"
crontab -l | grep -E "skills|sentinel|test_suite"
echo ""
echo "======================================"
