# OpenCode 全局开发规范、规则、要求

**目标**：一次性定义组织层面的开发约束，让 **所有后续项目** 在创建/克隆时自动获得并强制执行这些规范，而不需要每个项目单独手动配置。

---

## 1️⃣ 选定全局配置入口
| 方案 | 说明 | 推荐场景 |
|------|------|----------|
| **`/opt/opencode/global-config/`**（服务器目录） | 统一放置 YAML/JSON 配置、脚本、Git hooks、CI 模板等。所有机器挂载该路径（NFS、EFS、Samba）即可读取。| 企业内部私有服务器、CI/CD 统一节点 |
| **Git‑Hub（或 GitLab）组织/仓库 `opencode‑policy`** | 将所有规范存入单一仓库，使用子模块或 **Git‑worktree** 将其引用到每个项目。| 多仓库、分布式团队，想利用 Git 版本管理 |
| **`~/.opencode/config.yml`**（本地用户目录） | 轻量方案，适合个人或小团队，配合 `opencode init` 自动复制模板。| 开发者个人机器，快速上手 |

> **推荐**：在组织层面创建 **`opencode-policy`** 仓库，配合 **Git 子模块** 与 **Pre‑commit** / **CI** 自动检查，最易维护且版本可追溯。

---

## 2️⃣ 组织 `opencode-policy` 仓库结构
```
opencode-policy/
├─ .github/                # 统一 CI/CD 工作流模板（GitHub Actions）
│   └─ workflows/
│      └─ lint.yml
├─ .pre-commit-config.yaml # 统一 lint / format / security hooks
├─ conductor/               # OpenCode 专用上下文文件
│   ├─ product.md           # 项目目标、受众、价值主张（可共用）
│   ├─ tech-stack.md        # 统一技术栈（Node ≥20, Python ≥3.11, Docker 27, ...）
│   ├─ workflow.md          # 开发流程（branch‑strategy, PR‑policy, release‑flow）
│   └─ tracks.md            # 常用 Track 模板（feat, fix, docs, refactor…）
├─ standards/               # 代码/文档/安全/性能规范
│   ├─ eslint-config.json
│   ├─ prettier-config.json
│   ├─ stylelint-config.json
│   ├─ security-baselines.yml
│   └─ performance-guidelines.md
└─ scripts/
   ├─ enforce.sh            # 本地检查脚本（可在 CI 中调用）
   └─ init-project.sh       # 项目初始化脚本（创建目录结构、拷贝模板）
```

**关键文件说明**
| 文件 | 作用 | 示例 |
|------|------|------|
| `.pre-commit-config.yaml` | 所有项目统一的 **pre‑commit** 钩子。包括代码格式化、ESLint、依赖安全检查、license‑header 检查等。 | `- repo: https://github.com/pre-commit/mirrors-eslint` |
| `conductor/workflow.md` | OpenCode 的 **全局工作流**（branch‑strategy: `main` + `feature/*`、PR‑require‑review、CI‑pass、changelog‑gen）。| 同 `workflow.md` 参考 OpenCode 官方文档 |
| `scripts/enforce.sh` | 运行时检查项目是否已引用 `opencode-policy`（子模块或 worktree），若没有则 **自动添加** 并 **提示**。| `git submodule add https://github.com/your-org/opencode-policy.git .opencode` |
| `scripts/init-project.sh` | 项目创建脚本：`git clone <repo>` → `./scripts/init-project.sh` → 自动复制 `.pre-commit-config.yaml`、`conductor/`、`.github/workflows/` 等。| `./init-project.sh` |

---

## 3️⃣ 将规范强制作用于每个项目
### 3.1 采用 Git 子模块（推荐）
```bash
# 1️⃣ 在新项目根目录加入子模块（一次性完成）
git submodule add https://github.com/your-org/opencode-policy.git .opencode
git submodule update --init --recursive

# 2️⃣ 把子模块文件链接到项目根（软链接或 copy）
ln -s .opencode/conductor/* .
ln -s .opencode/.pre-commit-config.yaml .
ln -s .opencode/.github/workflows .github/workflows

# 3️⃣ 安装 pre‑commit 钩子（一次性）
pre-commit install
```
> **好处**：子模块指向同一仓库的特定 commit，所有项目同步更新只需在 `opencode-policy` 中提交一次。

### 3.2 CI/CD 自动校验（GitHub Actions 示例）
`.github/workflows/lint.yml`
```yaml
name: Lint & Policy Check
on:
  push:
    branches: [main, feature/*]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true      # 拉取子模块
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install deps
        run: npm ci
      - name: Run pre‑commit hooks
        run: npx pre-commit run --all-files
      - name: Enforce policy scripts
        run: ./.opencode/scripts/enforce.sh
```
> 只要 PR 触发该 workflow，未遵守的项目会 **直接失败**，阻止合并。

### 3.3 本地初始化脚本（一次性执行）
```bash
#!/usr/bin/env bash
set -e

# ① 拉取最新规范
git submodule update --remote .opencode

# ② 软链接或复制必备文件
ln -sf .opencode/.pre-commit-config.yaml .
ln -sf .opencode/conductor/* .
ln -sf .opencode/.github/workflows/* .github/workflows/

# ③ 安装 pre‑commit（若尚未）
if ! command -v pre-commit &>/dev/null; then
  npm i -g pre-commit
fi
pre-commit install

echo "✅ 项目已完成 OpenCode 规范化初始化"
```
将此脚本放在 `opencode-policy/scripts/init-project.sh`，每个新仓库在 `git clone` 后直接执行即可。

