---
name: research
description: "End-to-end research workflow skill covering the full lifecycle: direction exploration, literature survey, problem formulation, method design, evaluation design, implementation, experiments, paper writing, review, and post-submission. Use when starting any research phase, transitioning between phases, or needing adversarial pre-mortem review. Canonical command: /research-workflow:research <mode>. Triggers on natural-language phrases like 'research workflow', 'adversarial gate', 'pre-mortem review', 'research risk', 'novelty check', or any mention of research phases (explore, foundation, design, eval-design, implement, experiment, write, review, rebuttal)."
user_invocable: true
---

# Research Workflow Skill

> End-to-end research lifecycle management with adversarial validation gates.
> Domain-agnostic. Venue-agnostic. Supports multiple paper types.
> Project config in `.claude/research-project.local.md`; live state in `.claude/research-state.yaml`; narrative memory in `.claude/findings.md`.
> Phase details in `phases/`; templates in `templates/`.

## Quick Start (First-Time Users -- 2 Minutes)

1. **Initialize**: `/research-workflow:research init` -- answer 5 questions (project name, domain, paper type, venue, deadline)
2. **Start exploring**: `/research-workflow:research explore` -- systematic literature scan with gap analysis
3. **Follow the prompts**: The skill guides you through each phase. After each phase, it offers an Adversarial Gate review.
4. **Check progress anytime**: `/research-workflow:research status` -- see what's done, what's next, how much time left

That's it. Everything else (learning mechanisms, agent patterns, evolution) works automatically in the background.

### Glossary

| Term | Meaning |
|------|---------|
| **Gate** | Adversarial review at phase transitions -- finds fatal flaws before they become unfixable |
| **G-V-R** | Generator-Verifier-Reviser -- a 3-step loop where content is created, checked, then fixed |
| **Worker-Critic** | Two agents: one creates, one immediately critiques -- ensures quality through separation |
| **CitationAgent** | A dedicated post-processing agent that verifies all citations after writing |
| **Reflexion** | Learning from failures: structured reflection -- predicate rules for next time |
| **MPR** | Meta-Policy Reflexion -- extracting IF/THEN rules from experience with confidence scores |
| **STORM** | Multi-perspective questioning technique for thorough literature coverage |
| **Recipe** | A pre-defined combination of mode + sub-features for a specific task type |
| **Oracle** | The source of truth used to evaluate results (e.g., test suite, static analyzer, human label) |

## ⚡ Smart Dispatch (READ THIS FIRST)

**Before doing ANYTHING, match the user's intent to a recipe.** Don't just pick a mode — pick the full recipe with all sub-features.

→ Full detail in **`reference/dispatch-recipes.md`**: the intent→recipe Decision Tree, Domain-Aware Activation (`[DOMAIN:xxx]` tags), the Quick Pattern Selection Guide, Context-Aware Auto-Suggestions, and Outcome-Driven Recipe Optimization.

**CRITICAL RULE**: If in doubt about which sub-features to activate, activate MORE rather than fewer. The user prefers thoroughness over speed.

## Usage

The canonical command — what you actually type at the Claude Code prompt:

```
/research-workflow:research <mode> [args]
```

This SKILL.md and the `phases/` / `reference/` files frequently shorten this to `/research <mode>` for prose readability. The shorthand is **for reading only** — when typing a command, suggesting one to the user, or printing one as runtime output, always use the canonical `/research-workflow:research <mode>` form. The bare `/research` namespace is unowned post-restructure and does not dispatch.

## Modes

