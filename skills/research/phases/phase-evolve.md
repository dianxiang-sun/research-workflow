# Skill Evolution Protocol (`/research evolve`)

> Analyze accumulated reflection data to improve routing, rules, and gate questions over time.

## Applies to: ALL paper types (meta-protocol)

## Protocol

### 1. Data Collection
- Run `reflect.py stats` to get aggregate metrics: total invocations, outcome distribution, rule hit rates, mode usage frequency
- Run `reflect.py export-summary` to get a structured dump of all reflections with outcomes
- If either command fails or returns empty data, stop — there is nothing to evolve yet
- Record the current date and invocation count as the evolution baseline

### 2. Pattern Analysis

#### 2a. Rule Promotion (soft -> hard)
- Query all **soft rules** tested >=5 times with confidence >=0.7
- For each candidate:
  - Verify the confidence is not inflated by a single repeated scenario
  - Check that the rule has been tested across >=2 distinct phases (not just one context)
  - If both hold: propose promotion to hard rule
  - If only frequency holds: flag as "strong soft rule, monitor for one more cycle"

#### 2b. Rule Retirement
- Query all rules tested >=5 times with confidence <=0.3
- For each candidate:
  - Distinguish "wrong rule" (consistently bad advice) from "rarely triggered" (few test opportunities)
  - Wrong rules: propose retirement with replacement suggestion if pattern exists
  - Rarely triggered: propose rewording the trigger condition, not retirement

#### 2c. Dead Mode Analysis
- Identify modes with 0 uses since last evolution (or ever)
- For each unused mode:
  - Check if its trigger keywords overlap with a more popular mode (cannibalized?)
  - Check if the use case genuinely arises in this project type
  - Propose one of: reword triggers, merge into another mode, archive with rationale

#### 2d. New Gate Question Discovery
- Scan reflections for recurring failure patterns (same root cause >=3 times)
- For each pattern:
  - Formulate a gate question that would have caught the issue earlier
  - Identify which phase's gate criteria should include it
  - Draft the question in the same style as existing gates (yes/no, specific, testable)

#### 2e. Route Example Expansion
- Scan reflections for keywords the user typed when the semantic router missed
- For each missed route:
  - Add the user's phrasing as a new example in the route definition
  - Verify the new example does not create ambiguity with other routes

### 3. Proposal Generation
For each identified improvement, produce a structured proposal:

| # | Type | Target File | Change | Justification |
|---|------|-------------|--------|---------------|
| 1 | promote | `phases/phase-X.md` | Move rule R from soft to hard | Confidence 0.85 over 12 trials (sessions S3-S14) |
| 2 | retire | `phases/phase-Y.md` | Remove rule R, replace with R' | Confidence 0.15 over 8 trials, consistently misleading |
| 3 | new-gate | `phases/phase-Z.md` | Add gate: "Have you verified X?" | Same failure in reflections R4, R7, R11 |
| 4 | reword | `tools/semantic_router.py` | Add example "XYZ" to mode M | Missed in sessions S5, S8 |

- Every proposal must cite specific reflection IDs or session numbers as evidence
- Never propose changes based on fewer than 3 data points

### 4. User Review
- Present proposals as a numbered list grouped by type (promote / retire / new-gate / reword / archive)
- For each proposal, show: the change, the evidence, and the risk if rejected
- User approves, rejects, or modifies each individually
- Rejected proposals are logged with reason (they may resurface in future evolutions)

### 5. Application
- Apply approved changes to the target files
- For each applied change, append an entry to `evolution.md`:
  ```
  ## Evolution [DATE]
  - [TYPE] [TARGET]: [DESCRIPTION] (evidence: [REFS]) — approved by user
  ```
- Commit changes with prefix `research: evolve — [summary of changes]`

### 6. Verification
- Run the § Budget & Structure Check (G8) — the wc -l trend, the 5-check structural sweep, the dispatcher-shape check
- Run `semantic_router.py rebuild-index` to update route embeddings
- Run `reflect.py stats` again to confirm the tool still works after edits
- Verify no existing phase file has broken markdown (headers, tables, gate criteria)
- Run a smoke test: pick one recent reflection and confirm it would still route correctly

