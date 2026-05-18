# Phase 4: Engineering Implementation (`/research implement`)

> Working code that faithfully implements the design, with tests proving alignment.

## Applies to: systems (primary), benchmark (data pipeline)
**[EMPIRICAL]**: Replace with "Data Collection & Analysis Setup" — instruments, coding schemes, analysis scripts.
**[SURVEY/THEORY]**: Skip.

## Protocol

### 1. Design-Code Alignment

**Before coding**: Create mapping document:

| Design Component (§ ref) | Code Module | Interface | Test File |
|--------------------------|-------------|-----------|-----------|

**During coding**: Flag any deviation from design. Deviation is NOT forbidden but MUST be:
- Documented with reason
- Reflected back to design doc (update or note discrepancy)
- Checked: does this affect the ablation plan? the evaluation plan?

**After coding**: Re-verify mapping. Design drift is the #1 cause of "paper doesn't match code."

### 2. Test Discipline

| Test Level | What to Test | Priority |
|-----------|-------------|----------|
| Unit | Each component in isolation | HIGH — every key function |
| Integration | Component interactions | HIGH — data flow between phases |
| Evaluation pipeline | Scoring a known-good and known-bad input | CRITICAL — if evaluation is wrong, all results are wrong |
| Regression | All of the above, run after every change | MANDATORY |

**Critical**: Test your evaluation pipeline BEFORE running experiments.
- Score a manually-verified "perfect" input → does it get perfect scores?
- Score a known-bad input → does it get appropriately bad scores?
- If evaluation scoring is buggy, you'll discover it after 1000 runs instead of before.

### 3. Code Freeze Protocol

Before any experiment:
- [ ] Tag the exact commit: `git tag v{X}-pre-eval`
- [ ] Lock ALL dependencies to exact versions (pip freeze, package-lock, etc.)
- [ ] Record environment: OS, Python version, tool versions, API model versions
- [ ] Run full test suite — ALL pass
- [ ] NO code changes after this tag. Period. If you find a bug:
  - Fix it, create NEW tag, re-run ALL experiments from scratch
  - NEVER mix results from different code versions

### 4. [EMPIRICAL] Data Collection Setup
- Validate survey instrument with pilot (≥5 participants)
- Set up coding scheme with inter-rater agreement protocol
- Prepare analysis scripts with synthetic test data
- IRB approval documented

### 5. [BENCHMARK] Data Pipeline
- Automated data collection with provenance tracking
- Quality filters with documented thresholds
- Deduplication strategy
- Train/test split methodology (if applicable)
- Validate a random subset manually

## Emitted Artifact

`Implementation Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Method Design + Evaluation Design Spec` → scores `Implementation Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- Code tagged and dependency-locked?
- Full test suite passes?
- Design-code alignment verified (no undocumented drift)?
- Evaluation pipeline validated on known inputs?
- [EMPIRICAL] Pilot study completed? IRB approved?
- [BENCHMARK] Manual subset validation done?