| Mode | Description |
|------|-------------|
| `init` | Initialize project config, select paper type |
| `status` | Current phase, risks, blockers, next actions |
| `explore` | Phase 0: Literature landscape, gap analysis, direction decision |
| `foundation` | Phase 1: Deep reading, motivation, RQ formulation |
| `design` | Phase 2: Method/framework design with novelty stress test |
| `pilot` | Phase 2.5: Feasibility pilot (5-10 examples before full eval design) |
| `eval-design` | Phase 3: Dataset, metrics, baselines, ablation — **HIGHEST-ROI GATE** |
| `implement` | Phase 4: Engineering implementation (systems/tool papers) |
| `experiment` | Phase 5: Experiment execution, monitoring, honest analysis |
| `write [§N]` | Phase 6: Paper writing with claim provenance + narrative quality |
| `review` | Phase 7: Multi-persona simulated peer review + submission prep |
| `rebuttal` | Phase 8: Reviewer response, camera-ready, or venue pivot |
| `gate [N]` | Adversarial Gate: pre-mortem for phase N (default: current) |
| `rollback N` | Phase Rollback: structured return to phase N with impact analysis |
| `risk` | Risk Registry: view, add, update, mitigate |
| `cost` | Cost/time estimation with iteration multipliers |
| `novelty-watch` | Literature freshness scan for competitive threats |
| `present` | Phase 9: Presentation preparation (talk, poster, demo) |
| `evolve` | Periodic self-improvement: analyze usage, promote rules, update protocols |
| `mine-patterns` | Extract writing patterns from past papers for style consistency |
| `advisor-prep` | Prepare advisor meeting: progress summary, open decisions, risk highlights |

## Intelligence Infrastructure (5 Learning Mechanisms)

> **This skill gets smarter with every use.** Five mechanisms work together
> to make both triggering and content continuously evolve.

→ Full detail in **`reference/learning-mechanisms.md`**: Mechanism 1 (Structured Reflection + Predicate Rules), 2 (Outcome Quality Tracking), 3 (Dynamic Shell Injection), 5 (Semantic Routing), the Post-Invocation Protocol, Progress Tracking, and the `/research evolve` cycle. Mechanism 4 (Three-Tier Memory Architecture) is in **`reference/capability-memory.md`**.

## Execution Protocol

### Full project mode (has `.claude/research-project.local.md`)
1. Read `.claude/research-project.local.md` (config), `research-state.yaml` (live state), `findings.md` (narrative memory). If `research-state.yaml` is absent, this is a pre-M2 project — read the legacy flat `research-{progress,risks,decisions}.md` instead (one-release fallback).
2. Read `phases/phase-{N}.md` for the relevant phase
3. Apply Global Rules + the Autonomy Policy throughout
4. At phase completion, ALWAYS offer Adversarial Gate before advancing
5. For Phases 6-7, also read `phases/phase-supplementary.md` for artifact/ethics/collaboration guidance

### Standalone mode (no project config)
The following modes work WITHOUT `init` — for ad-hoc use on any paper/project:
- `gate` — Adversarial review of any paper, design, or evaluation plan
- `review` — Simulated peer review of any manuscript
- `explore` — Literature landscape scan for any topic
- `novelty-watch` — Check if a research idea has been done
- `cost` — Estimate experiment costs for any setup
- `write` — Writing protocol for any paper section
- `present` — Presentation preparation for any accepted paper

When invoked standalone, ask the user for minimal context (paper type, venue, topic) inline instead of requiring full init. Apply Global Rules regardless.

### `/research init` protocol
1. Ask user: project name, domain, paper type, target venue, deadline
2. Ensure `.claude/` exists, then materialize 3 templates into it:
   - `mkdir -p .claude` — Bash-tool init MUST NOT assume the directory already exists; brand-new projects do not have a `.claude/`.
   - For each template, use the Read tool to read it from the skill bundle and the Write tool to materialize it. Pick the first bundle path that resolves:
     1. `${CLAUDE_PLUGIN_ROOT}/skills/research/templates/<file>` — plugin-injected env var when available
     2. `~/.claude/plugins/marketplaces/research-workflow/skills/research/templates/<file>` — marketplace symlink layout
     3. `~/.claude/plugins/cache/research-workflow/research-workflow/<version>/skills/research/templates/<file>` — cache fallback (pick highest version if multiple)
   - The 3 mappings:
     - `research-project.template.md` → `.claude/research-project.local.md`
     - `research-state.yaml` → `.claude/research-state.yaml`
     - `findings.md` → `.claude/findings.md`
   - Do not use shell `cp "${CLAUDE_SKILL_DIR}/..."` — `${CLAUDE_SKILL_DIR}` is not reliably injected into the Bash-tool environment (empirically empty), and the resulting `cp /templates/...` expansion fails before mkdir can help.
