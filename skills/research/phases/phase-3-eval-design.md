# Phase 3: Evaluation Design (`/research eval-design`)

> An evaluation plan that convincingly answers your RQs — designed to withstand the harshest scrutiny.

> **THIS IS THE HIGHEST-ROI GATE.** Flaws discovered here cost 1x to fix.
> The same flaws discovered in Phase 7 cost 100x or are unfixable.

## Applies to: systems, empirical, benchmark
**[SURVEY]**: Skip. **[THEORY]**: Replace with proof validation strategy.

## Protocol

> **Read the project's `domain_adapter` block first** (`.claude/research-project.local.md`,
> R8) — it pins this project's claim type, oracle category, proxy / guardrail metrics,
> mutable scope, and evidence standard; the Oracle, Instrument, and Contamination
> matrices below instantiate it for the concrete tools and datasets. If the project
> predates M4a and has no `domain_adapter` block, derive a provisional one from
> `paper_type` + the RQs + planned metrics + `evaluation_instruments`, and offer to
> persist it to `research-project.local.md`.

### 1. Dataset Selection

**Task-Dataset Alignment Check** (MUST pass before proceeding):
```
Your method's input:  _____________
Your method's output: _____________
Dataset's input:      _____________
Dataset's output:     _____________
EXACT match?          YES / NO (explain gap)
```

If mismatch:
- Document it explicitly with impact assessment
- Can you pre/post-process to bridge the gap without introducing bias?
- If not, is there a better dataset? Or must you construct one?

**Dataset Quality Audit**:
- Label noise: How were labels created? Human? Automated? What's the error rate?
- Data leakage: Any overlap between train/test? Between your KB and test data?
- Size: Is N sufficient for statistical significance at your expected effect size?
- Representativeness: Does the sample reflect the population you'll claim generalization over?
- Licensing: Can you legally use and redistribute this data?

**[EMPIRICAL]**: Replace with "Study Population" — sampling frame, recruitment, representativeness, IRB/ethics.

### 1b. Benchmark Contamination / Training Data Leakage (CRITICAL for LLM-based methods)

If your method OR baselines use an LLM, assess contamination risk:

**Contamination Assessment Table**:
| Dataset | Creation Date | LLM Training Cutoff | Overlap Risk | Mitigation |
|---------|-------------|---------------------|-------------|------------|
| (fill) | (fill) | (fill) | High/Medium/Low | (fill) |

**Risk indicators**:
- Dataset is widely cited and publicly available → HIGH risk (likely in training data)
- Dataset uses well-known benchmarks (HumanEval, SWC-registry, SmartBugs) → HIGH risk
- Dataset created AFTER LLM training cutoff → LOW risk
- Dataset is proprietary or newly constructed → LOW risk

**Mitigation options** (use ≥1):
- Use post-training-cutoff data exclusively
- Construct new dataset from fresh sources
- Run canary/membership inference tests
- Analyze performance vs data rarity (if LLM scores perfectly on common items but poorly on rare ones → contamination signal)
- Compare LLM performance on dataset vs novel hand-crafted inputs

**[DOMAIN:security]** Additional: Common security benchmarks (SWC-registry, SmartBugs, Ethernaut, Damn Vulnerable DeFi) are almost certainly in LLM training data. Use post-2024 real-world contracts or construct synthetic vulnerabilities.

**Red flag**: If you cannot demonstrate that your evaluation dataset is NOT in the LLM's training data, reviewers WILL challenge your results. Address this proactively.

→ Beyond this table: run the full **leakage / contamination audit** (literature overlap · benchmark memorization · visible-holdout leakage · self-referential judging) and apply the **immutable-evaluator rule** — **`reference/capability-evaluation.md`**.

### 2. Metric Design

For EACH metric, fill this row:

| Metric | Math Definition | What It Measures | What It DOESN'T Measure | Edge Cases | Oracle Source |
|--------|----------------|-----------------|------------------------|------------|-------------|

**Edge cases that MUST be defined**:
- Zero denominator (no tests → Pass@1 = ?)
- Partial success (3/5 tests pass → binary or proportional?)
- Skipped/errored items (count as failure? exclude from denominator?)
- Ties (two methods score identically → how to rank?)

