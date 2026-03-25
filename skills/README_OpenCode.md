# OpenCode AI 配置指南

## 📋 概述

OpenCode AI 是一个基于 NVIDIA API 的智能代码助手，支持代码生成、解释、调试和优化功能。

## 🚀 快速开始

### 1. 环境准备

```bash
cd skills
source nvidia_env/bin/activate  # 激活虚拟环境
```

### 2. 测试配置

```bash
python test_opencode.py
```

### 3. 运行示例

```bash
python opencode_examples.py
```

## 📁 文件结构

```
skills/
├── config/
│   └── opencode_config.py       # OpenCode 配置文件
├── test_opencode.py             # 测试脚本
├── opencode_examples.py         # 使用示例
├── requirements_nvidia.txt      # 依赖包
└── README_OpenCode.md          # 本文档
```

## 🔧 核心功能

### 1. 代码生成 (Code Generation)

```python
from config.opencode_config import generate_code

# 生成 Python 代码
result = generate_code(
    prompt="写一个计算斐波那契数列的函数",
    language="python"
)

if result['success']:
    print(result['code'])
    print(f"使用 tokens: {result['tokens_used']}")
```

### 2. 代码解释 (Code Explanation)

```python
from config.opencode_config import explain_code

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

result = explain_code(code, "python")
if result['success']:
    print(result['explanation'])
```

### 3. 代码调试 (Code Debugging)

```python
from config.opencode_config import debug_code

buggy_code = """
def divide(a, b):
    return a / b
"""

result = debug_code(
    buggy_code,
    error_message="ZeroDivisionError: division by zero",
    language="python"
)

if result['success']:
    print(result['debug_info'])
```

### 4. 代码优化 (Code Optimization)

```python
from config.opencode_config import optimize_code

unoptimized_code = """
def find_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
"""

result = optimize_code(unoptimized_code, "python")
if result['success']:
    print(result['optimized_code'])
```

## 🎯 支持的编程语言

- **Python** - 全面支持，推荐使用
- **JavaScript/TypeScript** - Web 开发
- **Java** - 企业级应用
- **C/C++** - 系统编程
- **Go** - 云原生应用
- **Rust** - 系统级编程
- **PHP** - Web 后端
- **Ruby** - Web 开发
- **Swift** - iOS 开发
- **Kotlin** - Android 开发
- **Scala** - 大数据处理

## ⚙️ 配置参数

### 基础配置

```python
class OpenCodeConfig:
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = "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"
        self.model = "meta/llama-3.1-8b-instruct"
        self.temperature = 0.3  # 代码生成温度
        self.max_tokens = 2000  # 最大 token 数
```

### 系统提示词

OpenCode 使用专门的系统提示词来确保代码质量：

```
你是一个专业的代码助手，专门帮助用户编写、调试和优化代码。
你的任务是：
1. 根据用户需求生成高质量、可运行的代码
2. 提供清晰的代码注释和说明
3. 遵循最佳实践和编码规范
4. 优先考虑代码的可读性和可维护性
5. 如果需要，提供多种实现方案供用户选择
```

## 🛠️ 高级用法

### 1. 交互式编程会话

```python
# 构建上下文对话
context = ""
for step in development_steps:
    result = generate_code(step['prompt'], step['language'], context)
    if result['success']:
        context += f"\n{result['code']}"
```

### 2. 项目模板生成

```python
# 生成完整项目结构
project_types = [
    "React + TypeScript 项目",
    "FastAPI 后端项目", 
    "Django Web 应用",
    "Node.js Express 服务"
]

for project_type in project_types:
    result = generate_code(f"创建 {project_type} 的基础结构", "javascript")
```

### 3. 算法实现

```python
algorithms = [
    "快速排序算法",
    "二分查找算法",
    "动态规划 - 背包问题",
    "Dijkstra 最短路径算法"
]

for algo in algorithms:
    result = generate_code(f"实现 {algo}", "python")
```

## 📊 性能优化建议

### 1. Token 使用优化

- 使用简洁明确的提示词
- 避免过长的上下文
- 合理设置 `max_tokens` 参数

### 2. 温度参数调整

- **代码生成**: `temperature=0.3` (低温度，确保准确性)
- **代码解释**: `temperature=0.2` (更低温度，确保准确性)
- **创意性任务**: `temperature=0.7` (较高温度，增加多样性)

### 3. 模型选择

- **日常编程**: `meta/llama-3.1-8b-instruct` (推荐)
- **复杂任务**: `meta/llama-3.1-70b-instruct`
- **高质量要求**: `meta/llama-3.1-405b-instruct`

## 🔍 故障排除

### 常见问题

1. **API 连接失败**
   ```python
   # 检查网络连接和 API Key
   import requests
   response = requests.get("https://integrate.api.nvidia.com/v1/models")
   ```

2. **代码质量不佳**
   - 调整 `temperature` 参数
   - 优化提示词
   - 增加上下文信息

3. **Token 限制**
   - 调整 `max_tokens` 参数
   - 分解复杂任务为多个简单任务

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 在配置中启用详细日志
client = get_opencode_client()
# 查看详细的 API 请求和响应
```

## 🚀 集成示例

### 1. VS Code 扩展

```python
# 在 VS Code 扩展中使用
from config.opencode_config import generate_code

def generate_completion(prompt):
    result = generate_code(prompt, "python")
    return result['code'] if result['success'] else None
```

### 2. Web 应用集成

```python
# FastAPI 集成
from fastapi import FastAPI
from config.opencode_config import generate_code

app = FastAPI()

@app.post("/generate-code")
async def generate_code_api(prompt: str, language: str = "python"):
    result = generate_code(prompt, language)
    return result
```

### 3. 命令行工具

```python
# CLI 工具
import click
from config.opencode_config import generate_code

@click.command()
@click.argument('prompt')
@click.option('--language', default='python')
def cli_generate(prompt, language):
    result = generate_code(prompt, language)
    if result['success']:
        print(result['code'])
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    cli_generate()
```

## 📝 最佳实践

### 1. 提示词工程

- **明确具体**: 避免模糊的描述
- **包含上下文**: 提供相关的背景信息
- **指定语言**: 明确编程语言和版本
- **要求注释**: 请求代码注释和说明

### 2. 代码审查

- 始终测试生成的代码
- 检查安全漏洞
- 验证性能表现
- 确保符合编码规范

### 3. 持续学习

- 收集用户反馈
- 优化系统提示词
- 更新最佳实践
- 扩展语言支持

## 🎉 总结

OpenCode AI 为开发者提供了强大的代码辅助功能，通过 NVIDIA API 的高性能模型，能够显著提升编程效率和代码质量。

**开始使用**: `python test_opencode.py`

**查看示例**: `python opencode_examples.py`

---

**配置完成！现在你可以享受 AI 驱动的编程体验了！** 🚀
