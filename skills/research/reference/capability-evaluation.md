# Capability — Evaluation Integrity

> Reference detail for the `research` skill — the canonical statement of the
> cross-cutting evaluation *rules* the Phase 3 protocol and the Adversarial Gate
> enforce. The working matrices live in `phases/phase-3-eval-design.md`. (M3c / R9.)

## Oracle / instrument / contamination — canonical reference

Phase 3 fills three matrices — Oracle Validity (§2), Instrument Validity (§6),
Contamination Assessment (§1b). The rules they operationalize:

- **Oracle types** — `human_label` · `automated_tool` · `llm_judge` · `ground_truth`
  · `self_referential`. An `llm_judge` scoring LLM output is **circular** and needs a
  non-LLM cross-check; a `self_referential` oracle (a system grading itself) is almost
  never acceptable. Every metric names its oracle, the oracle's limitations, a
  mitigation, and whether reviewers at the target venue will accept that oracle.
- **Instrument validity** — any tool used as an evaluation oracle has a known
  false-positive / false-negative rate and finite coverage. Quantify both; a claim may
  not exceed what the instrument can actually detect.
- **Contamination** — when the method or a baseline uses an LLM, the evaluation data
  may already be in that model's training set. Assess overlap risk and mitigate it
  before any score is trusted (full audit below).

## Immutable evaluator rule

An evaluator is **registered** when the Phase-3 `Evaluation Design Spec` artifact
reaches lifecycle status `accepted`. Registration freezes, for every run that reports
against it: the evaluator / scoring script (path + version or hash), the dataset split
(id or hash), the metric definitions, the preprocessing and exclusion rules, and — for
an `llm_judge` oracle — the judge model + version + prompt. Once registered, all of
these are **immutable for that run**.

Editing the scorer, re-carving train/test, or swapping the metric *after results exist*
is reward-hacking surface — it lets a number move because the ruler changed, not the
method. Exploratory and debug runs *before* registration are non-claimable and may
iterate the evaluator freely; *after* registration, inspecting a result and then
changing the evaluator is itself a revision and must be logged.

A change is allowed only as an explicit, logged **eval-design revision**:
1. a **Decision Log** entry (`research-state.yaml`) — what changed, why, and which
   existing results it invalidates;
2. if any results already depend on the old evaluator, a **Phase Rollback**
   (`reference/rollback.md`) to re-run them under the revised design.

Never silently rewrite the evaluator to make a result look better. (Source:
buildoak/tennis-xgboost-autoresearch reward-hacking writeup — validation-carving that
slid into evaluator rewriting; §10-confirmed.)

## Leakage / contamination audit (mandatory for LLM-assisted research)

Any research where an LLM sits in the **method** OR the **evaluation** MUST clear this
audit before its results are trusted. Each row is a yes/no determination; an
unresolved or unknown item is logged to `.claude/GAP_REPORT.md` (R7) and blocks the
dependent result claim.

| Check | What it asks | Problem signal |
|-------|--------------|----------------|
| Literature overlap | Is the test set public and dated before the model's training cutoff? | public + pre-cutoff → plausible overlap |
| Benchmark memorization | Is the benchmark old and widely published? | perfect on common items, weak on rare ones |
| Visible-holdout contamination | Did the holdout leak via prompts, few-shot examples, or earlier iterations this session? | the holdout was ever shown to the model |
| Self-referential judging | Does the same model (or family) appear as both subject and judge? | method model == judge model |

Mitigations (apply ≥1 per open item): post-cutoff or freshly constructed data; canary /
membership-inference probes; performance-vs-rarity analysis; a non-LLM cross-check for
any `llm_judge` oracle. Phase 3 §1b records the per-dataset outcome in its Contamination
Assessment table.