**[DOMAIN:security] Common security evaluation metrics and pitfalls**:
| Metric | What It Measures | Common Pitfall |
|--------|-----------------|----------------|
| Detection Rate (Recall) | % of real vulnerabilities found | Meaningless without FPR — a tool that flags everything has 100% recall |
| False Positive Rate | % of flagged items that are not real vulnerabilities | Must report alongside recall; high FPR makes tools unusable |
| Precision | % of flagged items that are real vulnerabilities | Depends on base rate — 90% precision is poor if 99% of code is safe |
| Per-CWE/OWASP category | Breakdown by vulnerability type | Aggregate metrics hide that tool may excel on type A but fail on type B |
| Time-to-detect | How quickly vulnerabilities are found | Relevant for CI/CD integration claims |
| VRS (Vulnerability Risk Score) | Weighted severity of findings | Must define weights explicitly and justify them |
| ZRCP (Zero Risk Contract Proportion) | % of outputs with zero vulnerabilities | Must account for tool FP/FN — "zero findings" ≠ "zero vulnerabilities" |

**Oracle Validity Matrix** (CRITICAL — fill for every metric):

| Metric | Oracle Source | Oracle Type | Known FP Rate | Known FN Rate | Coverage | Mitigation | Residual Risk |
|--------|-------------|------------|---------------|---------------|----------|------------|---------------|

Oracle types: `human_label` | `automated_tool` | `llm_judge` | `ground_truth` | `self_referential`

Red flags:
- `llm_judge` evaluating LLM output → **circularity** → must have non-LLM cross-validation
- `automated_tool` with known FP/FN → must quantify impact on your metrics
- `self_referential` (your system judges itself) → almost never acceptable

**Scalability dimension** (if your method processes inputs of varying size/complexity):
- Include a scalability sub-experiment: test at 1x, 2x, 5x normal scale
- Report: Does performance degrade? Does cost scale linearly or worse?
- If method is O(n²) or worse, acknowledge and discuss practical limits
- **[DOMAIN:security]**: Test on contracts of varying LOC (100, 500, 1000, 5000 lines)
- **[DOMAIN:se]**: Test on projects of varying size (small/medium/large from dataset)

### 3. Baseline Selection

**Fairness Audit Table**:

| Baseline | Our Method | Fair? |
|----------|-----------|-------|
| Budget: $X per contract | Budget: $Y per contract | If Y >> X, what's the cost-adjusted comparison? |
| Knowledge: none | Knowledge: KB with N entries | Give baseline same KB? Or acknowledge in Threats? |
| Iterations: 1 pass | Iterations: k attempts | Give baseline k attempts too? |
| Model: GPT-4o | Model: GPT-4o | Same model? If different, confounded. |

Rules:
- MUST use original authors' code when available. Reimplementation introduces silent differences.
- If original code unavailable: document reimplementation, validate on their reported numbers.
- **Cost-adjusted comparison**: If your method costs 10x more, show what baseline achieves with 10x budget.

### 4. Ablation Design

From Phase 2's traceability table, derive ablation configs:

| Config | What's Removed | Expected Effect | Isolation Clean? | Confound Risk |
|--------|---------------|----------------|-----------------|---------------|

**Isolation check**: Removing component A also removes A's output to B → B degrades → you can't tell if it's A or B's contribution. If isolation isn't clean, acknowledge it.

### 5. Statistical Analysis Plan

Decide BEFORE running experiments (not post-hoc):

| Question | Method |
|----------|--------|
| Is method A better than B? | Paired t-test (parametric) or Wilcoxon signed-rank (non-parametric) |
| Multiple comparisons (k baselines) | Bonferroni or Holm correction |
| Effect size | Cohen's d (parametric) or Cliff's delta (non-parametric) |
| How many samples needed? | Power analysis: α=0.05, β=0.80, expected effect size → minimum N |
| Single system, no variance? | Report descriptive stats only; do NOT claim "significant" |
| Non-normal distribution? | Shapiro-Wilk test → choose non-parametric if p < 0.05 |

**Key rule**: "Statistically significant" ≠ "practically significant". Always report effect size alongside p-value.

**Single-run methods** (like your pipeline): Cannot compute variance from one run. Options:
- Run multiple trials with different random seeds / temperature
- Bootstrap confidence intervals from per-sample results
- Report descriptive statistics and explicitly note: "significance testing not applicable for single-system evaluation"

### 6. Evaluation Instrument Validity

For every tool used as an evaluation oracle:

| Tool | What it detects | What it MISSES | Known precision | Known recall | Your mitigation |
|------|----------------|----------------|-----------------|--------------|-----------------|

**Meta-validity question**: "If this tool gives your method a good score, what ALTERNATIVE explanations exist besides 'your method is genuinely better'?"
- Tool has blind spots your method accidentally avoids?
- Tool rewards superficial patterns your method produces?
- Tool's coverage doesn't match your claim scope?

