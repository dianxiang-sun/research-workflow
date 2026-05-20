# Dispatch Recipes — intent → full recipe

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

### Decision Tree: User Intent → Full Recipe

### Domain-Aware Activation

Content tagged [DOMAIN:xxx] in phase files activates based on the `domain` field
in .claude/research-project.local.md. Rules:
- [DOMAIN:security] → activates when domain contains "security", "vulnerability", "smart contract", "blockchain"
- [DOMAIN:se] → activates when domain contains "software engineering", "SE", "testing", "code"
- Untagged content → ALWAYS active (universal)
- When no project config exists (standalone mode): ask user's domain, then activate accordingly
- Multiple tags can apply simultaneously (e.g., a security SE paper gets both)

```
User wants to SEARCH/EXPLORE literature:
  → /research-workflow:research explore
  → USE: Semantic Scholar MCP (if available) for automated search
  → USE: Multi-perspective questioning (STORM pattern) for coverage
  → AFTER: Update progress tracker

User wants to DESIGN method/framework:
  → /research-workflow:research design
  → USE: Generator-Verifier-Reviser (G-V-R) for the design doc
  → AFTER: Offer /research-workflow:research gate 2

User wants to VALIDATE feasibility (pilot study):
  → /research-workflow:research pilot
  → RUN: 5-10 representative inputs through your method
  → INSPECT: Manually check outputs — reasonable?
  → DECIDE: 4-5/5 pass → proceed; 0-1/5 → return to Phase 2
  → DOCUMENT: Feed results into Phase 3 cost estimation

User wants to DESIGN evaluation:
  → /research-workflow:research eval-design
  → USE: G-V-R for the eval plan (this is the highest-stakes artifact)
  → MUST: Fill ALL matrices (Oracle, Instrument, Fairness)
  → AFTER: Run /research-workflow:research gate 3 (mandatory 12 questions)

User wants to WRITE a paper section:
  → /research-workflow:research write §N
  → USE: Worker-Critic pair (Worker writes, Critic reviews immediately)
  → AFTER WRITING: Spawn CitationAgent to verify all \cite{}
  → AFTER WRITING: Check claim-evidence boundary (G7)
  → AFTER WRITING: Update progress tracker (check off completed §)
  → IF writing Related Work: Apply citation context analysis (supporting/contrasting/mentioning)
  → IF writing Threats: Pull from Risk Registry (accepted_risk items)

User wants to REVIEW/AUDIT a paper:
  → /research-workflow:research review (or /research-workflow:research gate)
  → USE: 7-dimension rubric (D1-D7, each scored 1-5) with 5 personas
  → IF multiple LLM APIs available: Add cross-model review (Claude writes → GPT reviews)
  → AFTER: Critique loop-back (auto-search for delta-queries if CONDITIONAL/BLOCK)
  → AFTER: Update progress tracker

User wants to RUN experiments:
  → /research-workflow:research experiment
  → USE: Pre-experiment checklist (ALL items must pass)
  → IF parallel agents: Enable subagent health monitoring (escalating checks + auto-restart)
  → DURING: Checkpoint every N/10, early stopping rules active
  → AFTER: Log outcome via research-reflect, update cost tracker

User wants to BUILD research foundation (deep reading, RQ, motivation):
  → /research-workflow:research foundation
  → USE if installed: /speed-read or /map-reduce-papers for paper reading; else read papers by hand into the structured notes table
  → USE: /verify-before-write for every statistic extracted (G1 hard) — fallback is the inline manual verification in phase-1-foundation.md:21, not "skip"
  → AFTER: Draft RQs with confirmation/refutation criteria
  → AFTER: Offer /research-workflow:research gate 1

User wants to IMPLEMENT (code, build system):
  → /research-workflow:research implement
  → USE: Design-code alignment check (read design doc, map to code)
  → MUST: Validate evaluation pipeline on known-good AND known-bad inputs
  → AFTER: Code freeze tag + dependency lock + /research-workflow:research gate 4

User wants to HANDLE reviewer feedback (rebuttal, revision):
  → /research-workflow:research rebuttal
  → USE: Worker-Critic pair for response letter (Worker drafts, Critic checks tone+specificity)
  → MUST: Map every reviewer comment to specific paper change
  → AFTER: Cross-section consistency check on revised paper

User wants to PREPARE a presentation (talk, poster, demo):
  → /research-workflow:research present
  → USE: Read phase-9-present.md for structure (hook→method→results→takeaway)
  → MUST: 3 dry runs, pre-record backup for live demos
  → AFTER: Q&A preparation from reviewer feedback

User wants to ESTIMATE costs or time:
  → /research-workflow:research cost
  → USE: Bottom-up formula with retry multipliers (3x first-time, 1.5x familiar)
  → MUST: Include per-model pricing, debug budget (20%)
  → AFTER: Track actual vs estimated

User wants to MANAGE risks:
  → /research-workflow:research risk
  → SHOW: All open risks sorted by severity
  → FOR each accepted_risk: Verify paper defense exists in Threats section
  → AFTER: Update risk status

User wants to ROLL BACK to earlier phase:
  → /research-workflow:research rollback N
  → MUST: Impact analysis first (which artifacts/phases affected?)
  → DECIDE: Fix at source vs patch downstream vs abandon
  → AFTER: Re-run Gate on the fixed phase, propagate changes forward

User wants to EVOLVE the skill:
  → /research-workflow:research evolve
  → READ: phase-evolve.md for full protocol (data sources, two apply paths, Health Score)
  → DECIDE: per-item approve runtime applies (rule promote/retire, route example) vs maintainer-bound bundle proposals (new gate, phase reword, router DEFAULT edit)

User wants to EXTRACT writing patterns:
  → /research-workflow:research mine-patterns
  → READ: phase-writing-memory.md
  → INPUT: Previously accepted paper(s)
  → OUTPUT: .claude/research-writing-memory.md with patterns + structures

User wants to PREPARE for advisor meeting:
  → /research-workflow:research advisor-prep
  → READ: .claude/research-state.yaml for current status
  → SUMMARIZE: What's done since last meeting, what's blocked, what decisions needed
  → HIGHLIGHT: Top-3 risks from Risk Registry
  → PREPARE: 2-3 specific questions for advisor (with your proposed answers)
  → FORMAT: 15-minute meeting structure (5min update + 5min decisions + 5min next steps)

User wants to START a new project:
  → /research-workflow:research init
  → GUIDE: Ask project name, domain, paper type, venue, deadline
  → CREATE: .claude/research-project.local.md, research-state.yaml, findings.md (from templates/)
  → NEXT: Suggest /research-workflow:research explore

User wants to CHECK progress:
  → /research-workflow:research status
  → READ: .claude/research-state.yaml → display phase/gate/artifact/risk/milestone
  → COMPUTE: days_remaining, cost burn rate
  → SUGGEST: highest-priority next action

User mentions DEADLINE pressure or is BEHIND schedule:
  → Show /research-workflow:research status first
  → Then suggest scope cuts or phase acceleration
  → Reference kill conditions from project config

User finishes ANY /research-workflow:research mode:
  → POST-INVOCATION PROTOCOL (mandatory):
    1. Update progress tracker (check off items)
    2. Log outcome (research-reflect log-outcome)
    3. If failure: Log reflection + extract rule
    4. Ask: "这次有什么没覆盖到的？"
    5. If hook missed: Learn new trigger phrase
```