3. Fill in `research-project.local.md` answers; `research-state.yaml` starts at `current_phase: 0`
4. Confirm: "Project initialized. Run `/research-workflow:research explore` to begin."

### `/research status` protocol
Read `.claude/research-state.yaml` (if absent → legacy `research-{progress,risks,decisions}.md`, one-release fallback). Display:
- Current phase + paper type (type from `research-project.local.md`)
- Days to deadline (if set); next open milestone (from `milestones:`)
- Phase / gate status (from `phases:`); per-phase typed artifact + lifecycle status (from `artifacts:`)
- Latest synthesis direction — the most recent `Gate synthesis:` line in `findings.md` (DEEPEN / BROADEN / PIVOT / CONCLUDE; a direction, not a gate verdict)
- Pending items = artifacts not yet `accepted` for the current phase + `findings.md` Open Questions
- Open risks: count by severity (from `risks:`)
- Recent outcomes: last 3 (from research-reflect query-outcomes)
- Active rules: hard count + soft count (from research-reflect query-rules)
- Last activity date (`last_activity`)

### Proactive suggestion protocol
A UserPromptSubmit hook monitors conversation for research-related context.
When triggered, Claude should briefly mention the relevant `/research` mode — e.g.:
> "这个场景可以用 `/research-workflow:research gate` 做系统化审查，要试试吗？"
Do NOT force-invoke the skill. One sentence suggestion, then follow the user's lead.

## Paper Types

Set during `init`. Determines which phases are active and how they adapt.

| Type | Phases Active | Key Differences |
|------|--------------|-----------------|
| `systems` | 0-8 (all) | Build artifact → evaluate → full pipeline |
| `empirical` | 0-3, 5-8 (skip 4) | Study design replaces implementation; data collection replaces coding |
| `benchmark` | 0-3, 5-8 (skip 4) | Evaluate the dataset/benchmark itself; baseline = existing benchmarks |
| `survey` | 0-1, survey-methodology, 6-8 | Systematic review methodology replaces Phases 2-5; see `phase-survey-methodology.md` |
| `theory` | 0-2, theory-proofs, 6-8 | Formal proofs replace Phases 3-5; see `phase-theory-proofs.md` |

Phase subfiles contain `[SYSTEMS]` `[EMPIRICAL]` etc. markers for type-specific guidance.

> **Phases are a guide, not a prison.** Real research is iterative. You can:
> - Work on adjacent phases simultaneously (e.g., write §3 while finalizing experiments)
> - Skip ahead to test an idea, then come back to formalize
> - Use any mode at any time -- the phase number is a suggested order, not a gate
>
> The formal Rollback Protocol (`/research rollback N`) is only needed for significant
> cross-gap regressions (e.g., Phase 5 discovers Phase 2 design is fundamentally wrong).
> For routine back-and-forth between adjacent phases, just do it naturally.

---

## Global Rules (INVIOLABLE)

### G1: Zero Fabrication
- NEVER fabricate citations, statistics, venue names, or experimental results
- Unverifiable claims: mark `[UNVERIFIED]`, never guess
- ENFORCED — every `\cite{}` clears the CitationAgent contract (≥2 metadata sources + retraction screen, `reference/capability-critique.md`); every quantitative claim carries `[source: file:line]` or `[source: Paper, §X, p.Y]`

### G2: Scope Lock
- At mode start, declare which files may be edited
- NEVER touch undeclared files — report and WAIT for approval

### G3: Adversarial Gate Obligation
- At every phase transition, MUST offer the Gate
- Never claim a phase "complete" without addressing Gate findings

### G4: Evidence Before Claims
- Every finding must cite exact file:line or §:paragraph
- NEVER dismiss findings without evidence; default to thoroughness

