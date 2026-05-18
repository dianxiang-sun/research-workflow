# Capability — Direction Ideation

> Reference detail for the `research` skill — the GENERATION and non-scalar DECISION
> machinery `phases/phase-0-explore.md` calls. Phase 0 points here; this doc holds the
> taxonomy, lenses, and filters, and does not restate the phase protocol. (M4b / §12.)

## Diverge → Converge → Refine

Phase 0's ideation sub-protocol — **advisory, not a forced funnel** (see entry points):

- **Diverge** — generate 8-15 candidate directions (quantity first, no filtering yet); drive breadth with the gap-type taxonomy + the brainstorming lenses below.
- **Converge** — apply the disposition filters (keep/park/revise/escalate) + a quick candidate-novelty check on survivors.
- **Refine** — the chosen direction → a deep candidate-novelty check + a Research Direction Card.

### Entry points — the funnel is not an FSM

| You arrive with… | Enter at |
|------------------|----------|
| a vague topic / broad area | full Diverge |
| a specific idea already in hand | skip Diverge → quick novelty check → Refine |
| a set of reference papers | Diverge, seeded by reference-based ideation |
| an advisor-approved / mature direction | skip Phase 0 → Phase 1 (foundation) |

When Diverge or all of Phase 0 is skipped, still backfill a minimal Research Direction
Card (provenance · gap type · one-sentence claim · abandon-if) so the Phase-1 RQ Card's
provenance chain stays intact.

## Gap-type taxonomy

Every candidate direction names which gap type it targets — a positive taxonomy, not
only anti-patterns:

- **literature** — a question the published record openly leaves unanswered
- **methodological** — an approach works in setting X, is untried or fails in Y
- **application** — a mature method not yet brought to a domain that needs it
- **cross-domain-transfer** — a technique structurally imported from an adjacent field
- **temporal** — an old negative result worth revisiting under new compute / scale / data / tooling
- **assumption-relaxation** — a widely-held premise that does not hold in practice

**False-gap filter** — a generated gap must clear all three:
- "nobody has done X" — maybe X is not useful; show the demand.
- "we combine A and B" — combination alone is not novelty; show the non-obvious why.
- "we apply X to domain Y" — may be incremental; show what Y forces X to change.

## Brainstorming lenses (Diverge)

One pass per lens — each a distinct cognitive angle; skip any that do not fit:

1. **Problem-first / solution-first** — start from a real pain, or a capability seeking a problem.
2. **Abstraction ladder** — generalize the problem up, instantiate down, analogize sideways.
3. **Tension hunting** — find an accepted trade-off and ask what dissolves it.
4. **Cross-pollination** — import a structural pattern from another field.
5. **"What changed?"** — revisit an old dead end under new compute / scale / data / regulation.
6. **Failure / boundary probing** — where do current methods break, and why.
7. **Simplicity test** — the simplest thing that could possibly work here.
8. **Stakeholder rotation** — view the problem as each stakeholder in turn.
9. **Composition / decomposition** — fuse several problems, or split one into parts.
10. **Explain-it test** — if you cannot pitch it in two sentences, it is not sharp yet.

## Disposition filters (Converge)

For EACH candidate, judge each filter and assign a disposition WITH a cited reason —
**never a numeric or ordinal score, never an auto-drop on one fail**:

| Filter | Question |
|--------|----------|
| genuine problem | does a real beneficiary feel this pain? |
| novelty | is the closest-work overlap not HIGH (candidate-novelty check)? |
| simplicity | is the complexity justified by the problem? |
| beneficiary | who specifically ends up better off, and how? |
| feasibility | doable within the project's resources and timeline? |

Disposition ∈ **keep** (carry to Refine) · **park** (set aside, may revisit — e.g.
infeasible *now*) · **revise** (reframe, then re-filter) · **escalate** (no clear call →
the human decides). "No clear beneficiary" must not auto-kill theory work; "infeasible
now" is `park`, not a kill. A candidate-novelty `ABANDON` verdict is a cited *reason*
feeding the `novelty` filter, not an auto-drop. Parked / revised-away /
escalated-then-eliminated directions go to `findings.md` → Eliminated / Parked
Directions (anti-repetition memory).

For the surviving direction(s) make an **F5 decision card** — ≥3 candidates, each with
pros / cons / trade-off, task-specific 关键维度, a reasoned recommendation
(`~/.claude/CLAUDE.md` F5); relative and evidence-backed, the researcher decides. No
multiplied scalar, no "count the highs". If fewer than 3 candidates survive, do NOT pad
with weak ones — re-Diverge, revise a parked candidate, or escalate; a lone strong
survivor goes straight to Refine with the thin option space logged.

## Cards

Phase 0 emits a Research Direction Card; Phase 1 a Research Question Card. The single
canonical schema for both: `reference/capability-artifacts.md`.
