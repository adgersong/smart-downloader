"""
Playwright 浏览器引擎模块
提供浏览器自动化核心功能
"""
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Optional, Dict, Any
import asyncio
import random


class BrowserEngine:
    """浏览器引擎类"""
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def start(self, headless: bool = False):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        
        # 启动浏览器 (Chromium)
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # 创建浏览器上下文
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        # 创建页面
        self.page = await self.context.new_page()
        
        # 注入反检测脚本
        await self._inject_anti_detection()
    
    async def _inject_anti_detection(self):
        """注入反检测脚本"""
        await self.page.add_init_script('''
            // 移除 webdriver 标识
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // 隐藏自动化特征
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });
        ''')
    
    async def goto(self, url: str, wait_until: str = 'networkidle'):
        """导航到 URL"""
        await self.page.goto(url, wait_until=wait_until)
    
    async def click(self, selector: str):
        """点击元素"""
        await self.page.click(selector)
    
    async def fill(self, selector: str, text: str):
        """填充输入框"""
        await self.page.fill(selector, text)
    
    async def download(self, url: str, filename: str):
        """下载文件并保存为指定 filename"""
        # 通过页面导航触发下载并捕获 download 对象
        async with self.page.expect_download() as download_info:
            await self.page.goto(url)
        download = await download_info.value
        await download.save_as(filename)

    
    async def screenshot(self, path: str):
        """截图"""
        await self.page.screenshot(path=path, full_page=True)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


class HumanSimulator:
    """人类行为模拟器"""
    
    @staticmethod
    async def human_mouse_move(page: Page, selector: str):
        """拟人化鼠标移动"""
        element = await page.query_selector(selector)
        if not element:
            return
        
        box = await element.bounding_box()
        if not box:
            return
        
        # 计算目标位置 (添加随机偏移)
        target_x = box['x'] + box['width'] / 2 + random.uniform(-5, 5)
        target_y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
        
        # 获取当前位置
        mouse_x = random.randint(100, 200)
        mouse_y = random.randint(100, 200)
        
        # 贝塞尔曲线路径
        steps = random.randint(5, 10)
        for i in range(steps):
            t = i / steps
            # 添加随机偏移
            current_x = mouse_x + (target_x - mouse_x) * t + random.uniform(-10, 10)
            current_y = mouse_y + (target_y - mouse_y) * t + random.uniform(-10, 10)
            
            await page.mouse.move(current_x, current_y)
            
            # 随机延迟
            await asyncio.sleep(random.uniform(0.02, 0.08))
    
    @staticmethod
    async def human_type(page: Page, selector: str, text: str):
        """拟人化键盘输入"""
        await page.click(selector)
        
        # 随机延迟
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # 逐字符输入 (模拟人类打字)
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.2))
        
        # 偶尔的拼写错误和纠正 (5% 概率)
        if random.random() < 0.05:
            # 删除最后一个字符
            await page.keyboard.press('Backspace')
            await asyncio.sleep(random.uniform(0.1, 0.2))
            # 重新输入
            await page.keyboard.type(char)
    
    @staticmethod
    async def human_wait():
        """模拟人类思考时间"""
        await asyncio.sleep(random.uniform(0.5, 2.0))
    
    @staticmethod
    async def human_scroll(page: Page, direction: str = 'down'):
        """模拟人类滚动页面"""
        scroll_amount = random.randint(100, 500)
        
        if direction == 'down':
            await page.evaluate(f'window.scrollBy(0, {scroll_amount})')
        else:
            await page.evaluate(f'window.scrollBy(0, -{scroll_amount})')
        
        await asyncio.sleep(random.uniform(0.3, 1.0))
