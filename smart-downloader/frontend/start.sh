#!/bin/bash
# 前端服务启动脚本

set -e

echo "🚀 启动前端服务..."

cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖未安装，正在安装..."
    npm install
fi

echo "📦 启动开发服务器..."
echo "📱 访问地址：http://localhost:8000"
npm run dev
