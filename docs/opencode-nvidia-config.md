# opencode NVIDIA 大模型配置指南

## 已配置模型

| 模型 | 用途 | 特点 |
|------|------|------|
| `gpt-oss-120b` | 代码生成/复杂推理 | 120B 参数，支持推理链 |
| `llama-3.1-405b` | 通用对话/文档 | 405B 参数，高质量输出 |

## 使用方法

### 1. 全局使用

编辑 `~/.config/opencode/providers.json` (已配置)

### 2. 项目级别配置

在项目根目录创建 `.opencode/config.json`:

```json
{
  "provider": "nvidia",
  "model": "gpt-oss-120b",
  "temperature": 1,
  "max_tokens": 4096
}
```

### 3. 命令行使用

```bash
# 使用 NVIDIA 模型
opencode --provider nvidia --model gpt-oss-120b

# 或直接设置环境变量
export OPENCODE_PROVIDER=nvidia
export OPENCODE_MODEL=gpt-oss-120b
opencode
```

## 代码示例

### Python 调用

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key="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"
)

completion = client.chat.completions.create(
  model="openai/gpt-oss-120b",
  messages=[{"role":"user","content":"你好，请帮我写个 Python 函数"}],
  temperature=1,
  max_tokens=4096,
  stream=True
)

for chunk in completion:
  if chunk.choices and chunk.choices[0].delta.content:
    print(chunk.choices[0].delta.content, end="")
```

### Node.js 调用

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://integrate.api.nvidia.com/v1',
  apiKey: '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'
});

const completion = await client.chat.completions.create({
  model: 'openai/gpt-oss-120b',
  messages: [{ role: 'user', content: '你好' }],
  stream: true
});

for await (const chunk of completion) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

## 可用模型列表

### NVIDIA API _catalog

| 模型名称 | 参数 | 适用场景 |
|---------|------|----------|
| `openai/gpt-oss-120b` | 120B | 代码/推理 |
| `meta/llama-3.1-405b-instruct` | 405B | 通用对话 |
| `01ai/yi-large` | 34B | 中英文混合 |
| `mistralai/mixtral-8x22b-instruct` | 39B | 快速响应 |

## 最佳实践

### 代码生成
```json
{
  "model": "gpt-oss-120b",
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### 文档写作
```json
{
  "model": "llama-3.1-405b",
  "temperature": 0.5,
  "max_tokens": 2048
}
```

### 创意写作
```json
{
  "model": "gpt-oss-120b",
  "temperature": 1.0,
  "max_tokens": 4096
}
```

## 故障排查

### API Key 无效
```bash
# 测试 API Key
curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer nvapi-***" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":"test"}]}'
```

### 模型不可用
检查模型名称是否正确：
- ✅ `openai/gpt-oss-120b`
- ❌ `gpt-oss-120b`

---

**配置位置**: `~/.config/opencode/providers.json`  
**状态**: ✅ 已配置