## Health Score

Compute after data collection to guide evolution frequency:

```
Score = (hard_rules x 3 + soft_rules x 1 + logged_outcomes x 0.5) / max(total_invocations, 1)
```

| Score Range | Maturity | Recommended Cadence |
|-------------|----------|---------------------|
| < 1.0 | Cold start | Keep using the skill; evolve after 20+ invocations |
| 1.0 - 3.0 | Learning | Evolve monthly |
| > 3.0 | Mature | Evolve quarterly |

Report the health score at the start of every evolution run so the user knows whether evolution is premature.

## Budget & Structure Check (G8)

Run by `/research evolve` (and, during the restructure, by each migration phase) — the
standing enforcement of Global Rule **G8**. NOT a CI job and NOT new tooling: the same
kind of mechanical check the skill already does.

### Mechanical hook

1. **`wc -l` trend** — count the skill's `*.md` + `templates/research-state.yaml`;
   report the delta + cumulative vs the 3143 baseline. Reported for visibility — a
   positive delta is NOT a reject reason (§15).
2. **Structural sweep — 5 checks, each pass/fail:**
   1. every router-table mode in `SKILL.md` resolves to a phase / capability;
   2. every gated `phases/` file (all but `phase-writing-memory.md`, which has no gate)
      has an `## Emitted Artifact` section and a `## Gate Criteria` whose first line is
      a `> **Rubric contract** —` header naming input · emitted artifact · verdict;
   3. no live cross-reference points to an M2-retired file — `phase-progress-tracker.md`
      or the flat `research-progress` / `research-risks` / `research-decisions` files —
      except the sanctioned `SKILL.md` one-release fallback, `capability-artifacts.md`,
      and this G8 spec naming them;
   4. the Phase-3 mandatory-question count is identical in every file that states it;
   5. the skill loads — frontmatter intact, `research-state.yaml` parses, `/research status` dispatches.
3. **Dispatcher-shape check** — `wc -l SKILL.md` ≤ ~400, and no fenced code block in
   `SKILL.md` exceeds ~15 lines.

Concrete read-only checks:
- rubric headers — `grep -LF '**Rubric contract**' phases/phase-*.md` lists any gated
  phase missing the header (only `phase-writing-memory.md` is expected).
- retired-file pointers — `grep -rl 'phase-progress-tracker\|research-progress\|research-risks\|research-decisions' --include='*.md' . | grep -vE 'phase-evolve|SKILL|capability-artifacts'` must be empty (the G8 spec, the `SKILL.md` one-release fallback, and `capability-artifacts.md` legitimately name these retired tokens; any other hit is a dangling pointer).
- Phase-3 count — `grep -rhoE 'MANDATORY 1[0-9]' --include='*.md' .` must read "12" everywhere.
- dispatcher-shape — `wc -l SKILL.md`, then scan `SKILL.md` for a code-fence pair more than ~15 lines apart.

### Budget & Structure checklist (required artifact)

Every `/research evolve` change proposal (and every restructure migration-phase
proposal) MUST carry: (a) the `wc -l` delta + cumulative trend; (b) each new
`reference/`/`templates/` file's D-diagnosis / R-item justification; (c) each change
classified — *relocation* (names its paired delete) or *net-new gap-fill* (names the
D/R item); (d) a DRY / pointer audit.

G8 **REJECTS** a proposal that omits the checklist, or that fails the structural sweep
or the dispatcher-shape check — **never** on a positive line-count delta alone. The
checklist's *presence* is mechanical; its *content* is the judgement reviewed at the
APPLY gate.

## Emitted Artifact

`Evolution Log entry` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `accumulated reflection / outcome data` → scores `Evolution Log entry`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- Do you have >=20 logged invocations to analyze? (If not, evolution is premature)
- Has it been >=2 weeks since the last evolution? (Avoid thrashing)
- Did every proposal cite >=3 data points as evidence?
- Did the user explicitly approve each applied change?
- Does `semantic_router.py rebuild-index` complete without errors after changes?
