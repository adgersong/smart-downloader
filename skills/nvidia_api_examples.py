"""
NVIDIA API 便捷使用示例
展示如何在项目中使用配置好的 NVIDIA API
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.nvidia_api_config import get_nvidia_client, get_available_models

class NVIDIAChatBot:
    """基于 NVIDIA API 的聊天机器人"""
    
    def __init__(self, model="meta/llama-3.1-8b-instruct"):
        self.client = get_nvidia_client()
        self.model = model
        self.conversation_history = []
    
    def chat(self, message, system_prompt=None):
        """发送消息并获取回复"""
        # 构建消息历史
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加历史对话
        messages.extend(self.conversation_history)
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            # 保持历史记录在合理范围内
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return reply
            
        except Exception as e:
            return f"错误: {str(e)}"
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def stream_chat(self, message, system_prompt=None):
        """流式聊天"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # 更新历史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            yield f"错误: {str(e)}"

def example_usage():
    """使用示例"""
    print("🤖 NVIDIA API 使用示例")
    print("=" * 50)
    
    # 创建聊天机器人
    bot = NVIDIAChatBot()
    
    # 示例1：简单对话
    print("\n1️⃣ 简单对话示例:")
    response = bot.chat("你好！请介绍一下你的能力。")
    print(f"用户: 你好！请介绍一下你的能力。")
    print(f"AI: {response}")
    
    # 示例2：带系统提示
    print("\n2️⃣ 带系统提示的对话:")
    system_prompt = "你是一个专业的Python程序员，请用简洁的语言回答问题。"
    response = bot.chat("什么是装饰器？", system_prompt)
    print(f"系统提示: {system_prompt}")
    print(f"用户: 什么是装饰器？")
    print(f"AI: {response}")
    
    # 示例3：流式对话
    print("\n3️⃣ 流式对话示例:")
    print("AI: ", end="", flush=True)
    for chunk in bot.stream_chat("请用3句话解释机器学习"):
        print(chunk, end="", flush=True)
    print()
    
    # 示例4：多轮对话
    print("\n4️⃣ 多轮对话示例:")
    response1 = bot.chat("我想学习Python，有什么建议吗？")
    print(f"用户: 我想学习Python，有什么建议吗？")
    print(f"AI: {response1}")
    
    response2 = bot.chat("能推荐一些学习资源吗？")
    print(f"用户: 能推荐一些学习资源吗？")
    print(f"AI: {response2}")

def model_comparison():
    """模型对比示例"""
    print("\n🎯 模型对比示例")
    print("=" * 50)
    
    test_prompt = "解释什么是人工智能，用一句话回答。"
    models_to_test = [
        "meta/llama-3.1-8b-instruct",
        "mistralai/mixtral-8x7b-instruct-v0.1"
    ]
    
    for model in models_to_test:
        print(f"\n📝 测试模型: {model}")
        bot = NVIDIAChatBot(model=model)
        response = bot.chat(test_prompt)
        print(f"回答: {response}")

if __name__ == "__main__":
    # 运行示例
    example_usage()
    model_comparison()
    
    print("\n✅ 示例运行完成！")
    print("💡 提示: 你可以基于这些示例在自己的项目中使用 NVIDIA API")
