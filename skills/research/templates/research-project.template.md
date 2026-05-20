# Research Project Configuration Template
#
# This is a TEMPLATE. Created by `/research-workflow:research init` from this template using Read+Write into .claude/research-project.local.md (M9 — see SKILL.md `/research init` protocol).
# Fill in project-specific details. Read by `/research-workflow:research` at every invocation.

---
project_name: ""
domain: ""                        # e.g., "Smart Contract Security", "Code Generation", "SE Testing"
paper_type: "systems"             # systems | empirical | survey | benchmark | theory
target_venue: ""                  # e.g., "ASE 2026", "ICSE 2027", "TSE", "TOSEM"
venue_type: "conference"          # conference | journal | workshop
page_limit: 10                    # venue page limit (excluding references)
deadline: ""                      # submission deadline (ISO date, e.g., 2026-09-15)
# Live state (current_phase, phase status, artifacts, risks, decisions) lives in research-state.yaml
budget_usd: 0                     # total API/compute budget for experiments
language: "zh"                    # zh | en — affects post-invocation prompts
autonomy_level: "checkpoint"      # manual | gate-only | checkpoint | full-auto — HITL pause cadence; see SKILL.md Autonomy Policy

# Paths (absolute)
paper_path: ""                    # path to paper directory (LaTeX source)
results_path: ""                  # path to experiment results
codebase_path: ""                 # path to implementation source code
papers_path: ""                   # path to collected reference PDFs

# Research content
rqs:                              # research questions
  - ""                            # RQ1: ...
baselines:                        # baseline methods to compare against
  - ""                            # e.g., "Vanilla GPT-4o", "FSM-SCG (original code)"
key_contributions:                # 1-sentence contribution claims (evolves over phases)
  - ""                            # Contribution 1
ablation_components:              # components to ablate (from Phase 2 traceability table)
  - ""                            # e.g., "SecuritySpec", "KB", "Auditor"

# Domain oracle adapter (R8) — pins this project's evaluation contract so Phase 3 is
# reusable across paper types without generic per-type prose. Read by `/research-workflow:research eval-design`.
domain_adapter:
  claim_type: ""                  # the kind of claim — e.g. "detection accuracy", "speedup", "correctness guarantee", "empirical finding", "taxonomy coverage"
  oracle: ""                      # the CATEGORY of source-of-truth admissible for that claim — human-label / benchmark / machine-checked-proof / inter-rater-coding (the concrete tool goes in evaluation_instruments)
  proxy_metrics: []               # cheap stand-ins watched while iterating — NOT the headline claim
  guardrail_metrics: []           # metrics that must not regress — e.g. "false-positive rate", "compile rate", "cost/run"
  mutable_scope: ""               # what the method may iterate vs what is frozen once the evaluator is registered — see the immutable-evaluator rule in reference/capability-evaluation.md
  evidence_standard: ""           # what counts as sufficient evidence for the claim — e.g. "paired test p<0.05 + effect size, N>=100"

# Evaluation instruments (tools used as evaluation oracles)
evaluation_instruments:
  - name: ""                      # e.g., "Slither", "pytest", "JUnit", "LLM-as-judge"
    type: ""                      # automated_tool | llm_judge | human_label | ground_truth
    known_limitations: ""         # e.g., "FP/FN in reentrancy detection"
    mitigation: ""                # how you address the limitation

# Cost model (per-model pricing for accurate estimates)
model_pricing:
  - model: ""                     # e.g., "gpt-4o"
    input_per_1m: 0               # $/1M input tokens
    output_per_1m: 0              # $/1M output tokens
    pricing_date: ""              # when this pricing was checked

# Contingency plans (from Phase 3)
contingency_plans:
  - result_pattern: ""            # e.g., "All metrics worse than baselines"
    strategy: ""                  # e.g., "Reframe as negative result + analysis of why"

# Kill conditions (when to abandon current approach)
kill_conditions:
  - ""                            # e.g., "Compile rate < 20% after pipeline optimization"

# Collaborators
collaborators:
  - role: "advisor"               # advisor | co-author | reviewer
    name: ""
---

## Project Notes

(Free-form notes, context, decisions, or running observations specific to this project.)