### Quick Pattern Selection Guide

| Situation | Pattern | When |
|-----------|---------|------|
| Writing anything | **Worker-Critic** | Always for creative output |
| Writing with citations | + **CitationAgent** post-processing | Always when \cite{} involved |
| High-stakes artifact (design doc, eval plan, key §) | **G-V-R** (Generator-Verifier-Reviser) | Phase 2, 3, 6 key sections |
| Phase transition | **Adversarial Gate** with 7-dim + loop-back | Always between phases |
| Reviewing paper | **7-dim rubric** + **cross-model** | Phase 7, standalone review |
| Long experiment | **Subagent health monitoring** | N ≥ 100 or parallel agents |
| Literature search | **Semantic Scholar MCP** + **multi-perspective** | Phase 0, novelty-watch |
| Related work | **Citation context analysis** | Phase 6 §7 |
| After acceptance | **mine-patterns** | Extract winning patterns |

### Context-Aware Auto-Suggestions (Cross-Mode Intelligence)

Claude should PROACTIVELY suggest the next action in these situations:

| When you detect... | Auto-suggest... |
|-------------------|----------------|
| No `.claude/research-project.local.md` exists | `/research-workflow:research init` first |
| All Phase 6 sections checked off in progress | `/research-workflow:research review` ("论文写完了，要模拟评审吗？") |
| Gate returns BLOCK + Phase gap > 2 | `/research-workflow:research rollback` ("Phase 5 发现 Phase 2 的问题，要回退吗？") |
| Paper just accepted (user mentions acceptance) | `/research-workflow:research present` + `/research-workflow:research mine-patterns` |
| Paper rejected (user mentions rejection) | `/research-workflow:research rebuttal` (venue pivot analysis) |
| Cost tracker shows >80% budget burned | `/research-workflow:research cost` + scope cut suggestion |
| Phase active >14 days, <50% items done | Nudge: "Phase N 进展缓慢，要 /research-workflow:research status 看看？" |
| User writes §7 Related Work | Auto-activate: Semantic Scholar MCP check + citation context analysis |
| User writes §4/§5 (data sections) | Auto-activate: Claim Provenance Table + verify numbers against results/ |
| User writes §8 Threats | Auto-pull: Risk Registry `accepted_risk` items as candidates |
| Same mode used 3+ times with avg score <3 | Suggest: `/research-workflow:research evolve` ("这个功能效果不太好，要优化吗？") |
| User's message has no research context | Do NOTHING. Don't force research skill on non-research tasks. |

### Outcome-Driven Recipe Optimization

When a mode has 5+ logged outcomes, Claude should check the highest-scoring approach:
```bash
research-reflect query-outcomes --skill <mode> --limit 5
```
If the best approach (score 4-5) used a specific pattern, recommend it:
> "上次用 Worker-Critic 写 §5 效果很好(score=4)，这次也用同样方式？"

