#!/usr/bin/env python3
"""
智下载 - 登录自动化测试
使用 Playwright 进行浏览器自动化测试
"""
from playwright.sync_api import sync_playwright
import time
import json

def test_login():
    """登录功能测试"""
    print("=" * 50)
    print("智下载 - 登录自动化测试")
    print("=" * 50)
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            # 1. 访问登录页面
            print("\n1. 访问登录页面...")
            page.goto("http://localhost:8001/login", wait_until='networkidle')
            print(f"   ✅ 页面标题：{page.title()}")
            print(f"   ✅ 当前 URL: {page.url}")
            
            # 等待页面加载
            time.sleep(2)
            
            # 2. 检查登录表单元素
            print("\n2. 检查登录表单元素...")
            
            # 检查组织 ID 输入框
            org_input = page.locator('input[type="number"]').first
            if org_input.is_visible():
                print("   ✅ 组织 ID 输入框：存在")
            else:
                print("   ❌ 组织 ID 输入框：不存在")
            
            # 检查用户名输入框
            username_input = page.locator('input[placeholder*="用户名"]').first
            if username_input.is_visible():
                print("   ✅ 用户名输入框：存在")
            else:
                print("   ❌ 用户名输入框：不存在")
            
            # 检查密码输入框
            password_input = page.locator('input[type="password"]').first
            if password_input.is_visible():
                print("   ✅ 密码输入框：存在")
            else:
                print("   ❌ 密码输入框：不存在")
            
            # 检查登录按钮
            login_button = page.locator('button[type="submit"]').first
            if login_button.is_visible():
                print("   ✅ 登录按钮：存在")
            else:
                print("   ❌ 登录按钮：不存在")
            
            # 3. 填写登录表单
            print("\n3. 填写登录表单...")
            
            # 填写组织 ID
            org_input.fill("1")
            print("   ✅ 组织 ID: 1")
            
            # 填写用户名
            username_input.fill("admin")
            print("   ✅ 用户名：admin")
            
            # 填写密码
            password_input.fill("admin123")
            print("   ✅ 密码：admin123")
            
            # 4. 点击登录按钮
            print("\n4. 点击登录按钮...")
            login_button.click()
            
            # 等待响应
            print("   等待登录响应...")
            time.sleep(3)
            
            # 5. 检查登录结果
            print("\n5. 检查登录结果...")
            current_url = page.url
            print(f"   当前 URL: {current_url}")
            
            if '/dashboard' in current_url or current_url.endswith('/'):
                print("   ✅ 登录成功！已跳转到仪表盘")
                
                # 截图保存
                page.screenshot(path='tests/screenshots/login_success.png')
                print("   ✅ 截图已保存：tests/screenshots/login_success.png")
            else:
                print("   ⚠️ 登录可能失败，仍在登录页面")
                # 检查是否有错误消息
                error_msg = page.locator('.ant-message-error').first
                if error_msg.is_visible():
                    error_text = error_msg.inner_text()
                    print(f"   ❌ 错误消息：{error_text}")
            
            # 6. 检查仪表盘元素
            print("\n6. 检查仪表盘元素...")
            
            # 检查导航菜单
            sidebar = page.locator('.ant-layout-sider')
            if sidebar.is_visible():
                print("   ✅ 左侧导航栏：存在")
                
                # 获取菜单项
                menu_items = sidebar.locator('.ant-menu-item')
                count = menu_items.count()
                print(f"   ✅ 菜单项数量：{count}")
                
                for i in range(count):
                    item = menu_items.nth(i)
                    if item.is_visible():
                        text = item.inner_text()
                        print(f"      - 菜单 {i+1}: {text}")
            
            # 检查顶部用户菜单
            user_menu = page.locator('.ant-layout-header')
            if user_menu.is_visible():
                print("   ✅ 顶部导航栏：存在")
            
            # 截图保存
            page.screenshot(path='tests/screenshots/dashboard.png', full_page=True)
            print("   ✅ 仪表盘截图已保存")
            
            print("\n" + "=" * 50)
            print("✅ 登录自动化测试完成!")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ 测试失败：{e}")
            
            # 截图保存错误
            page.screenshot(path='tests/screenshots/login_error.png')
            print("   ✅ 错误截图已保存")
            
        finally:
            # 关闭浏览器
            time.sleep(2)
            browser.close()
            print("\n浏览器已关闭")

if __name__ == "__main__":
    import os
    os.makedirs("tests/screenshots", exist_ok=True)
    test_login()
