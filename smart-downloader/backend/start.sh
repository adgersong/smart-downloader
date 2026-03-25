#!/bin/bash
# 后端服务启动脚本

set -e

echo "🚀 启动后端服务..."

cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d "venv" ]; then
    echo "⚠️  虚拟环境不存在，正在创建..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt 不存在"
    exit 1
fi

echo "📦 安装依赖..."
pip install -q -r requirements.txt

echo "🗄️  初始化数据库..."
python3 -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

echo "🚀 启动服务..."
echo "📡 API 文档：http://localhost:8000/api/docs"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
