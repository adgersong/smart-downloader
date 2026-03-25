# NVIDIA API 配置指南

## 📋 概述

本项目已配置好 NVIDIA API 的 OpenAI 客户端，你可以直接使用 NVIDIA 的大模型服务。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills
pip install -r requirements_nvidia.txt
```

### 2. 测试连接

```bash
python test_nvidia_api.py
```

### 3. 运行示例

```bash
python nvidia_api_examples.py
```

## 📁 文件结构

```
skills/
├── config/
│   └── nvidia_api_config.py    # 配置文件
├── test_nvidia_api.py          # 测试脚本
├── nvidia_api_examples.py      # 使用示例
├── requirements_nvidia.txt     # 依赖包
└── README_NVIDIA.md           # 本文档
```

## 🔧 使用方法

### 基础用法

```python
from config.nvidia_api_config import get_nvidia_client

# 获取客户端
client = get_nvidia_client()

# 聊天完成
response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[
        {"role": "user", "content": "你好！"}
    ]
)

print(response.choices[0].message.content)
```

### 聊天机器人类

```python
from nvidia_api_examples import NVIDIAChatBot

# 创建机器人
bot = NVIDIAChatBot()

# 对话
response = bot.chat("请介绍一下人工智能")
print(response)

# 流式对话
for chunk in bot.stream_chat("解释机器学习"):
    print(chunk, end="", flush=True)
```

## 🎯 支持的模型

- `meta/llama-3.1-405b-instruct` - Llama 3.1 405B
- `meta/llama-3.1-70b-instruct` - Llama 3.1 70B  
- `meta/llama-3.1-8b-instruct` - Llama 3.1 8B (推荐)
- `mistralai/mixtral-8x7b-instruct-v0.1` - Mixtral 8x7B
- `google/gemma-2-27b-it` - Gemma 2 27B
- `microsoft/phi-3-medium-128k-instruct` - Phi-3 Medium
- `nvidia/nemotron-4-340b-instruct` - Nemotron 4 340B

## ⚙️ 配置说明

配置文件位于 `config/nvidia_api_config.py`：

```python
class NVIDIAConfig:
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = "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"
        self.default_model = "meta/llama-3.1-8b-instruct"
```

## 🛠️ 高级功能

### 1. 自定义系统提示

```python
response = bot.chat(
    "解释Python装饰器",
    system_prompt="你是一个专业的Python程序员"
)
```

### 2. 对话历史管理

```python
bot.clear_history()  # 清空历史
# 历史会自动维护在合理范围内
```

### 3. 流式响应

```python
for chunk in bot.stream_chat("写一首诗"):
    print(chunk, end="", flush=True)
```

## 📊 测试功能

测试脚本包含以下功能：

- ✅ API 连接测试
- ✅ 聊天完成测试
- ✅ 流式聊天测试
- ✅ 多模型对比测试

运行测试：

```bash
python test_nvidia_api.py
```

## 🔍 故障排除

### 常见问题

1. **连接超时**
   - 检查网络连接
   - 确认 API Key 有效

2. **模型不可用**
   - 检查模型名称拼写
   - 查看支持模型列表

3. **配额限制**
   - NVIDIA API 有调用限制
   - 适当控制请求频率

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 集成到项目

### 在 FastAPI 中使用

```python
from config.nvidia_api_config import get_nvidia_client
from fastapi import FastAPI

app = FastAPI()
client = get_nvidia_client()

@app.post("/chat")
async def chat(message: str):
    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": message}]
    )
    return {"response": response.choices[0].message.content}
```

### 在 LangGraph 中使用

```python
from config.nvidia_api_config import get_nvidia_client
from langgraph.graph import StateGraph

client = get_nvidia_client()

def ai_node(state):
    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": state["input"]}]
    )
    state["output"] = response.choices[0].message.content
    return state
```

## 📝 更新日志

- **v1.0** - 初始配置，支持基础聊天功能
- 支持流式响应
- 集成多种模型
- 完整的测试套件

## 🤝 支持

如有问题，请检查：
1. 网络连接
2. API Key 有效性
3. 模型名称正确性
4. 依赖包版本

---

**配置完成！现在你可以使用 NVIDIA 的强大 AI 模型了！** 🎉
