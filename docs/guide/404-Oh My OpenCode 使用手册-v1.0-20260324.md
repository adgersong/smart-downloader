# Oh‑My‑OpenCode 使用手册 v1.0（2026‑03‑24）

## 1. 目标

为帮助团队在 **OpenCode** 项目中统一使用 **Oh‑My‑OpenCode（omx）**，实现规划 → PRD → 代码生成 → 验证 → 修复的闭环工作流。

## 2. 适用范围

- 本项目（`/Users/songyanjie/opentest/00Bank_down`）下所有 **代码、文档、测试** 的开发与维护。
- 适用于功能需求、技术实现、测试用例、代码评审、自动化发布等场景。

## 3. 前置条件

| 条件 | 检查方式 | 备注 |
|------|----------|------|
| Node ≥ 18 | `node -v` | 推荐使用 LTS 版 |
| npm 可用 | `npm -v` | 自动安装全局包 |
| OpenAI API Key | 环境变量 `OPENAI_API_KEY` | 必须有效 |
| Git 访问权限 | `git remote -v` | 需要 `push` 权限 |

## 4. 安装与初始化

### 4.1 安装全局依赖

```bash
# Playwright（用于 E2E）
npm i -D @playwright/test && npx playwright install firefox

# Codex CLI（提供 $ 命令）
npm i -g @openai/codex

# Oh‑My‑OpenCode（omx）
npm i -g oh-my-codex
```

### 4.2 初始化 omx 配置（一次性）

```bash
# 在项目根目录执行，--force 覆盖旧配置
omx setup --force
```

此命令会在用户主目录创建以下结构（仅展示重要目录）：
- `~/.omc/PROMPTS/` – 默认 Prompt 库
- `~/.omc/SKILLS/` – 预置 Codex Skills
- `~/.omc/AGENTS.md` – Agent 列表说明
- `~/.omc/state/config.toml` – MCP 配置文件
- `~/.omc/hud/` – 可选 HUD 前端资源

### 4.3 验证环境（每次使用前）

```bash
omx doctor
```

**全部 10 项检查通过** 代表可直接使用 omx 进行后续操作。

## 5. 常用 omx / Codex REPL 命令

| 命令 | 作用 |
|------|------|
| `$plan "<目标>"` | 生成任务列表、依赖关系、验收标准 |
| `$prd "<目标>"` | 将计划转换为完整的 PRD（章节化） |
| `$code "<目标>"` | 自动执行计划，写代码、跑测试、创建分支并提交 |
| `$autopilot "<目标>"` | **一键全链路**：plan → PRD → code → 验证 → PR（生成 GitHub PR） |
| `$tdd "<目标>"` | 进入 TDD 流程：先写失败测试，再实现功能 |
| `$code‑review` | 触发 **code‑review** Skill，对当前分支进行代码审查并生成评论 |
| `$security‑review` | 触发 **security‑review** Skill，执行静态安全扫描 |
| `$memory save "<key>"` | 将文本/JSON 保存到 Agent 长期记忆 |
| `$memory recall "<key>"` | 读取前一步保存的记忆内容 |
| `omx hud` | 启动实时 UI HUD，展示当前 workflow、Agent 状态、Memory 等信息 |
| `omx team start <team‑name>` | 按模板启动多 Agent 团队（Planner、Reviewer、Tester 等） |

> 所有 `$` 前缀命令均在 **Codex REPL** 中执行：`codex` → 进入交互式提示符。

## 6. 示例工作流：实现「文件上传」功能

```bash
# 1. 进入 Codex REPL（全局已安装）
codex

# 2. 一键自动化（推荐）
$autopilot "实现文件上传功能（前端 + 后端 + 测试）"
```

系统会自动完成：
1. 生成 **Plan**（任务列表）
2. 生成 **PRD**（需求文档）
3. 在 `smart-downloader` 项目中创建 `feature/file-upload` 分支，编写代码、单元/集成/E2E 测试
4. 运行全部测试，若通过则 **push** 并在 GitHub 创建 PR，PR 中附带代码审查与安全审查报告。

## 7. 文档编写与评审规范（对应《文档管理规范》）

- **文档类型**：本手册属于 **用户指南类**，序号使用 400‑499 范围。已使用 **404**（前置已占用 401‑403）。
- **文件命名**：`404-Oh My OpenCode 使用手册-v1.0-20260324.md`（见本文件路径 `docs/guide/`）。
- **版本管理**：每次重大变更升主版本（如 `v2.0`），小幅更新升次版本（`v1.1`），并在文档末尾记录 **变更历史**（参照《文档管理规范》章节 8.2）。
- **评审流程**：提交 `doc/oh-my-opencode` 分支 → Pull Request → 通过 `$code-review` + 人工评审 → 合并 `main` 并打 Tag `docs-v1.0`。

## 8. 常见问题（FAQ）

1. **omx 找不到**：全局包名为 **`oh-my-codex`**，二进制为 **`omx`**。确保已 `npm i -g oh-my-codex` 并刷新 `PATH`。
2. **Codex REPL 报错**：检查 `OPENAI_API_KEY` 是否正确、网络是否通畅。
3. **$autopilot 卡住**：运行 `omx doctor` 确认全部子系统（Prompt、Skill、MCP）健康；如有错误，依据提示修复后重新执行。
4. **生成的 PR 没有自动审查**：在 REPL 中先执行 `$code-review` 与 `$security-review`，或在 Workflow 中添加 `omx doctor && $autopilot …` 步骤。

## 9. CI 集成示例（GitHub Actions）

在项目根目录新建 `.github/workflows/omx.yml`（请参考《文档管理规范》中的模板），核心步骤如下：
```yaml
name: omx CI
on:
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize ]

jobs:
  omx-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install deps
        run: |
          npm ci
          pip install -r requirements.txt || true
      - name: Install Codex & omx
        run: |
          npm i -g @openai/codex
          npm i -g oh-my-codex
      - name: Initialise omx
        run: omx setup --force
      - name: Run doctor
        run: omx doctor
      - name: Autopilot 示例
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          codex
          $autopilot "实现文件上传功能（前端 + 后端 + 测试）"
```

> 该 workflow 将在每次推送或 PR 时自动执行 **omx**，完成代码生成、测试、审查并提交 PR。

## 10. 变更历史

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-03-24 | 初始手册创建 | 自动生成 |

---

**备注**：本手册严格遵循 `/Users/songyanjie/opentest/00Bank_down/docs/文档管理规范-v1.0-20240115.md` 中的命名、版本、目录、评审及保密要求。后续如需更新，请在文档末尾追加 **变更历史** 并依据规范提交 PR。