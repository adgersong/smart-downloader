"""
Qwen VL 视觉引擎模块
基于 Ollama 的视觉语言模型集成
"""
import httpx
import base64
from typing import List, Dict, Any, Optional
from loguru import logger


class QwenVLEngine:
    """Qwen VL 视觉引擎"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "qwen-vl"):
        self.ollama_url = ollama_url
        self.model = model
    
    def _encode_image(self, image_path: str) -> str:
        """将图片编码为 base64"""
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        return image_data
    
    async def analyze_image(
        self,
        image_path: str,
        prompt: str = "描述这张图片",
        timeout: int = 30
    ) -> str:
        """分析图片"""
        try:
            image_base64 = self._encode_image(image_path)
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "images": [image_base64],
                        "stream": False
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        
        except Exception as e:
            logger.error(f"图片分析失败：{str(e)}")
            raise
    
    async def detect_elements(
        self,
        image_path: str
    ) -> Dict[str, Any]:
        """检测页面元素"""
        prompt = """分析这个网页截图，识别所有可交互的 UI 元素。
对于每个元素，提供：
1. 元素类型 (button/input/link/checkbox/select/table)
2. 元素上的文字内容
3. 元素的大致位置 (左上/中/右下等)
4. 元素可能的功能

以 JSON 格式返回，格式为：
{
    "elements": [
        {"type": "button", "text": "登录", "position": "中心", "function": "提交登录表单"}
    ]
}"""
        
        response = await self.analyze_image(image_path, prompt)
        
        try:
            import json
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"解析元素检测结果失败：{e}")
        
        return {"elements": [], "raw_response": response}
    
    async def parse_intent(
        self,
        image_path: str,
        annotations: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """解析用户意图 (支持标注)"""
        if annotations:
            prompt = f"""分析这个已标注的页面截图。
标注信息：{annotations}

请根据标注识别用户的操作意图，并生成对应的操作序列。
返回 JSON 格式：
{{
    "intent": "用户想要执行的操作",
    "actions": [
        {{"type": "click", "target": "元素描述"}},
        {{"type": "input", "target": "输入框", "value": "内容"}}
    ]
}}"""
        else:
            prompt = """分析这个页面截图，推断用户可能的操作意图。
识别页面中最可能的操作流程 (如登录、搜索、点击下载等)。
返回 JSON 格式：
{
    "intent": "推断的意图",
    "suggested_actions": [
        {"type": "click", "target": "元素描述"}
    ]
}"""
        
        response = await self.analyze_image(image_path, prompt)
        
        try:
            import json
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"解析意图失败：{e}")
        
        return {
            "intent": "未知",
            "actions": [],
            "suggested_actions": [],
            "raw_response": response
        }
    
    async def text_to_workflow(self, description: str) -> Dict[str, Any]:
        """文字描述转工作流"""
        prompt = f"""将以下操作描述转换为自动化工作流配置。

操作描述：{description}

请生成 YAML 格式的工作流配置，包含 nodes 和 edges。
节点类型支持：start, end, navigate, click, fill, wait, download

示例格式：
nodes:
  - id: start
    type: start
  - id: nav1
    type: navigate
    config:
      url: https://example.com
  - id: click1
    type: click
    config:
      selector: "#login-btn"
edges:
  - source: start
    target: nav1
  - source: nav1
    target: click1

直接返回 YAML 内容，不要用代码块包裹。"""
        
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": "qwen2.5:7b",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                yaml_content = result.get("response", "")
                
                return {
                    "yaml_config": yaml_content,
                    "success": True
                }
        
        except Exception as e:
            logger.error(f"文字转工作流失败：{str(e)}")
            return {
                "yaml_config": "",
                "success": False,
                "error": str(e)
            }
    
    async def check_health(self) -> bool:
        """检查 Ollama 服务健康状态"""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return any(self.model in m.get("name", "") for m in models)
        except Exception:
            pass
        return False


# 全局引擎实例
_engine = None


def get_qwen_engine() -> QwenVLEngine:
    """获取全局 Qwen VL 引擎实例"""
    global _engine
    if _engine is None:
        _engine = QwenVLEngine()
    return _engine
