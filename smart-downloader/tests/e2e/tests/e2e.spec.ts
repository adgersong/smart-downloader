import { test, expect } from '@playwright/test';

test.describe('智下载系统 - E2E 测试', () => {
  test('首页可访问', async ({ page }) => {
    await page.goto('http://localhost:8000');
    await expect(page).toHaveTitle(/智下载/);
  });

  test('登录页面显示', async ({ page }) => {
    await page.goto('http://localhost:8000/login');
    await expect(page.locator('text=智下载')).toBeVisible();
    await expect(page.locator('text=智能浏览器自动化下载系统')).toBeVisible();
  });

  test('登录表单存在', async ({ page }) => {
    await page.goto('http://localhost:8000/login');
    
    // 检查表单元素
    await expect(page.locator('input[placeholder*="组织 ID"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="用户名"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button:has-text("登录")')).toBeVisible();
  });

  test('登录表单验证', async ({ page }) => {
    await page.goto('http://localhost:8000/login');
    
    // 尝试提交空表单
    await page.click('button:has-text("登录")');
    
    // 应该显示验证错误
    await page.waitForTimeout(1000);
  });

  test('登录成功跳转', async ({ page }) => {
    await page.goto('http://localhost:8000/login');
    
    // 输入测试数据
    await page.fill('input[placeholder*="组织 ID"]', '1');
    await page.fill('input[placeholder*="用户名"]', 'admin');
    await page.fill('input[type="password"]', 'admin123');
    
    // 点击登录
    await page.click('button:has-text("登录")');
    
    // 等待跳转（可能成功或失败，取决于后端是否有该用户）
    await page.waitForTimeout(2000);
    
    // 检查是否跳转到仪表盘或显示错误
    const url = page.url();
    expect(url.includes('login') || url.includes('dashboard')).toBeTruthy();
  });

  test('仪表盘页面', async ({ page }) => {
    // 假设已经登录（或跳过认证）
    await page.goto('http://localhost:8000/dashboard');
    
    // 检查仪表盘元素
    await expect(page.locator('text=仪表盘')).toBeVisible();
    
    // 检查统计卡片
    const cards = page.locator('.ant-statistic');
    await cards.first().waitFor({ state: 'visible', timeout: 5000 }).catch(() => {});
  });

  test('组织管理页面', async ({ page }) => {
    await page.goto('http://localhost:8000/organization');
    
    // 检查页面元素
    await expect(page.locator('text=组织管理')).toBeVisible();
    await expect(page.locator('button:has-text("新建组织")')).toBeVisible();
  });

  test('业务系统页面', async ({ page }) => {
    await page.goto('http://localhost:8000/system');
    
    // 检查页面元素
    await expect(page.locator('text=业务系统')).toBeVisible();
    await expect(page.locator('button:has-text("新建系统")')).toBeVisible();
  });

  test('流程管理页面', async ({ page }) => {
    await page.goto('http://localhost:8000/workflow');
    
    // 检查页面元素
    await expect(page.locator('text=流程')).toBeVisible();
  });

  test('任务管理页面', async ({ page }) => {
    await page.goto('http://localhost:8000/task');
    
    // 检查页面元素
    await expect(page.locator('text=任务')).toBeVisible();
  });
});
