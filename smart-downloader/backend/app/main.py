"""
智下载后端服务
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, Base
from .api.v1 import auth, organizations, systems, credentials, workflows, tasks
# OpenTelemetry middleware import
from .middleware.otel import init_otel

# Load settings
from .core.config.settings import Settings
settings = Settings()

# Register exception handlers
from .core.exception_handler import http_exception_handler, generic_exception_handler

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="智下载 API",
    description="智能浏览器自动化下载系统",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    debug=settings.DEBUG,
)

# Register global exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "智下载 SmartDownloader",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 注册路由
app.include_router(auth, prefix="/api/v1/auth", tags=["认证"])
app.include_router(organizations, prefix="/api/v1/organizations", tags=["组织管理"])
app.include_router(systems, prefix="/api/v1/systems", tags=["业务系统"])
app.include_router(credentials, prefix="/api/v1/credentials", tags=["凭证管理"])
app.include_router(workflows, prefix="/api/v1/workflows", tags=["流程管理"])
app.include_router(tasks, prefix="/api/v1/tasks", tags=["任务管理"])
