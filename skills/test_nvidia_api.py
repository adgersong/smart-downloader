"""
NVIDIA API 测试脚本
测试 OpenAI 客户端连接到 NVIDIA API 的功能
"""
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.nvidia_api_config import get_nvidia_client, get_available_models, nvidia_config

def test_connection():
    """测试 API 连接"""
    print("🔗 测试 NVIDIA API 连接...")
    
    try:
        client = get_nvidia_client()
        
        # 测试模型列表
        models = client.models.list()
        print(f"✅ 连接成功！获取到 {len(models.data)} 个模型")
        
        # 显示前5个模型
        for i, model in enumerate(models.data[:5]):
            print(f"   {i+1}. {model.id}")
            
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False

def test_chat_completion(model="meta/llama-3.1-8b-instruct"):
    """测试聊天完成功能"""
    print(f"\n💬 测试聊天完成 (模型: {model})...")
    
    try:
        client = get_nvidia_client()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个有用的AI助手。"},
                {"role": "user", "content": "请简单介绍一下你自己。"}
            ],
            max_tokens=200,
            temperature=0.7,
            stream=False
        )
        
        print(f"✅ 聊天测试成功！")
        print(f"   响应: {response.choices[0].message.content}")
        print(f"   使用token: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ 聊天测试失败: {str(e)}")
        return False

def test_streaming_chat():
    """测试流式聊天"""
    print(f"\n🌊 测试流式聊天...")
    
    try:
        client = get_nvidia_client()
        
        stream = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {"role": "user", "content": "请用3句话介绍人工智能"}
            ],
            max_tokens=150,
            stream=True
        )
        
        print("   流式响应: ", end="")
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n✅ 流式聊天测试成功！")
        
        return True
        
    except Exception as e:
        print(f"❌ 流式聊天测试失败: {str(e)}")
        return False

def test_multiple_models():
    """测试多个模型"""
    print(f"\n🎯 测试多个模型...")
    
    test_models = [
        "meta/llama-3.1-8b-instruct",
        "mistralai/mixtral-8x7b-instruct-v0.1"
    ]
    
    results = {}
    
    for model in test_models:
        try:
            client = get_nvidia_client()
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "用一句话回答：什么是AI？"}
                ],
                max_tokens=50
            )
            
            results[model] = {
                "success": True,
                "response": response.choices[0].message.content
            }
            print(f"   ✅ {model}: {response.choices[0].message.content}")
            
        except Exception as e:
            results[model] = {
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ {model}: {str(e)}")
    
    return results

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 NVIDIA API 配置测试")
    print("=" * 60)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 API 地址: {nvidia_config.base_url}")
    print(f"🔑 API Key: {nvidia_config.api_key[:20]}...")
    print("-" * 60)
    
    # 运行测试
    tests = [
        ("连接测试", test_connection),
        ("聊天完成测试", lambda: test_chat_completion()),
        ("流式聊天测试", test_streaming_chat),
        ("多模型测试", test_multiple_models)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} 异常: {str(e)}")
            results[test_name] = False
    
    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    success_count = sum(1 for result in results.values() if result is not False)
    total_count = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result is not False else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {success_count}/{total_count} 测试通过")
    
    if success_count == total_count:
        print("🎉 所有测试通过！NVIDIA API 配置正确。")
    else:
        print("⚠️  部分测试失败，请检查配置。")

if __name__ == "__main__":
    main()
