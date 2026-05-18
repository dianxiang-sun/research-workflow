# Phase 0: Direction Exploration (`/research explore`)

> From a topic, an idea, or a paper set, decide a research direction with genuine novelty.

## Applies to: ALL paper types

## Protocol

> Phase 0 generates and decides a direction via an advisory **Diverge → Converge →
> Refine** sub-protocol. Gap-type taxonomy, brainstorming lenses, disposition filters,
> and entry-point rules: **`reference/capability-ideation.md`** — a researcher who
> already holds a specific idea or a mature direction skips ahead; this is a guide,
> not a funnel.

### 1. Literature Landscape Scan
- Define systematic search queries (NOT random browsing): ≥3 query phrasings per sub-area
- Build structured table:

  | Paper | Year | Venue | Method Type | Key Contribution | Limitations | Potential Gap |
  |-------|------|-------|-------------|-----------------|-------------|---------------|

- Use `/map-reduce-papers` for batch processing (3+ papers), `/speed-read` for individuals
- NEVER claim search is exhaustive — always document query scope and databases searched
- Check both published (DBLP, Semantic Scholar) and preprints (arXiv)
- Note the search date — results become stale within months

### 2. Diverge — generate candidate directions

- Generate 8-15 candidate directions; quantity first, do NOT filter yet.
- Drive breadth with the gap-type taxonomy + the brainstorming lenses
  (`reference/capability-ideation.md`).
- For each candidate, name the gap type it targets and a one-sentence jargon-free claim.
- Run the **gap-disproof search** — ≥3 query phrasings looking for papers that already
  FILL the gap; a candidate's gap survives only if the disproof search fails.

### 3. Converge — filter, novelty-check, decide

- Apply the disposition filters (`reference/capability-ideation.md`): each candidate
  gets **keep / park / revise / escalate** WITH a cited reason — never a numeric or
  ordinal score, never an auto-drop on a single fail.
- Run the **quick candidate-novelty check** on survivors — 2-3 searches each → overlap
  HIGH / MED / LOW (`reference/capability-critique.md`).
- For the survivors build an **F5 decision card** — ≥3 candidates · pros/cons/trade-off ·
  task-specific 关键维度 (e.g. publication potential, target-venue fit, feasibility vs
  timeline, resource cost) · reasoned recommendation; the researcher makes the call.
- Parked / revised-away / escalated-then-eliminated candidates → `findings.md`
  Eliminated / Parked Directions, so re-ideation does not regenerate them.

### 4. Refine — the chosen direction

- Run the **deep candidate-novelty check** on the chosen direction — multi-source +
  cross-model check → closest-work table + PROCEED / CAUTION / ABANDON
  (`reference/capability-critique.md`).
- Feasibility: resources (data — exists / licensable?; compute; tools; expertise), a
  realistic timeline to a target deadline, and the key technical risks.
- **Kill condition**: under what circumstances would you abandon this direction?

## Emitted Artifact

`Research Direction Card` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `topic / idea / paper set` → scores `Research Direction Card`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- **Evidence gate**: every source backing the direction is real and retrievable — no abstract-only or placeholder citation (cf. R7 / GAP_REPORT.md).
- Can you state the gap in ONE sentence without jargon?
- Have you searched ≥3 alternative phrasings and found NO paper filling the gap?
- Is the gap at the right granularity? (not "improve SE" nor "fix line 42")
- Is there a realistic path from gap to publishable result within your timeline?
- **Kill test**: If someone published a 70% overlap paper tomorrow, is your remaining 30% still publishable?
