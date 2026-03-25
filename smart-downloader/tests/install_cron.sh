#!/bin/bash
# 智下载系统 - 定时测试任务安装脚本
# 每 5 分钟执行一次全量测试

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_SCRIPT="$PROJECT_ROOT/tests/run_all_tests.sh"
CRON_FILE="/tmp/smart_downloader_cron"

echo "=========================================="
echo "⏰ 安装定时测试任务"
echo "=========================================="
echo ""

# 创建 cron 任务
cat > "$CRON_FILE" << EOF
# 智下载系统 - 定时测试任务
# 每 5 分钟执行一次全量测试
*/5 * * * * $TEST_SCRIPT >> $PROJECT_ROOT/tests/cron-test.log 2>&1
EOF

# 安装 cron 任务
crontab "$CRON_FILE"

echo "✅ 定时任务已安装"
echo ""
echo "配置信息:"
echo "  测试脚本：$TEST_SCRIPT"
echo "  执行频率：每 5 分钟"
echo "  日志文件：$PROJECT_ROOT/tests/cron-test.log"
echo ""
echo "查看定时任务:"
echo "  crontab -l"
echo ""
echo "查看测试日志:"
echo "  tail -f $PROJECT_ROOT/tests/cron-test.log"
echo ""
echo "删除定时任务:"
echo "  crontab -r"
echo ""
echo "=========================================="

# 立即执行一次测试
echo "🚀 立即执行一次测试..."
echo ""
$TEST_SCRIPT
