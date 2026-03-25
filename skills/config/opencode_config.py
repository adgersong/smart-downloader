"""
OpenCode AI 配置文件
配置 OpenCode 客户端连接到 NVIDIA API 服务
"""
import os
from openai import OpenAI

class OpenCodeConfig:
    """OpenCode AI 配置类"""
    
    def __init__(self):
        # NVIDIA API 配置
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = "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"
        
        # OpenCode 专用配置
        self.model = "meta/llama-3.1-8b-instruct"  # 默认使用 Llama 3.1 8B
        self.temperature = 0.3  # 代码生成温度较低，确保准确性
        self.max_tokens = 2000  # 代码生成最大token数
        
        # 代码生成专用提示词模板
        self.system_prompt = """你是一个专业的代码助手，专门帮助用户编写、调试和优化代码。
你的任务是：
1. 根据用户需求生成高质量、可运行的代码
2. 提供清晰的代码注释和说明
3. 遵循最佳实践和编码规范
4. 优先考虑代码的可读性和可维护性
5. 如果需要，提供多种实现方案供用户选择

请用简洁明了的方式回答，专注于代码本身。"""
        
        # 支持的编程语言
        self.supported_languages = [
            "python", "javascript", "typescript", "java", "cpp", "c",
            "go", "rust", "php", "ruby", "swift", "kotlin", "scala"
        ]
    
    def get_client(self):
        """获取 OpenAI 客户端实例（用于 OpenCode）"""
        return OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
    
    def generate_code(self, prompt, language="python", context=None):
        """生成代码"""
        client = self.get_client()
        
        # 构建完整的提示词
        full_prompt = f"请用 {language} 语言编写以下代码：\n\n{prompt}"
        
        if context:
            full_prompt = f"上下文信息：\n{context}\n\n{full_prompt}"
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return {
                "success": True,
                "code": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": None
            }
    
    def explain_code(self, code, language="python"):
        """解释代码"""
        client = self.get_client()
        
        prompt = f"请详细解释以下 {language} 代码的功能和实现逻辑：\n\n```{language}\n{code}\n```"
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个代码解释专家，能够清晰准确地解释代码的功能和逻辑。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            return {
                "success": True,
                "explanation": response.choices[0].message.content,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "explanation": None
            }
    
    def debug_code(self, code, error_message=None, language="python"):
        """调试代码"""
        client = self.get_client()
        
        prompt = f"请帮我调试以下 {language} 代码：\n\n```{language}\n{code}\n```"
        
        if error_message:
            prompt += f"\n\n错误信息：\n{error_message}"
        
        prompt += "\n\n请指出问题所在并提供修复方案。"
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个代码调试专家，能够快速定位和修复代码问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return {
                "success": True,
                "debug_info": response.choices[0].message.content,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "debug_info": None
            }
    
    def optimize_code(self, code, language="python"):
        """优化代码"""
        client = self.get_client()
        
        prompt = f"请优化以下 {language} 代码的性能和可读性：\n\n```{language}\n{code}\n```\n\n请提供优化后的代码和优化说明。"
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个代码优化专家，能够显著提升代码性能和可读性。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            
            return {
                "success": True,
                "optimized_code": response.choices[0].message.content,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "optimized_code": None
            }

# 全局配置实例
opencode_config = OpenCodeConfig()

# 便捷函数
def get_opencode_client():
    """获取 OpenCode 客户端"""
    return opencode_config.get_client()

def generate_code(prompt, language="python", context=None):
    """生成代码的便捷函数"""
    return opencode_config.generate_code(prompt, language, context)

def explain_code(code, language="python"):
    """解释代码的便捷函数"""
    return opencode_config.explain_code(code, language)

def debug_code(code, error_message=None, language="python"):
    """调试代码的便捷函数"""
    return opencode_config.debug_code(code, error_message, language)

def optimize_code(code, language="python"):
    """优化代码的便捷函数"""
    return opencode_config.optimize_code(code, language)