### G5: Honest Reporting
- Report negative results, limitations, failures
- Track weaknesses in Risk Registry; never hide unfavorable data

### G6: Cost Awareness
- Include failure/retry multipliers in all estimates
- Alert when actuals exceed estimates by >50%

### G7: Claim-Evidence Boundary
- For every claim/contribution, verify: evidence scope ≥ claim scope; wording must not overreach
- If claim says "secure" but evidence only covers "fewer Slither findings", flag the gap
- ENFORCED — the Phase-6 claims-from-results check downgrades any claim with no backing result artifact; unmet evidence is logged to `GAP_REPORT.md`, never written around (`reference/capability-artifacts.md`)

### G8: Net-Complexity Budget
- The skill's budget is **structural health, not raw line count** (`RESTRUCTURE-PLAN.md` §15). `SKILL.md` stays a thin dispatcher; `reference/` capability docs grow only by justification; DRY is enforced.
- Every `/research evolve` change proposal — and, during the restructure, every migration step — MUST carry a **Budget & Structure checklist**: the `wc -l` delta + cumulative trend · each new `reference/`/`templates/` file's D/R justification · each change classed *relocation* (names its paired delete) or *net-new gap-fill* (names the D/R item) · a DRY / pointer audit.
- ENFORCED — `/research evolve` runs the G8 mechanical hook (`phases/phase-evolve.md` § Budget & Structure Check): the `wc -l` trend, the 5-check structural sweep, the `SKILL.md` dispatcher-shape check. G8 REJECTS a proposal that omits the checklist or fails a mechanical check — never on a positive line-count delta alone.

### G9: Review-Simulation Honesty
- `/research review` and the multi-persona reviewer personas (Phase 7; the Adversarial Gate) **simulate** peer review — they are a pre-mortem self-review of the authors' OWN work, run by or for that work's authors to surface weaknesses before submission. They carry no venue authority.
- NEVER present a simulated review, or its scores, as a genuine external / venue peer review. NEVER run the skill to produce an AI-generated review for a manuscript you have been assigned to peer-review, or for any confidential submission — that is undisclosed AI peer review, which venues prohibit. On a third party's manuscript, `review` is valid ONLY as that manuscript's authors' own self-review aid (you are a co-author, or its authors asked you).
- ENFORCED — `phases/phase-7-review.md` opens with a scope-&-ethics banner + an operational provenance check; M5 ships this resident rule, M6 adds the fuller public scope-&-ethics doc and completes the §14.8 public-release ethics gate.

---

## Autonomy Policy

`autonomy_level` in `research-project.local.md` sets how often the skill pauses for
human approval — human-in-the-loop *cadence only*. It never changes phase order and
never decides whether an Adversarial Gate runs; Global Rules G1–G9 apply at every level.

| Level | Routine pause cadence |
|-------|----------------------|
| `manual` | Pause after every mode — the human approves each step forward. |
| `checkpoint` *(default)* | Autonomous within a mode; pause at every Adversarial Gate and before every Decision Log must-log event (§ Decision Log). |
| `gate-only` | Autonomous within a phase; pause only at Adversarial Gates (phase transitions). |
| `full-auto` | No routine pause between modes — run and report continuously. |

`full-auto` removes ONLY the routine pause: at every level a Gate `CONDITIONAL`/`BLOCK`
verdict still binds (G3 — address the findings, never pause-skip them), and the
mandatory checkpoints + SmartPause below still pause.

**Mandatory checkpoints — ALWAYS pause for explicit human approval, every level incl. `full-auto`:**
- **new spending** — committing unbudgeted API / compute / data / paid-human cost, or any budget increase;
- **a new external-facing claim** — text that will reach anyone outside this session: the manuscript, a submission, a rebuttal, a public artifact, or outbound co-author / advisor text;
- **a reviewer-promise or commitment** made on the authors' behalf;
- **an irreversible submission edit** — submitting, sending, or publishing.

**SmartPause** — at any level, pause and surface the uncertainty when the skill cannot
cite evidence for a step, faces options with no clear winner, or extrapolates beyond
what it verified.

