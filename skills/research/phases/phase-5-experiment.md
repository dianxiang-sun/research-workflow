# Phase 5: Experiment Execution (`/research experiment`)

> Fair, reproducible experiments with honest analysis and real-time monitoring.

## Applies to: systems, empirical, benchmark
**[SURVEY]**: Replace with "Systematic Review Execution." **[THEORY]**: Replace with "Proof Development."

## Protocol

### 1. Pre-Experiment Checklist

**MUST complete ALL before starting experiments:**

- [ ] Code frozen: tagged commit, dependency lock, environment recorded
- [ ] All baselines use original authors' code (or justified reimplementation validated against their numbers)
- [ ] Cost estimate reviewed, budget approved, payment method confirmed
- [ ] Contingency plans in place for each result pattern (from Phase 3)
- [ ] Evaluation instrument validity matrix reviewed (from Phase 3)
- [ ] Statistical analysis plan chosen pre-hoc (from Phase 3)
- [ ] Monitoring plan active (checkpoints, early stopping, anomaly alerts)
- [ ] Results directory structure created (per experiment type, append-only)
- [ ] Config files for each experiment saved (reproducibility)

### 2. Execution Monitoring

**For long-running experiments (N ≥ 100):**

| Checkpoint | Action | Threshold |
|-----------|--------|-----------|
| Every N/10 samples | Compute running metrics, compare to expectations | — |
| First 10 samples | Sanity check: are outputs reasonable? | If all fail → STOP and debug |
| First 10% complete | Compare to rough expectations | Compile rate < 10% → STOP |
| Cost per sample | Track rolling average | > 5× average → investigate |
| Error rate | Track API errors, timeouts | > 20% error → pause and check |
| 50% complete | Full interim analysis | Radically unexpected → pause |
| 100% complete | Full analysis + cost reconciliation | — |

### Subagent Health Monitoring (for parallel experiments)

When running multiple experiments via parallel agents (inspired by altmbr/claude-research-skill):

**Escalating health check protocol**:
- First 30 seconds: Check every 30s (catch immediate failures)
- 30s - 5min: Check every 2min
- After 5min: Check every 5min

**Stuck detection**: If an agent's output file line count hasn't changed between two checks, the agent is stuck.

**Auto-recovery**: Stuck agent → kill → relaunch with:
1. Same config
2. Append to prompt: "Previous attempt stalled at: [last output]. Continue from there."
3. Max 2 auto-relaunches before escalating to user

**Pre-created output files**: Before launching parallel agents, create output files with section headers.
This makes progress monitoring trivial (just count lines) and gives agents structure.

**Early stopping rules** (decide BEFORE, not during):
- Catastrophic failure: < X% success in first 10% → stop, debug, restart
- Budget breach: Actual cost tracking to exceed budget by >100% → stop, replan
- API instability: >5 consecutive failures → pause, retry after cooldown

**Logging requirements** (per run):
```
{
  "experiment_id": "...",
  "git_tag": "v...",
  "timestamp": "ISO8601",
  "config": { ... },
  "environment": { "python": "...", "model": "...", "dependencies": { ... } },
  "cost_actual": 0.0,
  "duration_seconds": 0,
  "errors": [ ... ]
}
```

### 3. Results Management

**Append-only rule**: NEVER overwrite results. New run = new timestamped directory.
```
results/
├── main/
│   ├── 2026-03-20T14-30-00_method_n1000/
│   └── 2026-03-21T09-15-00_method_n1000_rerun/   ← rerun, don't overwrite
├── baselines/
│   ├── vanilla_gpt4o_n1000/
│   └── fsmscg_n1000/
├── ablation/
│   ├── no_kb_n300/
│   └── no_auditor_n300/
└── analysis/
    └── comparative_2026-03-22/
```

Each experiment directory MUST contain:
- `config.json` — exact configuration
- `metadata.json` — git tag, timestamp, environment hash, cost
- `metrics.json` — computed metrics
- Raw outputs (if < 50MB; otherwise external storage with pointer)

### 4. Post-Experiment Analysis

**Step 1: Descriptive statistics**
- Per-metric: mean, median, std, min, max, distribution shape
- Per-baseline comparison: absolute and relative differences
- Visualize distributions (not just means)

**Step 2: Statistical testing** (following pre-registered plan from Phase 3)
- Run planned tests (paired/unpaired, parametric/non-parametric)
- Apply multiple comparison correction if comparing k > 2 methods
- Report: test statistic, p-value, effect size, confidence interval
- If single-system (no variance): report descriptive only, explicitly note

**Step 3: Cost-effectiveness analysis**
- Improvement per dollar: (metric_improvement / cost_ratio)
- Is the cost-effectiveness acceptable for the claimed contribution?
- Would a practitioner pay this cost for this improvement?

**Step 4: Failure analysis** (often more insightful than success analysis)
- Categorize failures: WHY did each failure fail?
- Taxonomy: input difficulty? method limitation? tool error? oracle error?
- Which failures are systematic (design flaw) vs random (noise)?
- Implications for method improvement (future work fodder)

**Step 5: Claim-Evidence reconciliation**
- For each planned claim/RQ: Does the evidence support it?
- Scope check: Does the evidence's scope match the claim's scope?
- If evidence is weaker than expected: adjust claims DOWN, don't inflate narrative

### 5. Honest Reporting Obligations

- Report ALL results including negative/unexpected ones
- If a baseline was dropped: explain WHY (not just silently removed)
- If experiments were re-run: report ALL runs, explain which you report and why
- If parameters were tuned: report the tuning process, not just final numbers
- Cost transparency: Report actual costs for each experiment

**[EMPIRICAL]**: Inter-rater reliability scores. Response rates. Demographic breakdown. Non-response bias analysis.

## Emitted Artifact

`Experiment Results Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Evaluation Design Spec + Implementation Record` → scores `Experiment Results Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- Results answer the RQs? (not adjacent questions)
- Negative results honestly reported?
- Statistical tests follow pre-registered plan? (no p-hacking)
- Cost-effectiveness acceptable for claimed contribution?
- Failure analysis provides genuine insight? (not just "it didn't work")
- Can someone reproduce with the metadata you logged?
- Claim scope ≤ evidence scope for every planned claim?
