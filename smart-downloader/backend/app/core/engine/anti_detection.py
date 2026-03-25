"""
反检测脚本模块
模拟真实浏览器特征，绕过 bot 检测
"""


ANTI_DETECTION_SCRIPT = """
// 反检测脚本 - 隐藏自动化特征

(function() {
    'use strict';
    
    // 1. 移除 webdriver 标识
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
        configurable: true
    });
    
    // 2. 隐藏 plugins 数组异常
    Object.defineProperty(navigator, 'plugins', {
        get: () => {
            const plugins = [
                {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgffccbbpenlnmmjdbfjfo'},
                {name: 'Native Client', filename: 'internal-nacl-plugin'}
            ];
            return plugins;
        },
        configurable: true
    });
    
    // 3. 设置正常的 languages
    Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en-US', 'en'],
        configurable: true
    });
    
    // 4. 模拟真实的 screen 属性
    Object.defineProperty(screen, 'avaiWidth', {
        get: () => window.screen.availWidth - random(0, 100),
        configurable: true
    });
    
    // 5. 隐藏 cdp 特征
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );
    
    // 6. 模拟 WebGL 指纹
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(index) {
        if (index === 37445) {
            return 'Intel Inc.';
        }
        if (index === 37446) {
            return 'Intel Iris OpenGL Engine';
        }
        return getParameter.call(this, index);
    };
    
    // 7. 模拟真实的 connection 属性
    Object.defineProperty(navigator, 'connection', {
        get: () => ({
            effectiveType: '4g',
            rtt: 50,
            downlink: 10,
            saveData: false
        }),
        configurable: true
    });
    
    // 8. 模拟 touch 支持
    Object.defineProperty(navigator, 'touchEnabled', {
        get: () => false,
        configurable: true
    });
    
    // 9. 模拟 hardwareConcurrency
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8,
        configurable: true
    });
    
    // 10. 模拟 deviceMemory
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8,
        configurable: true
    });
    
    console.log('Anti-detection scripts loaded');
})();
"""


def get_anti_detection_script() -> str:
    """获取反检测脚本"""
    return ANTI_DETECTION_SCRIPT


async def inject_anti_detection(page):
    """向页面注入反检测脚本"""
    await page.add_init_script(ANTI_DETECTION_SCRIPT)
