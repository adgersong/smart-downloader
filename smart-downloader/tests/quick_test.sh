#!/bin/bash
# 智下载系统 - 快速测试脚本
# 用于手动快速执行所有测试

set -e

echo "=========================================="
echo "🧪 智下载系统 - 快速测试"
echo "=========================================="
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

PASS_COUNT=0
FAIL_COUNT=0

run_test() {
    local name=$1
    local script=$2
    
    echo -e "\n📍 测试：$name"
    echo "----------------------------------------"
    
    if python3 "$script" 2>&1; then
        echo "✅ $name 通过"
        ((PASS_COUNT++))
    else
        echo "❌ $name 失败"
        ((FAIL_COUNT++))
    fi
}

# 检查服务
echo "🔍 检查服务状态..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务运行中"
else
    echo "❌ 后端服务未运行"
    echo "请先启动：cd backend && ./start.sh"
    exit 1
fi

# 执行测试
run_test "前端单元测试" "$PROJECT_ROOT/tests/test_frontend_unit.py"
run_test "后端单元测试" "$PROJECT_ROOT/tests/test_backend_unit.py"
run_test "API 接口测试" "$PROJECT_ROOT/tests/test_api.py"
run_test "集成测试" "$PROJECT_ROOT/tests/test_integration.py"
run_test "交互测试" "$PROJECT_ROOT/tests/test_interactive.py"

# 输出结果
echo ""
echo "=========================================="
echo "📊 测试结果"
echo "=========================================="
echo "通过：$PASS_COUNT"
echo "失败：$FAIL_COUNT"
echo "总计：$((PASS_COUNT + FAIL_COUNT))"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}有测试失败${NC}"
    exit 1
fi