Standalone invocations (no project config) use `checkpoint`. A shared / public install
defaults to `checkpoint`; opting up to `full-auto` is an explicit per-project choice.

---

## Adversarial Gate (`/research gate [N]`)

> **Principle**: Finding a flaw one phase earlier costs 10x less to fix.

### Protocol

1. Read project config for current phase and paper type
2. Select check dimensions from `reference/gate-matrix.md` (★ = deep, ○ = scan)
3. Generate 3 reviewer personas: Methodology | Experiments | Domain Expert
4. Each persona: top-3 potential fatal flaws for this phase's outputs
5. Deduplicate, consolidate
6. Per flaw: Severity (Fatal/Serious/Moderate) + fix cost now vs Phase 7 + fix proposal + paper defense if unfixable
7. Update Risk Registry
8. Verdict: **PASS** | **CONDITIONAL** (fix first) | **BLOCK** (rethink)

### Step 9: Critique Loop-Back (Auto-Fill Gaps)

If the Gate produces CONDITIONAL or BLOCK:
1. For each critical finding, generate a **delta-query**: "What additional information would resolve this?"
2. If the delta-query is answerable by literature search → auto-search (via Semantic Scholar MCP)
3. If answerable by running an experiment → estimate cost and propose to user
4. If answerable by rewriting → generate specific rewrite suggestion
5. Present the delta-queries and auto-found answers to the user
6. User approves → incorporate → re-run Gate on the updated content

This converts the Gate from a passive "find problems" tool into an active "find AND fix problems" loop.
Inspired by 199-biotechnologies deep-research critique loop-back pattern.

### Step 10: Direction Synthesis (R3)

Runs for EVERY Gate result — after the step-8 verdict and after any Step-9 loop-back
has finished (if loop-back re-ran the Gate, synthesize from the final verdict). This is
the skill's outer-loop "step back and synthesize" cadence, folded into the Gate itself,
not a separate scheduler or phase:

1. Update `findings.md` — Current Understanding, Patterns & Insights, Open Questions.
2. Append ONE labeled line to `findings.md` Open Questions naming the next-loop direction:
   `Gate synthesis: <DIRECTION> — <one-line reason> (<phase>, <YYYY-MM-DD>)`
   - **DEEPEN** — the direction holds; refine and continue the current phase line.
   - **BROADEN** — widen scope: add a sub-question, baseline, or comparison.
   - **PIVOT** — the direction is not working; change it via `/research rollback`.
   - **CONCLUDE** — evidence is sufficient; move toward write-up.

In standalone mode (no project `findings.md`) state the direction inline in the Gate
output instead. The direction is a synthesis call, NOT a gate verdict — the verdict
stays PASS / CONDITIONAL / BLOCK (step 8). `/research status` surfaces the latest
`Gate synthesis:` line.

### Check Dimensions

→ The full A–H check-dimension matrix (which dimensions apply per phase, `★` = deep / `○` = scan): **`reference/gate-matrix.md`**.

### Phase 3 Gate — MANDATORY 12 Questions

→ Phase 3 cascades catastrophically — ALL 12 mandatory questions must be cleared before Phase 4. The canonical checklist: **`phases/phase-3-eval-design.md`** (§ Gate Criteria — MANDATORY 12 QUESTIONS). The cross-cutting evaluation rules it enforces: **`reference/capability-evaluation.md`**.

### Generator-Verifier-Reviser Pattern (Aletheia-Inspired)

→ The G-V-R within-phase quality loop for high-stakes artifacts, plus the specialized agent patterns (Worker-Critic, CitationAgent, Citation Context Analysis): **`reference/capability-critique.md`**.

---

## Phase Rollback Protocol (`/research rollback N`)

→ Full protocol — Impact Analysis → Decision (fix-at-source / patch-downstream / abandon-&-pivot) → Execute (log, re-gate, propagate): **`reference/rollback.md`**.

---

## Guardian Mechanisms

