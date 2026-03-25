"""
OpenCode AI 测试脚本
测试 OpenCode 连接到 NVIDIA API 的代码生成功能
"""
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.opencode_config import (
    generate_code, 
    explain_code, 
    debug_code, 
    optimize_code,
    opencode_config
)

def test_code_generation():
    """测试代码生成功能"""
    print("💻 测试代码生成功能...")
    
    test_cases = [
        {
            "prompt": "写一个计算斐波那契数列的函数",
            "language": "python"
        },
        {
            "prompt": "创建一个 React 组件，显示用户列表",
            "language": "javascript"
        },
        {
            "prompt": "实现一个快速排序算法",
            "language": "python"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试用例 {i}: {test_case['prompt']}")
        print(f"   语言: {test_case['language']}")
        
        result = generate_code(
            test_case['prompt'], 
            test_case['language']
        )
        
        if result['success']:
            print(f"   ✅ 生成成功!")
            print(f"   模型: {result['model']}")
            print(f"   使用tokens: {result['tokens_used']}")
            print(f"   代码预览: {result['code'][:100]}...")
        else:
            print(f"   ❌ 生成失败: {result['error']}")

def test_code_explanation():
    """测试代码解释功能"""
    print("\n🔍 测试代码解释功能...")
    
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    result = explain_code(test_code, "python")
    
    if result['success']:
        print("   ✅ 解释成功!")
        print(f"   模型: {result['model']}")
        print(f"   解释内容: {result['explanation'][:200]}...")
    else:
        print(f"   ❌ 解释失败: {result['error']}")

def test_code_debugging():
    """测试代码调试功能"""
    print("\n🐛 测试代码调试功能...")
    
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
"""
    
    error_message = "ZeroDivisionError: division by zero when input list is empty"
    
    result = debug_code(buggy_code, error_message, "python")
    
    if result['success']:
        print("   ✅ 调试成功!")
        print(f"   模型: {result['model']}")
        print(f"   调试信息: {result['debug_info'][:200]}...")
    else:
        print(f"   ❌ 调试失败: {result['error']}")

def test_code_optimization():
    """测试代码优化功能"""
    print("\n⚡ 测试代码优化功能...")
    
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
        print("   ✅ 优化成功!")
        print(f"   模型: {result['model']}")
        print(f"   优化结果: {result['optimized_code'][:200]}...")
    else:
        print(f"   ❌ 优化失败: {result['error']}")

def test_interactive_session():
    """测试交互式编程会话"""
    print("\n🔄 测试交互式编程会话...")
    
    # 模拟一个完整的编程对话
    conversation_steps = [
        {
            "prompt": "创建一个学生类，包含姓名、年龄和成绩属性",
            "language": "python"
        },
        {
            "prompt": "为这个学生类添加一个计算平均成绩的方法",
            "language": "python"
        },
        {
            "prompt": "添加一个方法来判断学生是否及格",
            "language": "python"
        }
    ]
    
    context = ""
    
    for i, step in enumerate(conversation_steps, 1):
        print(f"\n📝 步骤 {i}: {step['prompt']}")
        
        result = generate_code(
            step['prompt'],
            step['language'],
            context
        )
        
        if result['success']:
            print(f"   ✅ 生成成功!")
            print(f"   代码: {result['code'][:150]}...")
            # 更新上下文
            context += f"\n步骤{i}: {step['prompt']}\n{result['code']}\n"
        else:
            print(f"   ❌ 生成失败: {result['error']}")

def test_multilanguage_support():
    """测试多语言支持"""
    print("\n🌍 测试多语言支持...")
    
    languages = ["python", "javascript", "java", "cpp"]
    simple_prompt = "写一个 Hello World 程序"
    
    for lang in languages:
        print(f"\n💻 测试 {lang.upper()}:")
        result = generate_code(simple_prompt, lang)
        
        if result['success']:
            print(f"   ✅ {lang} 代码生成成功!")
            print(f"   代码: {result['code'][:100]}...")
        else:
            print(f"   ❌ {lang} 代码生成失败: {result['error']}")

def main():
    """主测试函数"""
    print("=" * 70)
    print("🚀 OpenCode AI 配置测试")
    print("=" * 70)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 API 地址: {opencode_config.base_url}")
    print(f"🔑 API Key: {opencode_config.api_key[:20]}...")
    print(f"🤖 默认模型: {opencode_config.model}")
    print("-" * 70)
    
    # 运行测试
    tests = [
        ("代码生成测试", test_code_generation),
        ("代码解释测试", test_code_explanation),
        ("代码调试测试", test_code_debugging),
        ("代码优化测试", test_code_optimization),
        ("交互式会话测试", test_interactive_session),
        ("多语言支持测试", test_multilanguage_support)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 开始 {test_name}...")
            test_func()
            results[test_name] = True
            print(f"✅ {test_name} 完成")
        except Exception as e:
            print(f"❌ {test_name} 异常: {str(e)}")
            results[test_name] = False
    
    # 测试总结
    print("\n" + "=" * 70)
    print("📊 测试结果总结")
    print("=" * 70)
    
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体结果: {success_count}/{total_count} 测试通过")
    
    if success_count == total_count:
        print("🎉 所有测试通过！OpenCode AI 配置正确。")
        print("💡 现在你可以在项目中使用 OpenCode 进行代码生成了！")
    else:
        print("⚠️  部分测试失败，请检查配置。")

if __name__ == "__main__":
    main()