---

## 4️⃣ 用 OpenCode **Context‑Driven Development** 把全局规范注入运行时
OpenCode 支持在 **`conductor/`** 目录下的 `workflow.md`/`tech-stack.md` 自动为所有后续 `opencode` 命令提供上下文。只要子模块被拉取，这些文件会自动生效。

**示例 `conductor/workflow.md`（全局）**
```markdown
# OpenCode 全局工作流

- **分支策略**: `main` 为生产分支，功能分支 `feat/<ticket>-<short>`.
- **PR 规则**: 必须通过 `pre-commit`、CI、并且每次提交必须关联 JIRA ticket。
- **发布流程**: 自动生成 CHANGELOG（keepachangelog），语义化版本号 (`npm version`).
- **代码审查**: 所有代码必须通过 `senior‑code‑review`（自动化 + 手动）。
```
只要项目根目录中存在 `conductor/`（即子模块），OpenCode CLI 在执行 `opencode run`、`opencode test` 等命令时会自动读取这些规则，无需每次手动传参。

---

## 5️⃣ 统一安全 / 合规检查（可选）
| 检查 | 工具 | 对应文件 |
|------|------|----------|
| 依赖安全 (OWASP‑Dependency‑Check) | `dependency-check` CLI | `standards/security-baselines.yml` |
| Secret 检测 | `git‑secret` / `trufflehog` | `scripts/enforce.sh` 中调用 |
| 代码质量 (ESLint/Flake8/Ruff) | 对应语言 linter | `standards/*-config.*` |
| License / Header 规范 | `reuse` / `license‑header` | `standards/license-header.txt` |

在 `enforce.sh` 中统一调用：
```bash
#!/usr/bin/env bash
set -e

# 1️⃣ 检查子模块是否存在
if [ ! -d ".opencode" ]; then
  echo "❌ 缺少 .opencode 子模块，请先执行: git submodule add …"
  exit 1
fi

# 2️⃣ 运行安全基线检查
dependency-check --project "$(basename $(pwd))" --scan . --format HTML --out dc-report.html
if grep -q "VULNERABILITY" dc-report.html; then
  echo "⚠️ 发现安全漏洞，请修复后再提交"
  exit 1
fi

# 3️⃣ 运行 secret 检测
trufflehog git . --since-commit HEAD~1
```
---

## 6️⃣ 推广与落地步骤（一步一步执行）
1. **创建 `opencode-policy` 仓库**（组织管理员）
2. **把已有项目迁入子模块**
   ```bash
   cd <project>
   git submodule add https://github.com/your-org/opencode-policy.git .opencode
   git commit -m "Add global OpenCode policy submodule"
   ```
3. **在每个项目根目录运行一次初始化脚本**
   ```bash
   .opencode/scripts/init-project.sh
   ```
4. **在 CI/CD 中启用 `lint.yml`**（多数平台只需把文件 push 到 `.github/workflows/`）。
5. **培训开发者**：在 onboarding 文档说明 `pre‑commit install` 与 `opencode init` 的必做步骤。
6. **定期更新**：在 `opencode-policy` 中提交新的规范后，所有项目只要执行 `git submodule update --remote .opencode` 即可同步。

---

## 7️⃣ 常见疑问 & 快速解决方案
| 场景 | 解决办法 |
|------|----------|
| **子模块忘记拉取** | 在 CI 中强制 `git submodule update --init --recursive`；本地可在 `pre-commit` 添加检查。 |
| **想在新仓库自动带上子模块** | 在组织的 **模板仓库**（GitHub Template）里已经绑定子模块，创建新仓库时直接使用模板。 |
| **不同语言项目共享同一 eslint 配置** | `opencode-policy/standards/eslint-config.json` 通过软链接或 `extends` 方式统一引用。 |
| **团队不想使用子模块** | 改为 **Git 包**（`git subtree`）或 **NPM/Yarn workspace**（将 `opencode-policy` 发布为私有 npm 包），同样在 `init-project.sh` 中自动 `npm i @org/opencode-policy` 并复制文件。 |

---

## 🎯 小结
1. **建立统一仓库 `opencode-policy`**，内部放置所有规范、脚本、CI模板、Conductor 上下文文件。 
2. **在每个项目通过 Git 子模块（或 npm 包）引用**，并使用 `init-project.sh` 自动软链接关键文件。 
3. **在 CI（GitHub Actions、GitLab CI）中强制执行** `pre‑commit` + `enforce.sh`，保证所有 PR 必须符合全局规则。 
4. **利用 OpenCode 的 `conductor/` 上下文**，让 OpenCode CLI 在任何命令执行时自动读取这些全局约定。 
5. **定期更新 `opencode-policy`**，子模块一次更新即可同步所有项目。

这样，无论是新建项目还是已有项目，只要执行一次初始化脚本，就能确保 **“所有 OpenCode 项目”** 都统一遵循组织制定的开发规范、规则、要求。祝实施顺利 🚀!
