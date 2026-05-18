# Phase Rollback Protocol

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

When a later phase reveals an earlier phase's flaw:

### Step 1: Impact Analysis
```
Trigger: "Phase {current} discovered flaw in Phase {target}"

Impact Assessment:
  - Which phases between {target} and {current} are affected?
  - Which artifacts (docs, code, results, paper sections) must change?
  - Is the flaw fixable within {target} or does it require rethinking?
  - Estimated cost of fix vs cost of working around it
```

### Step 2: Decision
| Option | When | Action |
|--------|------|--------|
| **Fix at source** | Flaw is fixable, downstream cost manageable | Roll back, fix, re-gate, propagate changes forward |
| **Patch downstream** | Source fix too costly, workaround exists | Document in Risk Registry, adjust framing |
| **Abandon & pivot** | Flaw is fatal, no workaround | Kill current approach, return to Phase 0/1 with lessons |

### Step 3: Execute
- Log decision in Decision Log with full rationale
- If rolling back: re-run Adversarial Gate on the fixed phase
- Propagate changes forward through each affected phase
- Update Risk Registry with outcome
