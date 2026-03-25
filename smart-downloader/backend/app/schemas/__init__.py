"""
Pydantic 模型 - 用于请求/响应验证
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== 通用响应 ====================

class ResponseBase(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None
    timestamp: datetime


class PaginationInfo(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int


class PaginatedResponse(ResponseBase):
    data: dict


# ==================== 认证 ====================

class LoginRequest(BaseModel):
    org_id: int
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 86400


class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str
    org_id: int
    org_name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserInfo


# ==================== 组织 ====================

class OrganizationBase(BaseModel):
    name: str
    config: Optional[Dict[str, Any]] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationStats(BaseModel):
    user_count: int = 0
    system_count: int = 0
    workflow_count: int = 0
    task_count: int = 0


class OrganizationResponse(OrganizationBase):
    id: int
    stats: Optional[OrganizationStats] = None
    created_at: datetime
    updated_at: datetime


# ==================== 业务系统 ====================

class LoginConfig(BaseModel):
    login_url: str
    username_selector: str
    password_selector: str
    submit_selector: str
    success_url: Optional[str] = None


class BusinessSystemBase(BaseModel):
    name: str
    url: str
    type: Optional[str] = None
    description: Optional[str] = None
    login_config: Optional[Dict[str, Any]] = None


class BusinessSystemCreate(BusinessSystemBase):
    org_id: int


class BusinessSystemUpdate(BusinessSystemBase):
    pass


class BusinessSystemResponse(BusinessSystemBase):
    id: int
    org_id: int
    has_credential: bool = False
    workflow_count: int = 0
    created_at: datetime
    updated_at: datetime


# ==================== 凭证 ====================

class CredentialBase(BaseModel):
    username: str
    password: str
    auth_type: str = "password"
    mfa_config: Optional[Dict[str, Any]] = None


class CredentialCreate(CredentialBase):
    system_id: int


class CredentialUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    auth_type: Optional[str] = None
    mfa_config: Optional[Dict[str, Any]] = None


class CredentialResponse(BaseModel):
    id: int
    system_id: int
    username: str
    auth_type: str
    created_at: datetime


# ==================== 流程 ====================

class WorkflowStepConfig(BaseModel):
    url: Optional[str] = None
    selector: Optional[str] = None
    value: Optional[str] = None
    seconds: Optional[int] = None
    save_path: Optional[str] = None


class WorkflowStepBase(BaseModel):
    node_id: str
    node_type: str
    config: Dict[str, Any]


class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    yaml_config: str


class WorkflowCreate(WorkflowBase):
    org_id: int
    system_id: int


class WorkflowUpdate(WorkflowBase):
    pass


class WorkflowStats(BaseModel):
    execution_count: int = 0
    success_rate: float = 0.0
    last_execution: Optional[datetime] = None


class WorkflowResponse(WorkflowBase):
    id: int
    org_id: int
    system_id: int
    system_name: Optional[str] = None
    steps_count: int = 0
    created_by: Optional[str] = None
    stats: Optional[WorkflowStats] = None
    created_at: datetime
    updated_at: datetime


class WorkflowGenerateRequest(BaseModel):
    system_id: int
    description: str


class WorkflowGenerateResponse(BaseModel):
    yaml_config: str
    nodes_count: int
    confidence: float
    elements_detected: List[Dict[str, Any]]


class WorkflowValidationResponse(BaseModel):
    valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []


# ==================== 任务 ====================

# ==================== 权限 ====================

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskProgress(BaseModel):
    current_step: int
    total_steps: int
    percentage: int


class TaskBase(BaseModel):
    workflow_id: int
    schedule: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class TaskCreate(TaskBase):
    pass


class TaskExecuteRequest(BaseModel):
    workflow_id: int
    context: Optional[Dict[str, Any]] = None
    schedule: Optional[Dict[str, Any]] = None


class TaskResponse(TaskBase):
    id: int
    org_id: int
    status: str
    progress: Optional[TaskProgress] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    estimated_remaining: Optional[int] = None


class TaskLogEntry(BaseModel):
    timestamp: datetime
    level: str
    step: str
    message: str


class TaskLogResponse(BaseModel):
    task_id: int
    logs: List[TaskLogEntry]
