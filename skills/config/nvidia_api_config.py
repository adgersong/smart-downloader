"""
NVIDIA API 配置文件
用于配置 OpenAI 客户端连接到 NVIDIA 的 API 服务
"""
import os
from openai import OpenAI

class NVIDIAConfig:
    """NVIDIA API 配置类"""
    
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = "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"
        
        # 支持的模型列表
        self.supported_models = [
            "meta/llama-3.1-405b-instruct",
            "meta/llama-3.1-70b-instruct", 
            "meta/llama-3.1-8b-instruct",
            "mistralai/mixtral-8x7b-instruct-v0.1",
            "google/gemma-2-27b-it",
            "microsoft/phi-3-medium-128k-instruct",
            "nvidia/nemotron-4-340b-instruct"
        ]
        
        # 默认模型
        self.default_model = "meta/llama-3.1-8b-instruct"
    
    def get_client(self):
        """获取 OpenAI 客户端实例"""
        return OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
    
    def get_model_list(self):
        """获取支持的模型列表"""
        return self.supported_models
    
    def validate_model(self, model_name):
        """验证模型是否支持"""
        return model_name in self.supported_models

# 全局配置实例
nvidia_config = NVIDIAConfig()

# 便捷函数
def get_nvidia_client():
    """获取 NVIDIA API 客户端"""
    return nvidia_config.get_client()

def get_available_models():
    """获取可用模型列表"""
    return nvidia_config.get_model_list()
