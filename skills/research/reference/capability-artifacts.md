# Capability — Typed Artifacts & Project State

> Reference detail for the `research` skill. `SKILL.md` and the phase files point
> here and do not restate these schemas. Introduced in the M2 restructure (R2 + R4).

## Project state tree

Each research project keeps, under its `.claude/` directory:

```
.claude/
  research-project.local.md   static config — name, domain, paper type, venue, RQs, budget
  research-state.yaml         typed live state — phases, artifacts, risks, decisions, milestones
  findings.md                 outer-loop narrative memory — Understanding/Patterns/Lessons/Open Qs
  literature/                 reading notes, gap matrix             (Phases 0-1)
  experiments/<slug>/         protocol.md · results/ · analysis.md  (Phase 5)
  paper/                      manuscript sources                    (Phase 6+)
  GAP_REPORT.md               open evidence gaps (R7) — created on demand
```

`/research init` copies `research-state.yaml` and `findings.md` from the skill's
`templates/`. The `literature/`, `experiments/`, `paper/` directories are created
by the phases that first need them.

## Lifecycle status

Every artifact in `research-state.yaml` carries a status: **`draft`** (being produced,
ungated) → **`reviewed`** (passed an Adversarial Gate or critique loop) → **`accepted`**
(gate PASS — downstream phases may build on it) → **`superseded`** (replaced after a
rollback/pivot; kept for provenance). Status is advisory metadata, **not** a state
machine — any mode stays callable in any order and phase ORDER is never enforced
(cross-review C1).

## Artifact contracts

Each phase emits ONE primary typed artifact; its phase file points here for the
required fields rather than restating them.

| Phase | Emitted artifact | Required fields | Provenance |
|-------|------------------|-----------------|------------|
| 0 explore | Research Direction Card | see schema below | literature scan + gap matrix |
| 1 foundation | Research Question Card | see schema below | deep-reading notes |
| 2 design | Method Design Record | design rationale · novelty defense (Tests A/B/C) · design→eval traceability | Phase 1 RQ Card |
| 2.5 pilot | Feasibility Pilot Report | setup · 5-10-example result · go / no-go call | pilot run logs |
| 3 eval-design | Evaluation Design Spec | datasets · metrics + oracle · baselines · ablation · stat plan · contingencies · kill conditions · cost | Phase 2 Design Record |
| 4 implement | Implementation Record | design-code alignment · tests · code-freeze tag · pipeline validation | Phase 2/3 specs |
| 5 experiment | Experiment Results Record | raw results · per-run metadata · stat analysis · failure taxonomy · cost reconciliation · claim-evidence table | experiments/<slug>/ |
| 6 write | Paper Draft | sections · claim-provenance table · CitationAgent verdict table · threats (from risks) · self-audit | all upstream artifacts |
| 7 review | Submission Package | simulated reviews · weakness triage · CitationAgent verdict table · venue checklist · final PDF | Paper Draft |
| 8 rebuttal | Rebuttal / Revision Record | feedback analysis · response letter · change log · venue-pivot plan | reviewer feedback |
| 9 present | Presentation Package | slides + notes · backup demo · poster · Q&A prep | accepted paper |

Type-specific phases: survey-methodology → Survey Methodology Record;
theory-proofs → Theory & Proofs Record; supplementary → Supplementary & Artifact
Package. `/research-workflow:research evolve` emits an Evolution Log entry to
`${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` (state-dir
runtime log; the bundle file `evolution.md` is legacy pre-H2 scaffolding —
see backlog **M4** for removal tracking).

## Evidence-gap artifact — `GAP_REPORT.md`

When a claim lacks supporting evidence — or a `\cite{}` fails the CitationAgent
contract — the skill records it in `.claude/GAP_REPORT.md` rather than writing around
it or fabricating (R7 — enforces G1 / G7). One row per gap:

| Claim / cite (paper §) | Evidence needed | Why missing | Resolution | Status |
|------------------------|-----------------|-------------|------------|--------|

Resolution ∈ `run-experiment` / `search-literature` / `downgrade-claim` / `drop-claim`;
Status ∈ `open` / `resolved`.

**Acceptance rule:** the Phase 6 `Paper Draft` and Phase 7 `Submission Package`
artifacts cannot reach lifecycle status `accepted` while `GAP_REPORT.md` has any `open`
row or the CitationAgent verdict table has any verdict ≠ `verified`.

## Research Direction Card (Phase 0 — DD3)

Emitted by `/research explore`; the unit a direction decision commits to.

| Field | Content |
|-------|---------|
| provenance | where the direction came from — scan / specific idea / reference set / advisor |
| typed literature gap | the gap + its type: literature / methodological / application / cross-domain / temporal / assumption-relaxation |
| one-sentence claim | the contribution in one jargon-free sentence |
| candidate novelty | overlap HIGH/MED/LOW + closest work + verdict PROCEED/CAUTION/ABANDON (DD2 — wired in M4) |
| contribution type | technique / empirical finding / dataset / tool / SoK |
| falsification criteria | what result would refute the direction |
| feasibility-pilot result | go / no-go if a pilot was run, else `n/a` |
| abandon-if | the kill condition for this direction |

## Research Question Card (Phase 1 — DD3)

Emitted by `/research foundation`; one card per RQ. Carries the DD3 converged
fields plus its RQ-specific fields.

| Field | Content |
|-------|---------|
| provenance | which Direction Card + which motivation evidence `[Paper, §X, p.Y]` |
| typed literature gap | inherited / refined from the Direction Card (DG2 gap type) |
| RQ statement | SMART — Specific, Measurable, Answerable by your method, Relevant, Time-bounded |
| one-sentence claim | the hypothesised answer |
| candidate novelty | overlap HIGH/MED/LOW + closest work + PROCEED/CAUTION/ABANDON (DD2 — wired in M4) |
| contribution type | technique / empirical finding / dataset / tool / SoK |
| falsification criteria | the confirmation result vs the refutation result |
| measurement chain | RQ → experiment → metric → data |
| feasibility-pilot result | go / no-go if a pilot was run, else `n/a` |
| abandon-if | when to drop or reformulate this RQ |

## Fallback — pre-M2 projects

A project initialized before M2 may still carry flat `.claude/research-{progress,risks,decisions}.md`.
`/research` reads those if `research-state.yaml` is absent — a one-release grace
period; the operational fallback logic is in `SKILL.md`. Migrate by copying the two
templates in, moving risks/decisions across, then deleting the flat files.
