#!/bin/bash
# 智下载 - 快速启动脚本

set -e

echo "🚀 智下载 SmartDownloader - 启动脚本"
echo "====================================="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从 .env.example 复制"
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置必要的环境变量"
fi

# 启动服务
echo ""
echo "📦 启动服务..."
echo ""

# 检查是否启用 AI 功能
if [ "$1" == "--with-ai" ]; then
    echo "🤖 启用 AI 功能 (Ollama + Qwen VL)"
    docker-compose up -d --profile with-ai
else
    echo "⚡ 基础模式 (不含 AI 功能)"
    docker-compose up -d
fi

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 服务状态:"
docker-compose ps

echo ""
echo "✅ 启动完成!"
echo ""
echo "📱 访问地址:"
echo "   前端：http://localhost:3000"
echo "   后端 API: http://localhost:8000"
echo "   API 文档：http://localhost:8000/api/docs"
echo ""
echo "📝 常用命令:"
echo "   查看日志：docker-compose logs -f"
echo "   停止服务：docker-compose down"
echo "   重启服务：docker-compose restart"
echo "   启用 AI:   docker-compose up -d --profile with-ai"
echo ""
