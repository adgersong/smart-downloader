# Node.js 环境配置指南

## 当前状态

- **当前 Node 版本**: v24.13.0
- **推荐 Node 版本**: v20.x LTS
- **问题**: Umi 4.x 与 Node v24 存在兼容性冲突

---

## 解决方案

### 方法一：使用 NVM（推荐）

#### 1. 安装 NVM

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

#### 2. 加载 NVM

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

#### 3. 安装 Node 20

```bash
nvm install 20
```

#### 4. 使用 Node 20

```bash
nvm use 20
```

#### 5. 验证

```bash
node --version
# 应显示 v20.x.x
```

---

### 方法二：使用 Homebrew

```bash
# 安装 Node 20
brew install node@20

# 链接到 PATH
brew link node@20

# 验证
node --version
```

---

### 方法三：直接下载

访问 https://nodejs.org/zh-cn/ 下载 v20 LTS 版本安装包。

---

## 安装后配置

### 1. 清理前端缓存

```bash
cd smart-downloader/frontend
rm -rf node_modules package-lock.json src/.umi
```

### 2. 重新安装依赖

```bash
npm install
```

### 3. 启动前端

```bash
npm run dev
```

---

## 常见问题

### Q: NVM 安装后找不到命令

```bash
# 重新加载配置
source ~/.bashrc  # 或 ~/.zshrc
```

### Q: 权限错误

```bash
# macOS 使用 sudo
sudo brew install node@20
```

### Q: 版本切换

```bash
# 查看已安装版本
nvm ls

# 切换到特定版本
nvm use 20

# 设置默认版本
nvm alias default 20
```

---

## 验证步骤

1. **检查 Node 版本**
   ```bash
   node --version
   # 应显示 v20.x.x
   ```

2. **检查 npm 版本**
   ```bash
   npm --version
   # 应显示 10.x
   ```

3. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

4. **启动开发服务器**
   ```bash
   npm run dev
   ```

5. **访问前端**
   ```
   http://localhost:8001
   ```

---

## 快速命令参考

```bash
# 安装 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 加载 NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 安装并使用 Node 20
nvm install 20
nvm use 20

# 验证
node --version

# 前端配置
cd frontend
rm -rf node_modules package-lock.json src/.umi
npm install
npm run dev
```

---

**更新日期**: 2026-03-24
**适用系统**: macOS / Linux
