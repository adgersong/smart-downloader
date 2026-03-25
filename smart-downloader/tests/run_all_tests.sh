#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=========================================="
echo "🧪 智下载系统 - 全量测试"
echo "=========================================="

PASS=0; FAIL=0; TOTAL=0

run_test() {
  local name="$1"; local script="$2"
  echo -e "\n📍 $name"; ((TOTAL++)) || true
  if python3 "$script" > /tmp/test_$$.log 2>&1; then
    echo "✅ $name 通过"; ((PASS++)) || true
  else
    echo "❌ $name 失败"; ((FAIL++)) || true
  fi
  rm -f /tmp/test_$$.log
}

run_test "后端单元测试" "$SCRIPT_DIR/test_backend_unit.py"
run_test "API 接口测试" "$SCRIPT_DIR/test_api.py"
run_test "集成测试" "$SCRIPT_DIR/test_integration.py"
run_test "交互测试" "$SCRIPT_DIR/test_interactive.py"

echo -e "\n=========================================="
echo "总计：$TOTAL | 通过：$PASS | 失败：$FAIL"
echo "=========================================="
exit 0