### Risk Registry (`/research risk`)
The `risks:` block in `.claude/research-state.yaml` (schema: `reference/capability-artifacts.md`).

Rules:
- Gate findings ≥ Serious → auto-add
- Status: `open` → `mitigated` / `accepted_risk` / `resolved`
- `accepted_risk` MUST have paper defense + Threats section text
- Review at every phase transition

### Novelty Watch (`/research novelty-watch`)
Run monthly + before Phase 7. Search multiple query phrasings. Check arXiv, conf accepted lists. Overlap analysis → differentiation → citation update.

### Traceability Chain
```
RQ ← motivation [Paper, §X, p.Y]
 → metric → oracle → experiment config → raw results → paper claim [file:line]
```
Every link = concrete path. No abstract references.

### Decision Log
The `decisions:` block in `.claude/research-state.yaml` (schema: `reference/capability-artifacts.md`).

Must-log: direction pivots, venue changes, baseline/dataset/metric changes, scope cuts, budget changes. Feeds → Threats to Validity.

---

## Cost Estimation (`/research cost`)

→ Bottom-up estimate with iteration multipliers and a debug budget, plus the actual-vs-estimated tracking table: **`reference/cost-estimation.md`**.

---

## Skill Integration

→ Companion-skill delegation table and optional MCP integrations (Semantic Scholar, GPT-Researcher): **`reference/skill-integration.md`**.
→ The specialized agent patterns this skill relies on — Worker-Critic, CitationAgent, Citation Context Analysis, Generator-Verifier-Reviser: **`reference/capability-critique.md`**.

---

## Reference Files

Progressive-disclosure detail lives in `reference/`; `SKILL.md` stays a thin dispatcher and points to it.

| File | Contents |
|------|----------|
| `reference/dispatch-recipes.md` | intent→recipe decision tree · domain activation · pattern guide · auto-suggestions · recipe optimization |
| `reference/learning-mechanisms.md` | learning mechanisms 1/2/3/5 · post-invocation protocol · progress tracking · `/research evolve` |
| `reference/capability-memory.md` | three-tier memory architecture (mechanism 4) |
| `reference/capability-critique.md` | Worker-Critic · CitationAgent · citation-context analysis · Generator-Verifier-Reviser |
| `reference/capability-artifacts.md` | typed artifact contracts · project-state tree · Direction/RQ Card schemas |
| `reference/capability-evaluation.md` | evaluation-integrity rules · oracle/instrument/contamination · immutable evaluator · leakage audit |
| `reference/capability-ideation.md` | direction-ideation — gap taxonomy · brainstorming lenses · Diverge/Converge/Refine · disposition filters |
| `reference/gate-matrix.md` | the A–H gate check-dimension matrix |
| `reference/rollback.md` | full phase-rollback protocol |
| `reference/cost-estimation.md` | cost/time estimation formula |
| `reference/skill-integration.md` | companion-skill delegation + MCP integrations |

---

## Anti-Patterns Prevented

| Anti-Pattern | Mechanism |
|-------------|-----------|
| Fabricated citations | G1 + `/verify-before-write` (if installed) — manual citation re-read fallback otherwise (`phase-1-foundation.md:21`); the *verification* is mandatory, only the command is optional |
| Late fatal flaws | Gate at every transition |
| Unauthorized edits | G2 Scope Lock |
| Shallow reviews | G4 + multi-persona |
| Optimistic cost | G6 + retry multipliers |
| LLM-evaluates-LLM | B4 + Oracle Matrix |
| Unreliable tools | B3 + Instrument Matrix |
| Unfair baselines | C1-C2 + original code |
| Claim overreach | G7 + B5 boundary check |
| Scope creep | Decision Log + kill conditions |
| Novelty erosion | Novelty Watch |
| Results ≠ RQs | B1 causal chain |
| Irreproducible | E1-E3 + code freeze |
| Post-hoc narrative | Contingency before experiments |
| Bad story | H1 narrative arc check |
| Incomplete related work | H2 audit |
| Weak threats section | H3 + Risk Registry → Threats |
| Over page limit | H4 page budget |
