import { test, expect } from '@playwright/test';

test.describe('智下载系统 - 完整功能测试', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8000');
  });

  test('首页加载', async ({ page }) => {
    await expect(page).toHaveTitle(/智下载/);
    await page.screenshot({ path: 'test-results/home.png' });
  });

  test('登录页面 - 完整测试', async ({ page }) => {
    await page.goto('http://localhost:8000/login');
    
    // 检查所有表单元素
    await expect(page.locator('input[placeholder*="组织 ID"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="用户名"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button:has-text("登录")')).toBeVisible();
    
    // 点击自动登录复选框
    const autoLoginCheckbox = page.locator('label:has-text("自动登录")');
    if (await autoLoginCheckbox.isVisible()) {
      await autoLoginCheckbox.click();
    }
    
    // 填写并提交表单
    await page.fill('input[placeholder*="组织 ID"]', '1');
    await page.fill('input[placeholder*="用户名"]', 'admin');
    await page.fill('input[type="password"]', 'admin123');
    
    // 截图
    await page.screenshot({ path: 'test-results/login-filled.png' });
    
    // 点击登录按钮
    await page.click('button:has-text("登录")');
    
    // 等待响应
    await page.waitForTimeout(3000);
    
    // 截图
    await page.screenshot({ path: 'test-results/login-submitted.png' });
  });

  test('仪表盘页面 - 所有卡片点击', async ({ page }) => {
    await page.goto('http://localhost:8000/dashboard');
    
    // 截图
    await page.screenshot({ path: 'test-results/dashboard.png' });
    
    // 点击所有统计卡片
    const cards = page.locator('.ant-statistic');
    const count = await cards.count();
    
    for (let i = 0; i < count; i++) {
      await cards.nth(i).click();
      await page.waitForTimeout(500);
    }
    
    // 检查最近任务卡片
    await expect(page.locator('text=最近任务')).toBeVisible();
    
    // 检查系统健康状态卡片
    await expect(page.locator('text=系统健康状态')).toBeVisible();
  });

  test('组织管理页面 - 完整流程', async ({ page }) => {
    await page.goto('http://localhost:8000/organization');
    
    // 截图
    await page.screenshot({ path: 'test-results/organization.png' });
    
    // 点击新建组织按钮
    const createButton = page.locator('button:has-text("新建组织")');
    if (await createButton.isVisible()) {
      await createButton.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/organization-create-modal.png' });
      
      // 填写表单
      await page.fill('input[placeholder*="组织名称"]', `测试组织_${Date.now()}`);
      
      // 点击确定
      await page.click('button:has-text("确定")');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-results/organization-submitted.png' });
    }
    
    // 点击搜索框
    const searchBox = page.locator('input[placeholder*="搜索"]');
    if (await searchBox.isVisible()) {
      await searchBox.click();
      await searchBox.fill('测试');
      await page.waitForTimeout(1000);
    }
    
    // 点击编辑按钮
    const editButtons = page.locator('button:has-text("编辑")');
    if (await editButtons.count() > 0) {
      await editButtons.first().click();
      await page.waitForTimeout(1000);
    }
  });

  test('业务系统页面 - 完整流程', async ({ page }) => {
    await page.goto('http://localhost:8000/system');
    
    // 截图
    await page.screenshot({ path: 'test-results/system.png' });
    
    // 点击新建系统按钮
    const createButton = page.locator('button:has-text("新建系统")');
    if (await createButton.isVisible()) {
      await createButton.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/system-create-modal.png' });
      
      // 填写表单
      await page.fill('input[placeholder*="系统名称"]', `测试系统_${Date.now()}`);
      await page.fill('input[placeholder*="https://"]', 'https://test.example.com');
      
      // 选择类型
      const typeSelect = page.locator('select');
      if (await typeSelect.isVisible()) {
        await typeSelect.selectOption('custom');
      }
      
      // 点击确定
      await page.click('button:has-text("确定")');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-results/system-submitted.png' });
    }
    
    // 点击搜索框
    const searchBox = page.locator('input[placeholder*="搜索"]');
    if (await searchBox.isVisible()) {
      await searchBox.click();
      await searchBox.fill('测试');
      await page.waitForTimeout(1000);
    }
  });

  test('流程管理页面 - 所有功能', async ({ page }) => {
    await page.goto('http://localhost:8000/workflow');
    
    // 截图
    await page.screenshot({ path: 'test-results/workflow.png' });
    
    // 点击创建流程按钮
    const createButton = page.locator('button:has-text("创建")');
    if (await createButton.isVisible()) {
      await createButton.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/workflow-create.png' });
    }
    
    // 检查流程画布
    const canvas = page.locator('.react-flow');
    if (await canvas.isVisible()) {
      await canvas.click();
      await page.waitForTimeout(500);
    }
  });

  test('任务管理页面 - 所有功能', async ({ page }) => {
    await page.goto('http://localhost:8000/task');
    
    // 截图
    await page.screenshot({ path: 'test-results/task.png' });
    
    // 点击执行按钮
    const executeButtons = page.locator('button:has-text("执行")');
    if (await executeButtons.count() > 0) {
      await executeButtons.first().click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-results/task-executing.png' });
    }
    
    // 点击刷新按钮
    const refreshButton = page.locator('button[aria-label="刷新"]');
    if (await refreshButton.isVisible()) {
      await refreshButton.click();
      await page.waitForTimeout(1000);
    }
  });

  test('文件管理页面 - 所有功能', async ({ page }) => {
    await page.goto('http://localhost:8000/file');
    
    // 截图
    await page.screenshot({ path: 'test-results/file.png' });
    
    // 点击下载按钮
    const downloadButtons = page.locator('button:has-text("下载")');
    if (await downloadButtons.count() > 0) {
      await downloadButtons.first().click();
      await page.waitForTimeout(1000);
    }
    
    // 点击预览按钮
    const previewButtons = page.locator('button:has-text("预览")');
    if (await previewButtons.count() > 0) {
      await previewButtons.first().click();
      await page.waitForTimeout(1000);
    }
    
    // 点击搜索框
    const searchBox = page.locator('input[placeholder*="搜索"]');
    if (await searchBox.isVisible()) {
      await searchBox.click();
      await searchBox.fill('测试');
      await page.waitForTimeout(1000);
    }
  });

  test('导航栏 - 所有菜单项点击', async ({ page }) => {
    const menus = [
      { name: '仪表盘', url: '/dashboard' },
      { name: '组织管理', url: '/organization' },
      { name: '业务系统', url: '/system' },
      { name: '流程管理', url: '/workflow' },
      { name: '任务管理', url: '/task' },
      { name: '文件管理', url: '/file' },
    ];
    
    for (const menu of menus) {
      await page.goto(`http://localhost:8000${menu.url}`);
      await page.waitForTimeout(500);
      await page.screenshot({ path: `test-results/nav-${menu.name}.png` });
    }
  });

  test('完整流程 - 登录到所有页面', async ({ page }) => {
    // 1. 登录
    await page.goto('http://localhost:8000/login');
    await page.fill('input[placeholder*="组织 ID"]', '1');
    await page.fill('input[placeholder*="用户名"]', 'admin');
    await page.fill('input[type="password"]', 'admin123');
    await page.click('button:has-text("登录")');
    await page.waitForTimeout(3000);
    
    // 2. 访问所有页面
    const pages = [
      '/dashboard',
      '/organization',
      '/system',
      '/workflow',
      '/task',
      '/file',
    ];
    
    for (const p of pages) {
      await page.goto(`http://localhost:8000${p}`);
      await page.waitForTimeout(1000);
      
      // 点击页面上的所有按钮
      const buttons = page.locator('button');
      const count = await buttons.count();
      
      for (let i = 0; i < Math.min(count, 5); i++) {
        try {
          await buttons.nth(i).click();
          await page.waitForTimeout(500);
        } catch (e) {
          // 忽略无法点击的按钮
        }
      }
    }
    
    await page.screenshot({ path: 'test-results/full-flow-complete.png' });
  });
});
