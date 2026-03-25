#!/usr/bin/env python3
"""
OpenCode AI 快速使用脚本
简化版接口，方便日常使用
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.opencode_config import generate_code, explain_code, debug_code, optimize_code

def quick_generate():
    """快速代码生成"""
    print("💻 OpenCode AI 代码生成")
    print("=" * 40)
    
    prompt = input("请描述你想要的代码: ")
    language = input("编程语言 (默认python): ") or "python"
    
    print(f"\n🤖 正在生成 {language} 代码...")
    result = generate_code(prompt, language)
    
    if result['success']:
        print("\n✅ 生成成功!")
        print(f"📊 使用 tokens: {result['tokens_used']}")
        print("\n📝 生成的代码:")
        print("-" * 40)
        print(result['code'])
        print("-" * 40)
    else:
        print(f"❌ 生成失败: {result['error']}")

def quick_explain():
    """快速代码解释"""
    print("🔍 OpenCode AI 代码解释")
    print("=" * 40)
    
    print("请输入要解释的代码 (输入 'END' 结束):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    
    code = '\n'.join(lines)
    language = input("编程语言 (默认python): ") or "python"
    
    print(f"\n🤖 正在解释 {language} 代码...")
    result = explain_code(code, language)
    
    if result['success']:
        print("\n✅ 解释成功!")
        print("\n📝 代码解释:")
        print("-" * 40)
        print(result['explanation'])
        print("-" * 40)
    else:
        print(f"❌ 解释失败: {result['error']}")

def quick_debug():
    """快速代码调试"""
    print("🐛 OpenCode AI 代码调试")
    print("=" * 40)
    
    print("请输入有问题的代码 (输入 'END' 结束):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    
    code = '\n'.join(lines)
    error_msg = input("错误信息 (可选): ") or None
    language = input("编程语言 (默认python): ") or "python"
    
    print(f"\n🤖 正在调试 {language} 代码...")
    result = debug_code(code, error_msg, language)
    
    if result['success']:
        print("\n✅ 调试成功!")
        print("\n📝 调试信息:")
        print("-" * 40)
        print(result['debug_info'])
        print("-" * 40)
    else:
        print(f"❌ 调试失败: {result['error']}")

def quick_optimize():
    """快速代码优化"""
    print("⚡ OpenCode AI 代码优化")
    print("=" * 40)
    
    print("请输入要优化的代码 (输入 'END' 结束):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    
    code = '\n'.join(lines)
    language = input("编程语言 (默认python): ") or "python"
    
    print(f"\n🤖 正在优化 {language} 代码...")
    result = optimize_code(code, language)
    
    if result['success']:
        print("\n✅ 优化成功!")
        print("\n📝 优化后的代码:")
        print("-" * 40)
        print(result['optimized_code'])
        print("-" * 40)
    else:
        print(f"❌ 优化失败: {result['error']}")

def interactive_mode():
    """交互式模式"""
    print("🔄 OpenCode AI 交互式模式")
    print("=" * 40)
    print("输入 'help' 查看命令，输入 'quit' 退出")
    
    context = ""
    
    while True:
        command = input("\n> ").strip()
        
        if command.lower() in ['quit', 'exit', 'q']:
            print("👋 再见!")
            break
        elif command.lower() == 'help':
            print_help()
        elif command.lower() == 'clear':
            context = ""
            print("🧹 上下文已清空")
        elif command.lower().startswith('gen'):
            prompt = command[4:].strip() or input("请描述代码需求: ")
            language = input("编程语言 (默认python): ") or "python"
            
            result = generate_code(prompt, language, context)
            if result['success']:
                print(result['code'])
                context += f"\n用户: {prompt}\nAI: {result['code']}\n"
            else:
                print(f"❌ 失败: {result['error']}")
        else:
            # 默认当作代码生成请求
            language = input("编程语言 (默认python): ") or "python"
            result = generate_code(command, language, context)
            if result['success']:
                print(result['code'])
                context += f"\n用户: {command}\nAI: {result['code']}\n"
            else:
                print(f"❌ 失败: {result['error']}")

def print_help():
    """显示帮助信息"""
    print("""
📖 OpenCode AI 命令帮助:
  gen <prompt>     - 生成代码
  clear           - 清空上下文
  help            - 显示帮助
  quit/exit/q     - 退出程序
  
直接输入文本也会尝试生成对应的代码
    """)

def main():
    """主菜单"""
    print("🤖 OpenCode AI 智能编程助手")
    print("=" * 50)
    
    while True:
        print("\n请选择功能:")
        print("1. 💻 代码生成")
        print("2. 🔍 代码解释")
        print("3. 🐛 代码调试")
        print("4. ⚡ 代码优化")
        print("5. 🔄 交互式模式")
        print("6. 🚪 退出")
        
        choice = input("\n请输入选项 (1-6): ").strip()
        
        if choice == '1':
            quick_generate()
        elif choice == '2':
            quick_explain()
        elif choice == '3':
            quick_debug()
        elif choice == '4':
            quick_optimize()
        elif choice == '5':
            interactive_mode()
        elif choice == '6':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选项，请重新选择")

if __name__ == "__main__":
    main()
