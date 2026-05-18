# Phase 2.5: Feasibility Pilot

> A small, cheap validation that your method WORKS before committing to full evaluation design.
> Run after Phase 2 (design), before Phase 3 (eval-design).

## When to Run

ALWAYS, unless your method is purely theoretical. Even 5 examples save months.

## Comparative Pilot (advisory — DD5)

Beyond validating one already-chosen method, a pilot may also help SELECT among the
2-3 surviving candidate directions from Phase 0's Converge step: run the same cheap,
informative pilot on each and let the empirical signal *inform* the choice.

Scoped — advisory only: does NOT apply to theory or survey directions, nor to any idea
whose signal is literature / evidence rather than a runnable pilot; it never becomes a
required candidate-ranking mechanism, and the signal informs, never numerically ranks.

## Protocol

### 1. Select Pilot Samples
- Pick 5-10 representative inputs from your target domain
- Include at least: 1 easy, 2 medium, 2 hard
- If possible, pick examples where you know the expected output

### 2. Run Your Method
- Apply your method (even if partially implemented) to the pilot samples
- Manual/hacky execution is fine — this is about FEASIBILITY, not scale

### 3. Manual Inspection
- For each output: Is it reasonable? Is it what you expected?
- Identify failure modes: WHERE does the method break? WHY?
- Estimate rough success rate (if 0/5 work, your method has fundamental issues)

### 4. Feasibility Decision

| Pilot Result | Decision |
|-------------|----------|
| 4-5/5 reasonable | PROCEED to Phase 3 with confidence |
| 2-3/5 reasonable | PROCEED but note weaknesses, plan mitigation in eval design |
| 0-1/5 reasonable | STOP. Return to Phase 2. Redesign before investing in eval. |

### 5. Document
- Pilot results feed into Phase 3 cost estimation (extrapolate from pilot costs)
- Failure modes feed into contingency planning
- Success examples can become motivating examples in the paper

## Emitted Artifact

`Feasibility Pilot Report` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Method Design Record` → scores `Feasibility Pilot Report`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- At least 5 representative inputs tested?
- Manual inspection done (not just automated metrics)?
- Failure modes identified and documented?
- Decision to proceed is justified by pilot data (not hope)?
