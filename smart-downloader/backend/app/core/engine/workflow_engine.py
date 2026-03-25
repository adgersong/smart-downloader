"""
LangGraph 工作流引擎模块
实现基于状态机的自动化流程编排
"""
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from enum import Enum
import yaml


class NodeType(str, Enum):
    """节点类型枚举"""
    START = "start"
    END = "end"
    NAVIGATE = "navigate"
    CLICK = "click"
    FILL = "fill"
    WAIT = "wait"
    DOWNLOAD = "download"
    CONDITION = "condition"
    LOOP = "loop"


class NodeStatus(str, Enum):
    """节点状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowState(TypedDict):
    """工作流状态"""
    task_id: int
    org_id: int
    current_node: Optional[str]
    completed_nodes: List[str]
    failed_nodes: List[str]
    node_results: Dict[str, Any]
    status: str
    error_message: Optional[str]
    variables: Dict[str, Any]


class WorkflowEngine:
    """LangGraph 工作流引擎"""
    
    def __init__(self):
        self.graph = None
        self.state = None
        self.browser_engine = None  # 将在运行时注入
    
    def set_browser_engine(self, browser_engine):
        """注入浏览器引擎实例，以便节点处理函数调用"""
        self.browser_engine = browser_engine
    
    def build_graph(self, workflow_config: str) -> StateGraph:
        """从 YAML 配置构建工作流图"""
        config = yaml.safe_load(workflow_config)
        
        # 创建状态图
        builder = StateGraph(WorkflowState)
        
        nodes = config.get("nodes", [])
        edges = config.get("edges", [])
        
        # 添加节点
        for node in nodes:
            node_id = node.get("id")
            node_type = node.get("type")
            
            # 注册节点处理函数，传入 node_id 供内部使用
            builder.add_node(node_id, self._create_node_handler(node_id, node_type, node.get("config", {})))
        
        # 添加边
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            condition = edge.get("condition")
            
            if condition:
                # 条件边
                builder.add_conditional_edges(source, self._evaluate_condition(condition), {
                    "true": target,
                    "false": edge.get("alt_target", END)
                })
            else:
                # 普通边
                builder.add_edge(source, target)
        
        # 设置入口节点（使用第一个节点的 id）
        if nodes:
            builder.set_entry_point(nodes[0]["id"])
        
        self.graph = builder.compile()
        return self.graph
    
    def _create_node_handler(self, node_id: str, node_type: str, config: Dict):
        """创建节点处理函数，能够调用浏览器引擎执行实际操作"""
        async def handler(state: WorkflowState) -> WorkflowState:
            # 记录当前节点标识
            state["current_node"] = node_id
            state["status"] = "running"
            
            try:
                if node_type == NodeType.NAVIGATE:
                    url = config.get("url")
                    # 执行浏览器导航
                    if self.browser_engine:
                        await self.browser_engine.goto(url)
                    state["node_results"][node_id] = {
                        "action": "navigate",
                        "url": url,
                        "status": "success"
                    }
                
                elif node_type == NodeType.CLICK:
                    selector = config.get("selector")
                    if self.browser_engine:
                        await self.browser_engine.click(selector)
                    state["node_results"][node_id] = {
                        "action": "click",
                        "selector": selector,
                        "status": "success"
                    }
                
                elif node_type == NodeType.FILL:
                    selector = config.get("selector")
                    value = config.get("value")
                    if self.browser_engine:
                        await self.browser_engine.fill(selector, value)
                    state["node_results"][node_id] = {
                        "action": "fill",
                        "selector": selector,
                        "value": value,
                        "status": "success"
                    }
                
                elif node_type == NodeType.WAIT:
                    delay = config.get("delay", 1000)
                    # delay 单位为毫秒
                    await asyncio.sleep(delay / 1000.0)
                    state["node_results"][node_id] = {
                        "action": "wait",
                        "delay": delay,
                        "status": "success"
                    }
                
                elif node_type == NodeType.DOWNLOAD:
                    url = config.get("url")
                    filename = config.get("filename")
                    if self.browser_engine:
                        await self.browser_engine.download(url, filename)
                    state["node_results"][node_id] = {
                        "action": "download",
                        "url": url,
                        "filename": filename,
                        "status": "success"
                    }
                
                elif node_type == NodeType.START:
                    state["node_results"][node_id] = {
                        "action": "start",
                        "status": "success"
                    }
                
                elif node_type == NodeType.END:
                    state["status"] = "completed"
                    state["node_results"][node_id] = {
                        "action": "end",
                        "status": "success"
                    }
                
                # 标记为已完成的节点
                state["completed_nodes"].append(node_id)
                
            except Exception as e:
                state["failed_nodes"].append(node_id)
                state["error_message"] = str(e)
                state["status"] = "failed"
                
            return state
        
        return handler
    
    def _evaluate_condition(self, condition: Dict):
        """评估条件函数"""
        def check_condition(state: WorkflowState) -> str:
            # 简单的条件评估逻辑
            var_name = condition.get("variable")
            operator = condition.get("operator")
            value = condition.get("value")
            
            actual_value = state["variables"].get(var_name)
            
            if operator == "equals":
                return "true" if actual_value == value else "false"
            elif operator == "contains":
                return "true" if value in str(actual_value) else "false"
            elif operator == "exists":
                return "true" if actual_value else "false"
            
            return "false"
        
        return check_condition
    
    async def execute(self, initial_state: WorkflowState) -> WorkflowState:
        """执行工作流"""
        if not self.graph:
            raise ValueError("工作流图未初始化")
        
        result = await self.graph.ainvoke(initial_state)
        return result
    
    def validate(self, workflow_config: str) -> Dict[str, Any]:
        """验证工作流配置"""
        try:
            config = yaml.safe_load(workflow_config)
            errors = []
            warnings = []
            
            # 检查必需字段
            if "nodes" not in config:
                errors.append("缺少 nodes 配置")
            if "edges" not in config:
                errors.append("缺少 edges 配置")
            
            # 验证节点
            nodes = config.get("nodes", [])
            node_ids = set()
            for node in nodes:
                if "id" not in node:
                    errors.append("节点缺少 id 字段")
                if "type" not in node:
                    errors.append(f"节点 {node.get('id')} 缺少 type 字段")
                else:
                    valid_types = [t.value for t in NodeType]
                    if node["type"] not in valid_types:
                        errors.append(f"节点 {node.get('id')} 类型无效：{node['type']}")
                
                if "id" in node:
                    if node["id"] in node_ids:
                        errors.append(f"重复的节点 id: {node['id']}")
                    node_ids.add(node["id"])
            
            # 验证边
            edges = config.get("edges", [])
            for edge in edges:
                if "source" not in edge:
                    errors.append("边缺少 source 字段")
                if "target" not in edge:
                    errors.append("边缺少 target 字段")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
        
        except yaml.YAMLError as e:
            return {
                "valid": False,
                "errors": [f"YAML 解析错误：{str(e)}"]
            }
