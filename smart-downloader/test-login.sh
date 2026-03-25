#!/bin/bash
# 智下载 - 自动登录测试脚本

echo "======================================"
echo "智下载 - 自动登录测试"
echo "======================================"

# 1. 检查服务状态
echo ""
echo "1. 检查服务状态..."
curl -s http://localhost:8000/health > /dev/null && echo "✅ 后端服务：运行中" || echo "❌ 后端服务：未运行"
curl -s http://localhost:8001 > /dev/null && echo "✅ 前端服务：运行中" || echo "❌ 前端服务：未运行"

# 2. 测试登录 API
echo ""
echo "2. 测试登录 API..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"org_id":1,"username":"admin","password":"admin123"}')

echo "响应：$RESPONSE"

# 3. 获取 Token
TOKEN=$(echo $RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
  echo "✅ 登录成功"
  echo "Token: ${TOKEN:0:20}..."
  
  # 4. 测试受保护的 API
  echo ""
  echo "3. 测试受保护的 API..."
  ORG_RESPONSE=$(curl -s http://localhost:8000/api/v1/organizations?org_id=1 \
    -H "Authorization: Bearer $TOKEN")
  echo "组织 API 响应：$ORG_RESPONSE"
else
  echo "❌ 登录失败"
  echo "请检查用户名密码或创建测试用户"
fi

echo ""
echo "======================================"
echo "测试完成"
echo "======================================"
echo ""
echo "访问地址:"
echo "  登录页面：http://localhost:8001/login"
echo "  主界面：http://localhost:8001"
echo "  API 文档：http://localhost:8000/api/docs"
