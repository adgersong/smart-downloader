# 405-Oh My OpenCode 工作流完整指南 - v1.0 - 20260324

## 📘 目标
帮助团队在 OpenCode 项目中统一使用 Oh‑My‑OpenCode（omx），实现从需求捕获到代码交付的全链路闭环。

## 1️⃣ 前置准备
| 项目 | 检查方式 | 必须满足的条件 |
|------|----------|----------------|
| Node ≥ 18 | node -v | 推荐 LTS（如 20.x） |
| npm | npm -v | 用于全局包安装 |
| OpenAI API Key | echo $OPENAI_API_KEY | 必须有效 |
| GitHub Token（可选） | echo $GITHUB_TOKEN | 需要 repo 权限 |
| Git 远程可写 | git remote -v | 能 push 到仓库 |
| Playwright（Firefox） | npx playwright --version | 已安装 firefox |
| Codex CLI | codex -v | 已全局安装 @openai/codex |
| Oh‑My‑OpenCode | omx -V | 已全局安装 oh‑my‑codex |
| 健康检查 | omx doctor | 全部 10 项检查通过 |

> 在确认 `omx doctor` 全部通过后，运行 `codex` 进入 REPL，出现 `>` 提示符后即可输入 `$` 前缀命令。

## 2️⃣ 创建需求工作区
1. 创建需求分支：`git checkout -b doc/bank-download-feature`
2. 新建计划目录：`mkdir -p docs/ways-of-work/plan/bank-automation-download`
3. （可选）写需求概要 `000-需求概述.md`（遵循文档规范）。

## 3️⃣ 生成 Plan（任务拆解）
在 REPL 中执行：
```
$plan "实现银行自动化下载功能，支持批量下载、进度展示和安全校验"
```
系统会在 `docs/ways-of-work/plan/bank-automation-download/001-Plan 银行自动化下载功能‑v1.0‑20260324.md` 生成 Plan，包括里程碑、任务清单、依赖关系、验收标准。

## 4️⃣ 生成 PRD（需求规格）
仍在 REPL 中执行：
```
$prd "/Users/songyanjie/opentest/00Bank_down/docs/ways-of-work/plan/bank-automation-download"
```
系统在同目录下生成 PRD：`002-PRD 银行自动化下载功能‑v1.0‑20260324.md`，结构包括业务背景、功能概述、详细需求、接口定义、非功能要求、验收标准、变更历史。

## 5️⃣ 代码实现
### 5.1 手动方式（可控）
```
$code "实现银行自动化下载功能，支持批量下载、进度展示和安全校验"
```
- 自动生成前端（React）、后端（FastAPI/Node）代码、测试用例。
- 创建分支 `feature/bank-download-v1.0`，提交 `feat: impl bank download`。
- 运行全部测试并生成报告至 `reports/`。
- 如需手动推送：`git push -u origin feature/bank-download-v1.0`。

### 5.2 一键全链路（推荐）
```
$autopilot "实现银行自动化下载功能，支持批量下载、进度展示和安全校验"
```
Omx 将依次完成：Plan → PRD → 代码生成 → 测试运行 → 自动在 GitHub 创建 Pull Request（标题 `feat: bank‑download‑v1.0`，描述包括 Plan、PRD、测试报告）。

## 6️⃣ 测试与验证
- 若使用 TDD：`$tdd "实现银行自动化下载功能"` 会先生成失败测试，再迭代实现直至通过。
- E2E 测试：在项目根目录执行 `npm run test:e2e`（Playwright），产生 `smart-downloader/reports/e2e_report_YYYYMMDD_HHMMSS.json` 与 `.txt`。
- 运行 `omx doctor` 检查测试覆盖率，低于 80% 会提示。
- 可使用 `$memory save "test‑report"` 将报告路径保存至记忆，便于后续引用。

## 7️⃣ 代码审查 & 安全审查
在 REPL 中分别执行：
```
$code-review
$security-review
```
- 生成 Markdown 审查报告，自动在当前 Pull Request 中添加 Review Comment，并在本地 `reviews/` 目录生成 `003-Code Review …md` 与 `004-Security Review …md`（遵循文档规范的命名规则）。
- 提交审查报告：`git add . && git commit -m "docs: add code‑review & security‑review"`。

## 8️⃣ 可视化监控（HUD）
运行 `omx hud`，在浏览器打开实时 Dashboard（默认 http://localhost:3000），展示当前 workflow、Agent 状态、Memory 内容与 Trace 日志。可在 HUD 中点击 Pause/Resume 手动控制 AI 生成。

## 9️⃣ PR 合并与发布
1. 自动生成的 PR 已在第 5 步完成（若未自动，可手动 `git push` 后 `gh pr create`）。
2. 团队 Review（代码审查、安全审查）后合并至 `main`。
3. 打标签：`git tag docs-v1.0-20260324 && git push origin docs-v1.0-20260324` 用于文档版本追踪。
4. 如需对外发布，可将 `docs/` 目录同步至 Confluence、GitHub Pages 等文档站点。

## 🔟 常用快捷命令表
| 场景 | 命令 | 示例 |
|------|------|------|
| 生成计划 | $plan "<目标>" | $plan "实现银行自动化下载功能" |
| 生成 PRD | $prd "<plan 目录>" | $prd "/Users/.../bank-automation-download" |
| 全链路自动化 | $autopilot "<目标>" | $autopilot "实现银行自动化下载功能..." |
| TDD 流程 | $tdd "<目标>" | $tdd "实现银行自动化下载功能" |
| 代码审查 | $code-review | $code-review |
| 安全审查 | $security-review | $security-review |
| 保存记忆 | $memory save "<key>" | $memory save "plan‑path" |
| 读取记忆 | $memory recall "<key>" | $memory recall "plan‑path" |
| 打开 HUD | omx hud | omx hud |
| 启动团队 | omx team start <team‑name> | omx team start dev‑team |
| 健康检查 | omx doctor | omx doctor |
| 查看帮助 | omx help <command> | omx help setup |

---

### 📌 小结
- 所有文档、代码、报告均遵循 **文档管理规范 v1.0**（序号‑中文名‑vX.Y‑YYYYMMDD.md）。
- 使用 `$` 前缀命令在 Codex REPL 中即可触发每一步工作流。
- HUD 提供实时可视化，CI 中可通过 `omx setup && $autopilot …` 实现全自动化交付。

祝项目顺利落地 🚀