### 6b. Adversarial Evaluation Design

If your method is a detection/analysis/generation tool, evaluate against ADVERSARIAL inputs:

**Standard evaluation**: Benchmark inputs (cooperative, representative)
**Adversarial evaluation**: Inputs specifically designed to fool your method

| Adversarial Type | How to Construct | Expected Impact |
|-----------------|-----------------|-----------------|
| Obfuscated inputs | Apply known obfuscation techniques to benchmark inputs | Measures robustness |
| Novel patterns | Create inputs with patterns NOT in training data or KB | Measures generalization |
| Edge cases | Boundary conditions, unusual combinations | Measures coverage |
| Evasion attempts | Deliberately craft inputs to bypass detection | Measures security |

**[DOMAIN:security]**: This is MANDATORY for security tool papers. Test against:
- Obfuscated vulnerable code (renamed variables, restructured logic)
- Novel vulnerability patterns not in any known dataset
- Deliberately crafted evasion attempts targeting your detection method
- Cross-contract vulnerabilities that span multiple files

**[DOMAIN:se]**: Recommended for tool papers. Test against:
- Adversarial code that mimics patterns your tool looks for but is actually correct
- Edge cases at language feature boundaries

### 7. Resource Planning

**Cost estimation** (per `/research cost` protocol):
```
Method:    [per-run cost] × N × trials = ___
Baseline1: [per-run cost] × N × trials = ___
...
Ablation1: [per-run cost] × N × trials = ___
...
Subtotal: ___
× retry_multiplier (first-time=3.0, familiar=1.5): ___
+ debug_budget (20%): ___
TOTAL: ___
```

**Contingency planning** (BEFORE experiments):
| Result Pattern | Interpretation | Publication Strategy |
|---------------|---------------|---------------------|
| All metrics better | Strong result | Standard framing |
| Mixed (some better, some worse) | Trade-off | Reframe as analysis of trade-offs |
| Marginal improvement | Weak result | Emphasize qualitative analysis, insights |
| Worse than baselines | Negative result | Negative result paper? Or pivot? |
| Ablation shows component X doesn't help | Design flaw | Remove X, simplify method, rerun |

**Kill condition**: Define explicitly: "If ___ happens, we abandon this approach." Having this BEFORE experiments prevents sunk cost fallacy.

### 8. Experiment Monitoring Plan

For long-running experiments (N ≥ 100):
- **Checkpoint frequency**: Every N/10 samples, compute running metrics
- **Early stopping**: If first 10% shows catastrophic failure (e.g., 0% compile rate), investigate before continuing
- **Anomaly alerts**: Per-sample cost > 5× average → flag and investigate
- **Progress tracking**: Estimated completion time, actual vs projected cost curve

## Emitted Artifact

`Evaluation Design Spec` — required fields & provenance: `reference/capability-artifacts.md`.

### Note: Registered Reports [DOMAIN:se]

If your target venue accepts registered reports (EMSE, some TSE tracks):
- Phase 3 output IS essentially a Stage 1 registered report
- Submission guarantees publication regardless of results if the plan is sound
- This eliminates publication bias and rewards good methodology over good results
- Consider this option especially for large-scale empirical studies with uncertain outcomes

## Gate Criteria — MANDATORY 12 QUESTIONS

> **Rubric contract** — input `Method Design Record` → scores `Evaluation Design Spec`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the 12 mandatory questions below; A–H matrix `reference/gate-matrix.md`.

**MUST answer ALL before proceeding to Phase 4:**

1. **Task Alignment**: Dataset task EXACTLY matches method input→output?
2. **Oracle Chain**: Every metric has oracle + limitations + mitigation?
3. **Circularity**: No unmitigated LLM-evaluates-LLM?
4. **Baseline Fairness**: Same budget/knowledge/iterations → results change how?
5. **Ablation Isolation**: Each config isolates ONE component? Confounds documented?
6. **Negative Plan**: Contingency for each result pattern? Kill condition defined?
7. **Instrument Validity**: Each tool's FP/FN and coverage assessed?
8. **Cost Reality**: Total including failures/debug within budget?
9. **Claim-Evidence Boundary**: Each claim's scope ≤ evidence scope?
10. **Statistical Plan**: Tests chosen pre-hoc? Power adequate? Multiple comparison corrected?
11. **Contamination**: If using LLMs — is evaluation data potentially in training data? Mitigation?
12. **Adversarial**: For tool/detection papers — tested against adversarial inputs? Robustness assessed?
