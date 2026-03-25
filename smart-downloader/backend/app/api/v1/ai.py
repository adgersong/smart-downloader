"""
AI 流程生成 API 路由
支持文字描述和截图标注生成自动化流程
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from ...db.database import get_db
from ...models.user import User
from ...models.workflow import Workflow
from ...schemas import WorkflowGenerateFromTextRequest, WorkflowGenerateFromImageRequest, WorkflowResponse, ResponseBase
from ...core.deps import get_current_user
from ...core.engine.vision_engine import get_qwen_engine
import yaml

router = APIRouter()


@router.post("/generate/from-text", response_model=WorkflowResponse)
async def generate_from_text(
    request: WorkflowGenerateFromTextRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从文字描述生成流程"""
    engine = get_qwen_engine()
    
    # 调用 AI 生成工作流
    result = await engine.text_to_workflow(request.description)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"AI 生成失败：{result.get('error', '未知错误')}")
    
    yaml_config = result["yaml_config"]
    
    # 验证 YAML
    try:
        config = yaml.safe_load(yaml_config)
        if "nodes" not in config:
            raise ValueError("生成的工作流缺少 nodes 配置")
    except yaml.YAMLError as e:
        raise HTTPException(status_code=500, detail=f"YAML 解析失败：{str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # 创建工作记录
    workflow = Workflow(
        org_id=request.org_id,
        system_id=request.system_id,
        name=request.name or f"AI 生成的流程 - {request.description[:20]}...",
        description=f"通过 AI 从文字描述生成",
        yaml_config=yaml_config,
        created_by=current_user.id
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    
    return WorkflowResponse(
        id=workflow.id,
        org_id=workflow.org_id,
        system_id=workflow.system_id,
        name=workflow.name,
        description=workflow.description,
        yaml_config=yaml_config,
        created_by=current_user.username,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@router.post("/generate/from-image", response_model=Dict[str, Any])
async def generate_from_image(
    org_id: int = Form(...),
    system_id: Optional[int] = Form(None),
    name: Optional[str] = Form(None),
    file: UploadFile = File(...),
    annotations: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """从截图生成流程 (支持标注)"""
    import tempfile
    import os
    import json
    
    engine = get_qwen_engine()
    
    # 保存上传的文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 解析标注
        annotation_list = None
        if annotations:
            annotation_list = json.loads(annotations)
        
        # 调用 AI 分析
        result = await engine.parse_intent(tmp_path, annotation_list)
        
        # 生成 YAML 配置
        actions = result.get("actions", result.get("suggested_actions", []))
        
        yaml_config = "nodes:\n"
        yaml_config += "  - id: start\n    type: start\n"
        
        for i, action in enumerate(actions):
            node_id = f"node-{i+1}"
            action_type = action.get("type", "click")
            
            yaml_config += f"  - id: {node_id}\n"
            yaml_config += f"    type: {action_type}\n"
            yaml_config += f"    config:\n"
            
            if action_type == "navigate":
                yaml_config += f"      url: {action.get('target', 'https://example.com')}\n"
            elif action_type == "click":
                yaml_config += f"      selector: \"[data-desc='{action.get('target', '')}']\"\n"
            elif action_type == "fill":
                yaml_config += f"      selector: \"[data-desc='{action.get('target', '')}']\"\n"
                yaml_config += f"      value: \"{action.get('value', '')}\"\n"
        
        yaml_config += "edges:\n"
        prev_id = "start"
        for i in range(len(actions)):
            node_id = f"node-{i+1}"
            yaml_config += f"  - source: {prev_id}\n    target: {node_id}\n"
            prev_id = node_id
        
        # 创建工作记录
        workflow = Workflow(
            org_id=org_id,
            system_id=system_id,
            name=name or f"AI 生成的流程 - 截图分析",
            description=f"通过 AI 从截图分析生成",
            yaml_config=yaml_config,
            created_by=current_user.id
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        
        return {
            "workflow_id": workflow.id,
            "intent": result.get("intent", "未知"),
            "actions_count": len(actions),
            "yaml_config": yaml_config,
            "raw_response": result.get("raw_response", "")
        }
    
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.post("/analyze/elements")
async def analyze_elements(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """分析截图中的 UI 元素"""
    import tempfile
    import os
    
    engine = get_qwen_engine()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        result = await engine.detect_elements(tmp_path)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.post("/validate/ai-generated")
async def validate_ai_generated(
    yaml_config: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """验证 AI 生成的流程"""
    try:
        config = yaml.safe_load(yaml_config)
        errors = []
        
        if "nodes" not in config:
            errors.append("缺少 nodes 配置")
        if "edges" not in config:
            errors.append("缺少 edges 配置")
        
        valid_types = ["start", "end", "navigate", "click", "fill", "wait", "download", "condition", "loop"]
        for node in config.get("nodes", []):
            if node.get("type") not in valid_types:
                errors.append(f"无效的节点类型：{node.get('type')}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "message": "流程配置有效" if not errors else "流程配置存在问题"
        }
    
    except yaml.YAMLError as e:
        return {
            "valid": False,
            "errors": [f"YAML 解析错误：{str(e)}"]
        }
