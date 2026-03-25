# Oh‑My‑OpenCode (omx) Quick‑Start Guide for the Smart Downloader Repository

---

## 🎯 Goal

1. **Run the full end‑to‑end (E2E) test suite** for the *Smart Downloader* project and generate a passing report.
2. **Set up Oh‑My‑OpenCode (omx) inside this OpenCode repository** so you can drive future development with its multi‑agent workflow:
   - Plan → PRD → Execute → Verify → Fix

---

## 📦 Prerequisites

| Tool | Install Command |
|------|-----------------|
| **Playwright (Firefox, headless)** | `npm i -D @playwright/test && npx playwright install firefox` |
| **Codex CLI** (for `$` commands) | `npm i -g @openai/codex` |
| **Oh‑My‑OpenCode** (omx) | `npm i -g oh-my-codex` |
| **Node ≥ 18** (recommended) | See your local Node version with `node -v` |

Make sure you have a valid **OpenAI API key** available as the environment variable `OPENAI_API_KEY` (required by Codex and omx).

---

## 🛠️ 1️⃣ Install & Verify the Toolchain

```bash
# Install Playwright (Firefox headless) – already in repo dev dependencies
npm i -D @playwright/test
npx playwright install firefox

# Install Codex CLI (global)
npm i -g @openai/codex

# Install Oh‑My‑OpenCode (global)
npm i -g oh-my-codex
```

### Verify installations

```bash
playwright -V               # → prints version, should include Firefox
codex -v                    # → prints Codex CLI version
omx -V                      # → prints omx version
```

If any command fails, re‑run the corresponding install line.

---

## 🚀 2️⃣ Run the E2E Test Suite

The repository ships an **E2E master script** that uses Playwright‑Firefox in headless mode and logs in via the authentication API (no UI login flakiness).

```bash
# From the repository root:
python3 skills/e2e-testing/scripts/e2e_master.py --full
```

### What the script does

1. **Starts the backend** (`uvicorn smart_downloader.main:app --port 8001`).
2. **Starts the front‑end** (`npm run dev` on port 3000).  
   → Both URLs are printed to the console.
3. **Logs in via API** (POST `/api/auth/login`).
4. Stores the returned JWT in `localStorage` (`access_token`).
5. **Runs the Playwright test suite** (`npm run test`).
6. **Generates reports**:
   - JSON: `smart-downloader/reports/e2e_report_<timestamp>.json`
   - Text: `smart-downloader/reports/e2e_report_<timestamp>.txt`
7. **Screenshots on failure** are saved under `smart-downloader/screenshots/` (empty when all tests pass).

✅ After a successful run you should see `0` failures and the two report files mentioned above.

---

## 🛠️ 3️⃣ Initialise Oh‑My‑OpenCode (omx) for This Repo

```bash
# Run setup – the `--force` flag overwrites any existing configuration files.
omx setup --force
```

What `omx setup` creates (all under `~/.omc/` and `~/.codex/`):

- **Prompt library** (`PROMPTS/`) – default prompts for planning, PRD, code‑review, security‑review, etc.
- **Skill catalog** (`SKILLS/`) – ready‑to‑use Codex skills (e2e‑testing, code‑refactoring, …).
- **AGENTS.md** – description of all built‑in agents (Planner, Reviewer, Tester, …).
- **MCP configuration** (`~/.omc/state/config.toml`).
- **HUD assets** (`~/.omc/hud/`) – optional real‑time UI you can launch with `omx hud`.

---

## ✅ 4️⃣ Verify the Oh‑My‑OpenCode Setup

```bash
omx doctor
```

You should see **10 checks** (CLI, prompts, skills, agents, MCP, HUD, memory, etc.) all passing.  If a check fails, the output tells you exactly what to fix (usually a missing environment variable or a stale configuration file).

---

## 💡 5️⃣ Core `omx` / `codex` Commands

| Command | Description |
|---------|-------------|
| `$plan "<goal>"` | Generates a high‑level plan (tasks, dependencies, acceptance criteria). |
| `$prd "<goal>"` | Turns a plan into a full Product Requirements Document (sectioned). |
| `$code "<goal>"` | Executes the plan: writes code, runs tests, creates a Git branch/commit. |
| `$autopilot "<goal>"` | **One‑liner** – does plan → PRD → code → verify → PR creation automatically. |
| `$tdd "<goal>"` | Starts a Test‑Driven‑Development cycle (writes failing test, implements, runs). |
| `$code‑review` | Runs the **code‑review** skill on the current branch and posts a summary. |
| `$security‑review` | Runs the **security‑review** skill (static analysis, OWASP checks). |
| `$memory save "<key>"` | Persists a snippet or JSON in the agent’s long‑term memory. |
| `$memory recall "<key>"` | Retrieves the saved snippet. |
| `omx hud` | Launches a tiny web HUD that visualises the current workflow, agents, and memory. |
| `omx team start <team‑name>` | Spins up a multi‑agent team (Planner, Reviewer, Tester, …) for a given goal. |

All `$` commands are typed **inside the Codex REPL** (run `codex` to start):

```bash
codex       # opens the REPL prompt
$plan "实现文件上传功能（前端+后端+测试）"
```

The REPL will echo the AI‑generated output, and you can pipe it to a file, commit, or let the agent automatically push a branch and open a PR on GitHub (requires `GITHUB_TOKEN`).

---

## 📁 6️⃣ Generated Files & Where to Find Them

| Path | Purpose |
|------|---------|
| `smart-downloader/reports/` | JSON & text E2E reports (timestamped). |
| `smart-downloader/screenshots/` | Screenshots captured on test failures. |
| `~/.codex/` | Global Codex configuration, prompt cache, skill registry. |
| `~/.omc/` | Oh‑My‑OpenCode state: prompts, skills, agents, HUD, memory, trace logs. |
| `oh_my_opencode_manual.md` | This manual you just created (in the repo root). |

---

## 📦 7️⃣ Example CI Integration (GitHub Actions)

Add the following workflow to `.github/workflows/omx.yml` (replace `GITHUB_TOKEN` with a repo‑scoped token if you need PR creation):

```yaml
name: omx CI
on:
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize ]

jobs:
  omx‑run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          npm ci
          pip install -r requirements.txt   # if Python deps exist
      - name: Install Codex & omx
        run: |
          npm i -g @openai/codex
          npm i -g oh-my-codex
      - name: Initialise omx
        run: omx setup --force
      - name: Run omx doctor (fails fast if mis‑configured)
        run: omx doctor
      - name: Autopilot – generate a feature PR
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          codex
          $autopilot "实现文件上传功能（前端+后端+测试）"
```

When the workflow succeeds, a PR will appear automatically with the generated code, tests, and a review comment.

---

## 🧭 8️⃣ Next Steps / Suggested Workflow

1. **Pick a feature** (e.g., *file upload* – the default in this guide).  
2. Open the Codex REPL: `codex`.
3. Run the one‑liner: `$autopilot "实现文件上传功能（前端+后端+测试）"`.
4. Observe the REPL output – it will create a branch, commit, run the test suite, and open a PR on GitHub.
5. **Review the PR** – you can let the built‑in `$code‑review` and `$security‑review` agents comment automatically, or do a manual review.
6. **Merge** once all checks pass.
7. Rinse & repeat for the next feature.

---

## ❓ Need Anything Else?

- Want a **custom prompt** (e.g., fintech‑architect) before running autopilot?  
- Want to **add a new skill** to the catalog?  
- Need help configuring the **HUD** (`omx hud`) for a visual view of agents?  

Just let me know and I’ll walk you through the extra steps! 

---

*Generated on $(date)*
