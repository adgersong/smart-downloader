#!/bin/bash
# 技能系统安装脚本

echo "======================================"
echo "智能测试技能系统 - 安装向导"
echo "======================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi
echo "✅ Node.js: $(node --version)"

# 安装 Python 依赖
echo ""
echo "安装 Python 依赖..."
pip3 install playwright --break-system-packages -q
echo "✅ Playwright 已安装"

# 安装浏览器
echo ""
echo "安装 Chromium 浏览器..."
python3 -m playwright install chromium 2>&1 | tail -3
echo "✅ Chromium 已安装"

# 创建目录
echo ""
echo "创建目录结构..."
mkdir -p skills/environment-sentinel/{scripts,config,reports,logs}
mkdir -p skills/e2e-testing/{scripts,test-cases,reports,screenshots}
echo "✅ 目录已创建"

# 测试安装
echo ""
echo "测试安装..."
python3 skills/environment-sentinel/scripts/env_sentinel.py --check 2>&1 | head -10
echo ""
echo "======================================"
echo "✅ 安装完成!"
echo "======================================"
echo ""
echo "使用方式:"
echo "  环境守护：python3 skills/environment-sentinel/scripts/env_sentinel.py --start"
echo "  E2E 测试：python3 skills/e2e-testing/scripts/e2e_master.py --full"
echo ""
