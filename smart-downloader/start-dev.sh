#!/bin/bash
# 智下载系统 - 开发环境启动脚本

set -e

echo "🚀 智下载系统 - 启动中..."

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

start_backend() {
    echo "📦 启动后端服务..."
    cd backend
    source venv/bin/activate 2>/dev/null || true
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
    cd ..
}

start_frontend() {
    echo "🎨 启动前端服务..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
    cd ..
}

wait_for_services() {
    echo "⏳ 等待服务启动..."
    sleep 5
    
    echo ""
    echo "=================================="
    echo "✅ 所有服务已启动"
    echo "=================================="
    echo "📱 前端：http://localhost:8000"
    echo "📡 后端：http://localhost:8000/api/docs"
    echo "=================================="
    echo ""
    echo "按 Ctrl+C 停止所有服务"
    
    wait
}

trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

start_backend
start_frontend
wait_for_services
