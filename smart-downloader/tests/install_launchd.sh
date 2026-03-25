#!/bin/bash
# 智下载系统 - 安装系统级定时任务 (launchd for macOS)

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/com.smartdownloader.test.plist"
TEST_SCRIPT="$PROJECT_ROOT/run_all_tests.sh"
LOG_DIR="$PARENT_ROOT/logs"

echo "=========================================="
echo "⏰ 安装系统级定时任务 (launchd)"
echo "=========================================="
echo ""

# 创建日志目录
mkdir -p "$LOG_DIR"

# 创建 launchd plist 文件
cat > "$LAUNCHD_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.smartdownloader.test</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$TEST_SCRIPT</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$PARENT_ROOT</string>
    
    <key>StandardOutPath</key>
    <string>$LOG_DIR/test-cron.log</string>
    
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/test-cron-error.log</string>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# 加载 launchd 任务
launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
launchctl load "$LAUNCHD_PLIST"

echo "✅ 系统级定时任务已安装"
echo ""
echo "配置信息:"
echo "  任务标签：com.smartdownloader.test"
echo "  执行间隔：300 秒 (5 分钟)"
echo "  日志目录：$LOG_DIR"
echo "  Plist 文件：$LAUNCHD_PLIST"
echo ""
echo "管理命令:"
echo "  查看状态：launchctl list | grep smartdownloader"
echo "  查看日志：tail -f $LOG_DIR/test-cron.log"
echo "  卸载任务：launchctl unload $LAUNCHD_PLIST"
echo "  加载任务：launchctl load $LAUNCHD_PLIST"
echo ""
echo "=========================================="

# 立即执行一次
echo "🚀 立即执行一次测试..."
bash "$TEST_SCRIPT"
