# Phase 2: Method Design (`/research design`)

> A technical approach that is novel, sound, and implementable — with every decision justified.

## Applies to: systems, empirical, theory, benchmark

**[SURVEY]**: Skip this phase. Proceed from Phase 1 to Phase 6 with systematic review methodology.

## Protocol

### 1. Design Approach
- **Outline first**: TOC + 2-3 sentence summary per section → get user approval → then expand
- Every design decision must cite rationale: literature evidence, empirical data, or principled argument
- Maintain terminology file — new terms defined on first use, no synonyms
- If the project has a terminology file, check consistency with every edit

### 2. Novelty Stress Test (CRITICAL)

Three mandatory tests before this phase can pass Gate:

**Test A — One-Sentence Differentiation**:
> State your method's core novelty in one sentence WITHOUT using generic terms
> ("framework", "pipeline", "multi-agent", "novel", "efficient", "effective").
>
> Bad: "We propose a multi-agent framework for secure code generation."
> Good: "We operationalize 5 official security guidelines into 94 enforceable SOPs
> that govern each agent's decisions at 59 quality checkpoints."

If you can't pass Test A, your novelty isn't clear enough.

**Test B — Reviewer Dismissal Defense**:
> If Reviewer 2 says "This is just X + Y glued together", what's your defense?
> The defense must be TECHNICAL, not rhetorical.
> It must point to a specific design decision that prior work lacks.

**Test C — So-What Test**:
> "If this paper didn't exist, what would the field lose?"
> If the answer is "a slightly better number on benchmark Z", the contribution is weak.

### 3. Design-to-Evaluation Traceability

Build this table NOW (it will drive Phase 3):

| Design Component | Claimed Benefit | How to Prove It | Ablation Config | Metric |
|-----------------|----------------|----------------|-----------------|--------|
| (each major component) | (what it adds) | (experiment) | (remove this) | (measure this) |

Rules:
- Every component must map to ≥1 metric. If it can't be evaluated, question if it should exist.
- Every claimed benefit must have a measurable ablation. No "it obviously helps."
- Components with coupled dependencies: note which ablations are confounded.

### 4. Design Documentation

**[SYSTEMS]**
- Architecture diagram with data flow
- Per-component specification (input/output/algorithm/parameters)
- Interface contracts between components
- Design decisions log with alternatives considered

**[EMPIRICAL]**
- Study design (survey instrument / mining methodology / interview protocol)
- Sampling strategy with justification
- Data collection procedure
- Coding scheme or analysis framework

**[THEORY]**
- Formal problem definition
- Proof strategy outline
- Key lemmas and their roles
- Connection to practical implications

**[BENCHMARK]**
- Benchmark design rationale (what gap it fills)
- Data collection and curation methodology
- Quality assurance process
- Intended usage and limitations

## Emitted Artifact

`Method Design Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Research Question Card` → scores `Method Design Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- A1: One-sentence test PASSES (no generic terms)?
- A2: Reviewer dismissal defense is TECHNICAL and specific?
- B1: Every component maps to ≥1 evaluation metric?
- Traceability table complete with no "obvious" entries?
- All design decisions have documented rationale?
- **Rollback check**: If Phase 5 reveals this design is flawed, what's the escape path?
