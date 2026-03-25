"""
OpenCode AI 使用示例
展示如何使用配置好的 OpenCode 进行各种编程任务
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.opencode_config import (
    generate_code, 
    explain_code, 
    debug_code, 
    optimize_code
)

def example_code_generation():
    """代码生成示例"""
    print("💻 代码生成示例")
    print("=" * 50)
    
    # 示例1：Python 函数
    print("\n1️⃣ 生成 Python 函数:")
    prompt = "写一个函数，检查字符串是否为回文"
    result = generate_code(prompt, "python")
    
    if result['success']:
        print(f"✅ 生成成功 (使用 {result['tokens_used']} tokens)")
        print("生成的代码:")
        print(result['code'])
    
    # 示例2：React 组件
    print("\n2️⃣ 生成 React 组件:")
    prompt = "创建一个登录表单组件，包含用户名和密码输入框"
    result = generate_code(prompt, "javascript")
    
    if result['success']:
        print(f"✅ 生成成功 (使用 {result['tokens_used']} tokens)")
        print("生成的代码:")
        print(result['code'])

def example_code_explanation():
    """代码解释示例"""
    print("\n🔍 代码解释示例")
    print("=" * 50)
    
    complex_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""
    
    print("要解释的代码:")
    print(complex_code)
    
    result = explain_code(complex_code, "python")
    
    if result['success']:
        print("\n✅ 解释成功!")
        print("解释内容:")
        print(result['explanation'])

def example_code_debugging():
    """代码调试示例"""
    print("\n🐛 代码调试示例")
    print("=" * 50)
    
    buggy_code = """
def find_max(numbers):
    max_num = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num
"""
    
    error_msg = "IndexError: list index out of range when input list is empty"
    
    print("有问题的代码:")
    print(buggy_code)
    print(f"错误信息: {error_msg}")
    
    result = debug_code(buggy_code, error_msg, "python")
    
    if result['success']:
        print("\n✅ 调试成功!")
        print("调试信息:")
        print(result['debug_info'])

def example_code_optimization():
    """代码优化示例"""
    print("\n⚡ 代码优化示例")
    print("=" * 50)
    
    unoptimized_code = """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
"""
    
    print("未优化的代码:")
    print(unoptimized_code)
    
    result = optimize_code(unoptimized_code, "python")
    
    if result['success']:
        print("\n✅ 优化成功!")
        print("优化结果:")
        print(result['optimized_code'])

def example_project_development():
    """项目开发示例"""
    print("\n🏗️ 项目开发示例")
    print("=" * 50)
    
    # 模拟开发一个简单的待办事项应用
    project_steps = [
        {
            "step": "创建数据模型",
            "prompt": "创建一个 Todo 类，包含 id、title、completed 和 created_at 属性",
            "language": "python"
        },
        {
            "step": "实现数据存储",
            "prompt": "创建一个 TodoManager 类，用于管理 Todo 对象的增删改查",
            "language": "python"
        },
        {
            "step": "创建API接口",
            "prompt": "使用 FastAPI 创建 Todo 的 REST API 接口",
            "language": "python"
        }
    ]
    
    context = ""
    
    for i, step_info in enumerate(project_steps, 1):
        print(f"\n📝 步骤 {i}: {step_info['step']}")
        print(f"需求: {step_info['prompt']}")
        
        result = generate_code(
            step_info['prompt'],
            step_info['language'],
            context
        )
        
        if result['success']:
            print(f"✅ 生成成功!")
            print("生成的代码:")
            print(result['code'])
            
            # 更新上下文，让后续生成考虑之前的代码
            context += f"\n=== {step_info['step']} ===\n{result['code']}\n"
        else:
            print(f"❌ 生成失败: {result['error']}")

def example_multilanguage_project():
    """多语言项目示例"""
    print("\n🌍 多语言项目示例")
    print("=" * 50)
    
    # 同一个功能在不同语言中的实现
    task = "实现一个简单的计算器类，支持加减乘除运算"
    
    languages = ["python", "javascript", "java", "cpp"]
    
    for lang in languages:
        print(f"\n💻 {lang.upper()} 实现:")
        result = generate_code(task, lang)
        
        if result['success']:
            print(f"✅ {lang} 代码生成成功!")
            print(result['code'])
        else:
            print(f"❌ {lang} 代码生成失败: {result['error']}")

def example_learning_assistance():
    """学习辅助示例"""
    print("\n📚 学习辅助示例")
    print("=" * 50)
    
    # 为初学者生成学习代码
    learning_topics = [
        {
            "topic": "变量和数据类型",
            "prompt": "为初学者创建一个示例，展示 Python 中的基本数据类型",
            "language": "python"
        },
        {
            "topic": "循环结构",
            "prompt": "创建一个示例，展示 for 循环和 while 循环的用法",
            "language": "python"
        },
        {
            "topic": "函数定义",
            "prompt": "创建一个示例，展示如何定义和调用函数，包括参数传递",
            "language": "python"
        }
    ]
    
    for topic_info in learning_topics:
        print(f"\n📖 {topic_info['topic']}:")
        result = generate_code(
            topic_info['prompt'],
            topic_info['language']
        )
        
        if result['success']:
            print("✅ 学习示例生成成功!")
            print("示例代码:")
            print(result['code'])
            
            # 为代码添加解释
            explanation = explain_code(result['code'], topic_info['language'])
            if explanation['success']:
                print("\n解释:")
                print(explanation['explanation'])
        else:
            print(f"❌ 学习示例生成失败: {result['error']}")

def main():
    """主函数"""
    print("🤖 OpenCode AI 使用示例")
    print("=" * 60)
    
    examples = [
        example_code_generation,
        example_code_explanation,
        example_code_debugging,
        example_code_optimization,
        example_project_development,
        example_multilanguage_project,
        example_learning_assistance
    ]
    
    for example_func in examples:
        try:
            example_func()
            print("\n" + "-" * 60)
        except Exception as e:
            print(f"❌ 示例运行失败: {str(e)}")
    
    print("✅ 所有示例运行完成！")
    print("💡 你现在可以在自己的项目中使用 OpenCode AI 了！")

if __name__ == "__main__":
    main()
