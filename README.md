# research-workflow

> End-to-end research workflow for Claude Code — an adversarial validation Gate across the
> full research lifecycle. 面向 Claude Code 的端到端科研工作流 —— 覆盖全研究生命周期的对抗性校验 Gate。

**[English](#english)** · **[中文](#中文)**

---

## English

`research-workflow` turns Claude Code into a research companion that walks a project from a
blank page to a submitted paper — literature exploration, problem formulation, method
design, evaluation design, experiments, writing, simulated peer review, and rebuttal — with
an **adversarial validation Gate** at every phase transition.

> **Core principle — finding a fatal flaw one phase earlier costs 10× less to fix.**

### What it is / who it's for

It is for anyone running a research project with Claude Code — students, researchers,
engineers writing systems / empirical / benchmark / survey / theory papers. Domain- and
venue-agnostic. It does **not** write your paper for you; it imposes a disciplined process —
typed artifacts, evidence-cited claims, pre-mortem reviews — so flaws surface early and
claims never outrun their evidence.

What it gives you:

- A **phased lifecycle** (Phase 0–9), each step with one clear artifact to produce.
- An **Adversarial Gate** at every transition — multi-persona reviewers hunt for fatal
  flaws before they become unfixable.
- **Anti-fabrication contracts** — every citation is verified, every quantitative claim
  carries a source.
- **Typed project state** — progress, risks, decisions, artifacts live in structured
  files, not in Claude's conversation memory.
- **Learning** — the skill records what worked and what failed and gets sharper with use.

### Install

```
/plugin marketplace add dianxiang-sun/research-workflow
/plugin install research-workflow@research-workflow
```

Restart Claude Code if prompted. The skill is then invocable as `/research-workflow:research`.

### Quick start (2 minutes)

```
/research-workflow:research init       # answer 5 questions: name, domain, paper type, venue, deadline
/research-workflow:research explore    # systematic literature scan + gap analysis
/research-workflow:research status     # phase, risks, next actions, time to deadline
```

`init` writes three files into your project's `.claude/` directory (see **Project files**).
After each phase the skill offers an Adversarial Gate — accept it, address its findings,
then move on. That is the whole loop.

### The research lifecycle

| Phase | Mode | Produces |
|-------|------|----------|
| 0 | `explore` | Literature landscape, gap analysis, a research direction |
| 1 | `foundation` | Deep reading, motivation, research questions |
| 2 | `design` | Method / framework design, novelty stress-test |
| 2.5 | `pilot` | Feasibility pilot on 5–10 examples |
| 3 | `eval-design` | Dataset, metrics, baselines, ablations — the highest-ROI gate |
| 4 | `implement` | Engineering implementation (systems / tool papers) |
| 5 | `experiment` | Experiment execution, monitoring, honest analysis |
| 6 | `write` | Paper writing with claim provenance |
| 7 | `review` | Multi-persona simulated peer review + submission prep |
| 8 | `rebuttal` | Reviewer response, camera-ready, or venue pivot |
| 9 | `present` | Talk / poster / demo preparation |

> Note: Phases 0-8 are the tracked main research sequence in `research-state.yaml`. Phase 9 (`present`) is a post-acceptance add-on; run `/research-workflow:research present` after acceptance for talk, poster, or demo preparation.

**Paper types** (chosen at `init`) decide which phases are active:

| Type | Active phases |
|------|---------------|
| `systems` | 0–8 (all) |
| `empirical` | 0–3, 5–8 — study design replaces implementation |
| `benchmark` | 0–3, 5–8 — evaluate the dataset / benchmark itself |
| `survey` | 0–1, survey-methodology, 6–8 |
| `theory` | 0–2, theory-proofs, 6–8 |

Phases are a guide, not a prison — work adjacent phases together, skip ahead to test an
idea, or use any mode at any time.

### Modes

Invoke as `/research-workflow:research <mode> [args]`.

**Lifecycle:** `init` · `status` · `explore` · `foundation` · `design` · `pilot` ·
`eval-design` · `implement` · `experiment` · `write [§N]` · `review` · `rebuttal` · `present`

**Cross-cutting — usable at any time:**

- `gate [N]` — run the Adversarial Gate (pre-mortem) for phase N (default: current).
- `rollback N` — structured return to phase N with impact analysis.
- `risk` — view / add / update the Risk Registry.
- `cost` — bottom-up cost / time estimate with failure-retry multipliers.
- `novelty-watch` — scan recent literature for competing work.
- `evolve` — periodic self-improvement: promote learned rules, update protocols.
- `mine-patterns` — extract writing patterns from past papers for style consistency.
- `advisor-prep` — prepare an advisor meeting: progress, open decisions, risk highlights.

Seven modes work **standalone** without `init` — `gate`, `review`, `explore`,
`novelty-watch`, `cost`, `write`, `present` — for ad-hoc use on any paper or idea.

### The Adversarial Gate

The Gate is the skill's core mechanism. At a phase transition (or any time via `gate [N]`):

1. Generates 3 reviewer personas — Methodology · Experiments · Domain Expert.
2. Each persona names its top-3 potential fatal flaws for this phase's output.
3. Each flaw gets a severity (Fatal / Serious / Moderate), the fix cost now vs. at Phase 7,
   a fix proposal, and a paper defense if it cannot be fixed.
4. **Verdict: PASS · CONDITIONAL (fix first) · BLOCK (rethink).**
5. On CONDITIONAL / BLOCK, a **critique loop-back** turns each finding into a delta-query
   and auto-searches or proposes a concrete fix.
6. A **direction synthesis** records the next-loop direction — DEEPEN / BROADEN / PIVOT /
   CONCLUDE — into `findings.md`.

### Autonomy levels

Set `autonomy_level` in `.claude/research-project.local.md`. It controls only **how often
the skill pauses for your approval** — never phase order, never whether a Gate runs.

| Level | Pause cadence |
|-------|---------------|
| `manual` | After every mode. |
| `checkpoint` *(default)* | Autonomous within a mode; pause at every Gate and before every must-log decision. |
| `gate-only` | Autonomous within a phase; pause only at Gates. |
| `full-auto` | No routine pause — run and report continuously. |

**Mandatory checkpoints pause at every level, including `full-auto`:** new spending, a new
external-facing claim, a reviewer commitment, an irreversible submission. **SmartPause**
also pauses whenever the skill cannot cite evidence for a step. A fresh install defaults to
the conservative `checkpoint`.

### Project files

`init` creates three files in your project's `.claude/`:

| File | Holds |
|------|-------|
| `research-project.local.md` | Config — name, domain, paper type, venue, deadline, `autonomy_level`, domain adapter |
| `research-state.yaml` | Live typed state — phases, gates, artifacts, risks, decisions, milestones |
| `findings.md` | Outer-loop narrative memory — current understanding, patterns, open questions, the Gate-synthesis trail |

They are yours — they stay in your project, are read by the skill at every invocation, and
are where your research state lives.

### Learning & runtime state

The skill sharpens with use through five mechanisms — structured reflection (Reflexion),
outcome-quality tracking, runtime context injection, a three-tier memory, and semantic
routing. Learned rules / reflections / outcomes / routes are **runtime state**, stored
**outside the plugin bundle** so an update never wipes them:

- Default: `~/.claude/research/memory/`
- Override: set `RESEARCH_SKILL_STATE_DIR` to an **absolute, writable directory**.

A fresh install starts cold — no learned rules — and bootstraps from your usage. The
bundled `research-reflect` / `research-router` tools manage this state; the skill invokes
them for you.

### Global Rules (inviolable)

G1 Zero fabrication · G2 Scope lock · G3 Adversarial Gate obligation · G4 Evidence before
claims · G5 Honest reporting · G6 Cost awareness · G7 Claim–evidence boundary · G8
Net-complexity budget · **G9 Review-simulation honesty**. They hold at every autonomy level.

### Optional: companion commands

The phase files reference nine `/companion-command` items — `/map-reduce-papers`, `/speed-read`, `/verify-before-write`, `/verify-citations`, `/pipeline-review`, `/architecture-review`, `/disk-first-batch`, `/canary-check`, `/session-checkpoint`. **None of them ship with this plugin** — they are independent commands you may have installed separately. The skill works without any of them; every reference degrades to an inline manual fallback documented in the corresponding phase file (full table: `skills/research/reference/skill-integration.md`). Two of them — `/verify-before-write` and `/verify-citations` — gate G1 (zero fabrication), and the inline fallback is **mandatory** regardless: only the *command* is optional, the verification itself MUST always happen.

### Optional: semantic-router hook

`research-router` can power a `UserPromptSubmit` hook that auto-suggests a mode from a
plain-language message. It is **opt-in** — the skill is fully correct without it;
`/research-workflow:research <mode>` is the canonical dispatch path. To enable it, wire a
`UserPromptSubmit` hook that calls `research-router route "<message>"` and surfaces the
suggestion. Without the hook you simply invoke modes yourself.

### Scope & ethics

See [SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md). In short: the simulated peer review
(`review` and the Gate personas) is a **pre-mortem self-review of your own work** — never a
substitute for, or an undisclosed input to, a real venue peer review (Global Rule G9). The
optional cross-model review transmits your manuscript to an external API — check
confidentiality and disclosure rules first.

### FAQ

**Do I need a project to use it?** No — `gate`, `review`, `explore`, `novelty-watch`,
`cost`, `write`, `present` work standalone. Full lifecycle tracking needs `init`.

**Does it write my paper?** No. It runs a disciplined process — typed artifacts, verified
citations, pre-mortem reviews. You and Claude do the research; the skill keeps it honest.

**Could an update wipe my learned rules?** No — runtime state lives outside the plugin
(`~/.claude/research/memory/`). If you relocated it, point `RESEARCH_SKILL_STATE_DIR` back.

**`research-reflect: command not found`?** The `bin/` wrappers are on PATH only when the
plugin is installed and enabled. Re-enable the plugin or restart Claude Code. The skill
still dispatches correctly without the tools — only the learning features pause.

### Release history

A plain-language summary of what each 0.1.x release changed and why it matters to you. Items marked **[important]** are the most user-visible data / behavior bugs; the rest are mostly docs / internal cleanup or one-time install / onboarding fixes called out inline.

- **0.1.8** — **[important]** Closed a remaining gap where a brand-new rule could be marked "hard" (mandatory) without ever being validated; `--confidence` now rejects out-of-range / `nan` / `inf` values. Also merged the three-tier-memory doc inline.
- **0.1.7** — `query-*` commands gained a `--json` flag for machine-readable output (so `evolve` can consume it). Mostly invisible in normal use.
- **0.1.6** — Docs cleanup: separated "run a gate" from "review a manuscript", and clarified that Phase 9 (`present`) is a post-acceptance add-on, not part of the tracked 0–8 pipeline.
- **0.1.5** — Renamed gate-matrix row codes to `DV*` / `RP*` so they stop colliding with the review-rubric and Global-Rule codes (you may see slightly different labels).
- **0.1.4** — Removed a stale bundled file and a duplicated protocol; successful runs no longer ask the "what did we miss?" reflection question.
- **0.1.3** — **[important]** Concurrency fix: parallel agents writing learned rules at the same time no longer lose each other's updates (file lock). Single-session use is unaffected.
- **0.1.2** — **[important]** Rule "hardening" now requires validation across enough runs and multiple phases before a rule becomes a mandatory "hard" rule; retired rules can no longer be revived by `boost-rule`.
- **0.1.1** — Removed dead-code fallback for a pre-release project format.
- **0.1.0** — First public release: bilingual manual + the full toolchain. A burst of post-release fixes (same version) removed assumptions that only held on the author's machine: tool command names, the `/research-workflow:research` dispatch path, reliable `init`, read-only-safe `evolve`, and route persistence.

**Upgrading:** use `/research-workflow:research <mode>` (bare `/research` is no longer the recommended form). If you logged rules before 0.1.8, ask Claude to list any over-confident "hard" rules first, then downgrade them — only retire ones that are clearly wrong.

### License

MIT — see [LICENSE](LICENSE).

---

## 中文

`research-workflow` 把 Claude Code 变成一个科研搭档,带着一个项目从空白页走到投稿 ——
文献探索、问题奠基、方法设计、评估设计、实验、写作、模拟同行评审、rebuttal —— 并在
**每一次阶段转换**都设一道**对抗性校验 Gate**。

> **核心原则 —— 早一个阶段发现致命伤,修复成本低 10 倍。**

### 这是什么 / 给谁用

给任何用 Claude Code 做科研项目的人 —— 写 systems / empirical / benchmark / survey /
theory 论文的学生、研究者、工程师。领域无关、venue 无关。它**不替你写论文**;它强加一套
有纪律的流程 —— 类型化产物、带证据引用的 claim、pre-mortem 评审 —— 让缺陷尽早暴露、让
claim 永远不超出它的证据。

它给你:

- 一条**分阶段的生命周期**(Phase 0–9),每步只产出一个明确的 artifact。
- 每次转换处的一道**对抗性 Gate** —— 多视角审稿人在致命伤变得无法修复前把它揪出来。
- **反捏造契约** —— 每条引用都被核实,每个量化 claim 都带来源。
- **类型化项目状态** —— 进度、风险、决策、artifact 存在结构化文件里,而非 Claude 的对话记忆里。
- **学习能力** —— skill 记录什么有效、什么失败,越用越锋利。

### 安装

```
/plugin marketplace add dianxiang-sun/research-workflow
/plugin install research-workflow@research-workflow
```

如提示则重启 Claude Code。之后该 skill 以 `/research-workflow:research` 调用。

### 快速上手(2 分钟)

```
/research-workflow:research init       # 回答 5 个问题:名称、领域、论文类型、venue、deadline
/research-workflow:research explore    # 系统性文献扫描 + gap 分析
/research-workflow:research status     # 当前阶段、风险、下一步、距 deadline
```

`init` 会在你项目的 `.claude/` 目录写入三个文件(见**项目文件**)。每个阶段结束后 skill
会提议一道对抗性 Gate —— 接受它、处理它的发现、再往下走。整个循环就是这样。

### 研究生命周期

| Phase | Mode | 产出 |
|-------|------|------|
| 0 | `explore` | 文献全景、gap 分析、一个研究方向 |
| 1 | `foundation` | 深读、motivation、研究问题 |
| 2 | `design` | 方法 / 框架设计、novelty 压力测试 |
| 2.5 | `pilot` | 5–10 个样本的可行性 pilot |
| 3 | `eval-design` | 数据集、指标、baseline、消融 —— ROI 最高的一道 gate |
| 4 | `implement` | 工程实现(systems / tool 论文) |
| 5 | `experiment` | 实验执行、监控、诚实分析 |
| 6 | `write` | 带 claim 溯源的论文写作 |
| 7 | `review` | 多视角模拟同行评审 + 投稿准备 |
| 8 | `rebuttal` | 审稿回复、camera-ready,或转投 |
| 9 | `present` | 报告 / 海报 / demo 准备 |

> 注:0-8 是 `research-state.yaml` 跟踪的主研究流程。Phase 9（`present`）是论文接收后的附加流程;accepted 后再运行 `/research-workflow:research present` 准备报告、海报或 demo。

**论文类型**(`init` 时选定)决定哪些阶段生效:

| 类型 | 生效阶段 |
|------|----------|
| `systems` | 0–8(全部) |
| `empirical` | 0–3、5–8 —— 研究设计取代实现 |
| `benchmark` | 0–3、5–8 —— 评估数据集 / benchmark 本身 |
| `survey` | 0–1、survey-methodology、6–8 |
| `theory` | 0–2、theory-proofs、6–8 |

阶段是指南、不是牢笼 —— 可同时推进相邻阶段、跳前面试想法、随时用任何 mode。

### 模式

以 `/research-workflow:research <mode> [args]` 调用。

**生命周期:** `init` · `status` · `explore` · `foundation` · `design` · `pilot` ·
`eval-design` · `implement` · `experiment` · `write [§N]` · `review` · `rebuttal` · `present`

**横切 —— 任何时候可用:**

- `gate [N]` —— 对阶段 N 跑对抗性 Gate(pre-mortem,默认当前阶段)。
- `rollback N` —— 带影响分析地结构化回退到阶段 N。
- `risk` —— 查看 / 新增 / 更新风险登记表。
- `cost` —— 含失败-重试乘数的 bottom-up 成本 / 时间估算。
- `novelty-watch` —— 扫描最新文献里的竞争工作。
- `evolve` —— 周期性自我改进:提升学到的规则、更新协议。
- `mine-patterns` —— 从过往论文提取写作风格模式。
- `advisor-prep` —— 准备导师会议:进度、待决策、风险要点。

七个模式**无需 `init` 即可独立使用** —— `gate`、`review`、`explore`、`novelty-watch`、
`cost`、`write`、`present` —— 用于对任何论文或想法的临时使用。

### 对抗性 Gate

Gate 是 skill 的核心机制。在阶段转换处(或随时通过 `gate [N]`):

1. 生成 3 个审稿人 persona —— Methodology · Experiments · Domain Expert。
2. 每个 persona 对本阶段产出列出 top-3 潜在致命伤。
3. 每个致命伤标注严重度(Fatal / Serious / Moderate)、现在修 vs Phase 7 修的成本、
   修复方案、若无法修则给论文里的辩护说法。
4. **裁决:PASS · CONDITIONAL(先修)· BLOCK(重新想)。**
5. CONDITIONAL / BLOCK 时,一个**critique loop-back** 把每条发现变成 delta-query,
   自动检索或给出具体修复。
6. 一次**方向综合**把下一轮方向 —— DEEPEN / BROADEN / PIVOT / CONCLUDE —— 记入 `findings.md`。

### 自主级别

在 `.claude/research-project.local.md` 设 `autonomy_level`。它只控制 **skill 多久暂停一次
等你批准** —— 绝不改变阶段顺序、绝不决定 Gate 是否运行。

| 级别 | 暂停节奏 |
|------|----------|
| `manual` | 每个 mode 后都暂停。 |
| `checkpoint`(默认) | mode 内自主;每道 Gate、每个 must-log 决策前暂停。 |
| `gate-only` | 阶段内自主;只在 Gate 暂停。 |
| `full-auto` | 无例行暂停 —— 连续运行并汇报。 |

**强制 checkpoint 在每个级别(含 `full-auto`)都暂停:** 新花钱、新的对外声明、向作者方做出
的评审承诺、不可逆的提交。**SmartPause** 也会在 skill 无法为某步引用证据时暂停。全新安装
默认保守的 `checkpoint`。

### 项目文件

`init` 在你项目的 `.claude/` 下创建三个文件:

| 文件 | 装什么 |
|------|--------|
| `research-project.local.md` | 配置 —— 名称、领域、论文类型、venue、deadline、`autonomy_level`、domain adapter |
| `research-state.yaml` | 实时类型化状态 —— phases、gates、artifacts、risks、decisions、milestones |
| `findings.md` | 外层叙事记忆 —— 当前理解、模式、待解问题、Gate-综合轨迹 |

它们是你的 —— 留在你的项目里,skill 每次调用都读它们,你的研究状态就活在这里。

### 学习机制与运行时状态

skill 通过五个机制越用越锋利 —— 结构化反思(Reflexion)、产出质量追踪、运行时上下文注入、
三层记忆、语义路由。学到的规则 / 反思 / 产出 / 路由是**运行时状态**,存在 **plugin bundle
之外**,因此更新永远不会抹掉它们:

- 默认:`~/.claude/research/memory/`
- 覆盖:把 `RESEARCH_SKILL_STATE_DIR` 设为一个**绝对、可写的目录**。

全新安装从冷启动开始 —— 没有学到的规则 —— 从你的使用中自举。随附的 `research-reflect` /
`research-router` 工具管理这份状态;skill 会替你调用它们。

### 全局规则(不可违反)

G1 零捏造 · G2 范围锁 · G3 对抗性 Gate 义务 · G4 证据先于 claim · G5 诚实汇报 · G6 成本
意识 · G7 claim–证据边界 · G8 净复杂度预算 · **G9 评审模拟诚实性**。它们在每个自主级别都成立。

### 可选:companion commands

skill 的 phase 文件中引用了 9 个 `/companion-command` —— `/map-reduce-papers`、`/speed-read`、`/verify-before-write`、`/verify-citations`、`/pipeline-review`、`/architecture-review`、`/disk-first-batch`、`/canary-check`、`/session-checkpoint`。**它们都不随本插件分发**,是用户可能另装的独立命令。skill 在没有它们时仍可工作 —— 每处引用都降级到对应 phase 文件中描述的内联手动 fallback(完整表见 `skills/research/reference/skill-integration.md`)。其中两个 —— `/verify-before-write` 和 `/verify-citations` —— 关乎 G1(零捏造)硬规则,内联 fallback **强制执行**:只有*命令*是可选的,验证本身永远 MUST 发生。

### 可选:语义路由 hook

`research-router` 可驱动一个 `UserPromptSubmit` hook,从一句自然语言自动建议合适的 mode。
它是**可选的** —— 没有它 skill 也完全正确;`/research-workflow:research <mode>` 是正规
派发路径。要启用它,接一个调用 `research-router route "<消息>"` 并呈现建议的
`UserPromptSubmit` hook。没有 hook,你自己调用 mode 即可。

### 范围与伦理

见 [SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md)。简言之:模拟同行评审(`review` 与 Gate 的
persona)是**对你自己工作的 pre-mortem 自审** —— 绝不充当、也绝不作为未披露的输入进入真实
venue 同行评审(全局规则 G9)。可选的 cross-model 评审会把你的稿件传给外部模型 API ——
先确认机密性与披露规则。

### 常见问题

**一定要先建项目吗?** 不用 —— `gate`、`review`、`explore`、`novelty-watch`、`cost`、
`write`、`present` 可独立使用。完整生命周期追踪才需要 `init`。

**它会替我写论文吗?** 不会。它跑一套有纪律的流程 —— 类型化 artifact、核实过的引用、
pre-mortem 评审。研究是你和 Claude 做的;skill 负责让它诚实。

**更新会抹掉我学到的规则吗?** 不会 —— 运行时状态存在 plugin 之外
(`~/.claude/research/memory/`)。若你迁移过它,把 `RESEARCH_SKILL_STATE_DIR` 指回去。

**`research-reflect: command not found`?** `bin/` wrapper 只有在 plugin 已安装并启用时才
在 PATH 上。重新启用 plugin 或重启 Claude Code。没有这些工具,skill 仍能正确派发 —— 只是
学习功能暂停。

### 发布历史

每个 0.1.x 版本改了什么、对你意味着什么的大白话小结。标 **【重要】** 的是最值得留意的数据 / 行为类 bug;其余多为文档 / 内部整理,或条目里单独说明的一次性安装 / 上手修复。

- **0.1.8** — **【重要】** 堵上最后一个漏洞:新建的规则原先可能没经任何验证就被标成"铁律"(强制执行);`--confidence` 现在会拒绝超范围 / `nan` / `inf`。另把三层记忆的说明合并进正文。
- **0.1.7** — `query-*` 命令新增 `--json` 选项输出机器可读格式(供 `evolve` 消费)。日常使用基本无感。
- **0.1.6** — 文档整理:把"跑 Gate"和"审稿"分开讲清,并说明 Phase 9(`present`)是录用后的附加项,不属被追踪的 0–8 主流程。
- **0.1.5** — gate-matrix 行号改名 `DV*` / `RP*`,不再与审稿 rubric、全局规则编号撞车(你可能看到标签略有变化)。
- **0.1.4** — 删掉一个过时的捆绑文件和重复协议;成功完成的运行不再追问"这次有什么没覆盖到"。
- **0.1.3** — **【重要】** 并发修复:多个 agent 同时写学习规则时不再互相覆盖丢失(加了文件锁)。单会话使用不受影响。
- **0.1.2** — **【重要】** 规则"强化"现在要经过足够次数、跨多个阶段验证,才会升级成强制的"铁律";退役规则不能再被 `boost-rule` 复活。
- **0.1.1** — 删掉一段针对发布前项目格式的死代码兜底。
- **0.1.0** — 首次公开发布:双语手册 + 完整工具链。发布后一批同版本号的急修,移除了只在作者本机成立的假设:工具命令名、`/research-workflow:research` 派发路径、可靠的 `init`、只读环境也能跑的 `evolve`、以及路由持久化。

**升级提示:** 用 `/research-workflow:research <mode>`(裸 `/research` 已不是推荐写法)。若你在 0.1.8 前记录过规则,先让 Claude 列出过度自信的"铁律"规则审查,再降级 —— 只退役明显错误的。

### 许可证

MIT —— 见 [LICENSE](LICENSE)。
