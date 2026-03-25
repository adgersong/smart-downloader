#!/bin/bash
# 智下载 - 数据迁移脚本

set -e

echo "🔄 智下载 - 数据迁移脚本"
echo "========================"

# 检查参数
if [ -z "$1" ]; then
    echo "用法：./migrate.sh <操作>"
    echo ""
    echo "可用操作:"
    echo "  init     - 初始化数据库"
    echo "  backup   - 备份数据"
    echo "  restore  - 恢复数据"
    echo "  clean    - 清理旧数据"
    exit 1
fi

ACTION=$1
BACKUP_DIR="./data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

case $ACTION in
    init)
        echo "📦 初始化数据库..."
        docker-compose exec backend python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
        echo "✅ 数据库初始化完成"
        ;;
    
    backup)
        echo "💾 备份数据..."
        mkdir -p $BACKUP_DIR
        docker cp $(docker-compose ps -q backend):/app/data/app.db $BACKUP_DIR/app_$TIMESTAMP.db
        echo "✅ 数据已备份到：$BACKUP_DIR/app_$TIMESTAMP.db"
        ;;
    
    restore)
        if [ -z "$2" ]; then
            echo "❌ 请指定备份文件"
            exit 1
        fi
        BACKUP_FILE=$2
        echo "🔄 恢复数据从：$BACKUP_FILE"
        docker cp $BACKUP_FILE $(docker-compose ps -q backend):/app/data/app.db
        docker-compose restart backend
        echo "✅ 数据恢复完成"
        ;;
    
    clean)
        echo "🧹 清理旧数据..."
        docker-compose exec backend python -c "
from app.services.execution_logger import get_execution_logger
logger = get_execution_logger()
deleted = logger.clear_old_logs(days=30)
print(f'清理了 {deleted} 个日志文件')
"
        echo "✅ 清理完成"
        ;;
    
    *)
        echo "❌ 未知操作：$ACTION"
        exit 1
        ;;
esac

echo ""
echo "🎉 操作完成!"
