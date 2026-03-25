"""
API 路由模块
"""
from .auth import router as auth
from .organizations import router as organizations
from .systems import router as systems
from .credentials import router as credentials
from .workflows import router as workflows
from .tasks import router as tasks
from .permissions import router as permissions

__all__ = ["auth", "organizations", "systems", "credentials", "workflows", "tasks", "permissions"]
