# Phase 6: Paper Writing (`/research write [§N]`)

> Translate results into a compelling, honest, verifiable academic narrative.
> This phase covers BOTH data accuracy AND writing quality.

## Applies to: ALL paper types

## Protocol

### 1. Narrative Arc Design (BEFORE writing any section)

A paper is a STORY, not a report. Design the arc first:

```
Hook (§1 para 1)     → Why should the reader care? (problem severity, real-world impact)
Problem (§1-§2)      → What's broken? (with evidence, not strawman)
Insight (§2-§3)      → What key insight enables your solution?
Method (§3)          → How does your insight become a method?
Evidence (§4-§5)     → Does it work? (honest, with limitations)
Implications (§6)    → What does this mean for the field?
```

**Test**: Read only the first sentence of each section — do they tell a coherent story?

**Motivating Example** (§2, if applicable):
- Pick ONE concrete example that demonstrates the problem AND hints at the solution
- Must be real (not contrived), representative (not cherry-picked), understandable (not too complex)
- The reader should think "Oh, I see why this is hard" and "Oh, I see how their approach helps"

### 2. Page Budget Allocation

Before writing, plan space usage. Example for 10-page conference paper:

| Section | Target Pages | Priority if Over Limit |
|---------|-------------|----------------------|
| §1 Introduction | 1.0 | Cut background, keep contribution list |
| §2 Motivating Example / Background | 0.5-1.0 | Can merge into §1 or §3 |
| §3 Method/Framework | 2.5-3.0 | Core — protect |
| §4 Evaluation Setup | 1.0-1.5 | Move details to appendix |
| §5 Results & Analysis | 2.0-2.5 | Core — protect |
| §6 Discussion | 0.5-1.0 | Can trim |
| §7 Related Work | 1.0-1.5 | Trim if needed, never cut entirely |
| §8 Threats to Validity | 0.5 | Required for SE venues |
| §9 Conclusion | 0.3-0.5 | Keep tight |

**Over limit?** Cut in this order:
1. Verbose explanations → tighten prose
2. Redundant figures/tables → keep only highest-value ones
3. Move implementation details to appendix/supplementary
4. Merge sections (Background into Intro, Discussion into Results)

**Adapt by venue type:**
- Workshop (4-6 pages): Merge §2 into §1, cut §6, minimize §7-§8
- Conference (10-12 pages): Use table above
- Journal (no limit): Expand §3, §5, §7; add detailed appendices
- Read `page_limit` from project config to calibrate

**Figure/Table ROI**: Each figure ≈ 1/3 page. Ask: "Does this figure convey information that text alone cannot? Is it worth 1/3 page?"

### 3. Section-by-Section Writing Protocol

**§1 Introduction**:
- Para 1: Hook — problem statement with real-world impact (NOT "software is important")
- Para 2-3: Problem scope + existing approaches and their limitations
- Para 4: Your insight/key idea (one sentence that captures the novelty)
- Para 5-6: Your approach (brief) + key results (numbers!)
- Final para: Contribution list (numbered, specific, verifiable)
- **Self-check**: Contributions in §1 must EXACTLY match §9 conclusion claims

**§3 Method**:
- Architecture overview first (figure + 1 paragraph), details second
- Each component: what it does, why it's designed this way (cite rationale), how it connects to others
- Algorithm/pseudocode for non-obvious logic
- **Scope lock**: Only edit declared .tex files

**§4 Evaluation Setup**:
- RQs listed explicitly
- Dataset description with provenance
- Metrics with precise definitions (not just names)
- Baselines with fairness justification
- Implementation details (models, parameters, hardware)

**§5 Results**:
- One subsection per RQ
- Lead with the answer ("RQ1: Yes, our method improves..." or "RQ1: Partially, ...")
- Then evidence (tables, figures, numbers — ALL with provenance)
- Then analysis (WHY, not just WHAT)
- Include negative/unexpected findings

**§7 Related Work** — see dedicated protocol below

**§8 Threats to Validity** — see dedicated protocol below

### 4. Data-Driven Writing (Claim Provenance)

Every number in the paper must be traceable. Build this table:

| Claim | Paper Location | Source File:Line | Paper Value | Source Value | Match? |
|-------|---------------|-----------------|-------------|-------------|--------|

Rules:
- Use `/verify-before-write` for statistics from cited papers
- Never add `\cite{}` without PDF verification
- After writing each section, grep all numbers → verify each against source

**Claims-from-results check** (R7 — enforces G7): in the Claim Provenance Table, every
claim whose value comes from your experiments MUST have a `Source File:Line` resolving
under `experiments/*/results/`. A result claim with no such backing row is downgraded
(scope-limited or `[UNVERIFIED]`) or logged to `GAP_REPORT.md` — never asserted on
absent evidence.

**Decoupled descriptions (T3 — enforces G1)**: keep any model-written *description* of a
source — a one-line gloss of a cited paper's method, a qualitative summary, a synthetic
/ AI-drafted figure caption — in a field SEPARATE from verbatim source text. In the
Claim Provenance Table, when a `Source Value` is a natural-language description (not a
bare number — a copied number is verbatim by nature), tag it `verbatim: "<text copied
from the source>"` or `paraphrase: <your own wording>`. Only a `verbatim` value may be
quoted or attributed as the source's own words; a `paraphrase` is your framing and is
never quoted, captioned, or cited as the source's verbatim text. This closes the path
where a `\cite{}` quotes a hallucinated caption — the CitationAgent contract
(`reference/capability-critique.md`) verifies the citation *exists*; T3 ensures any
quoted *text* is genuinely the source's.

### 5. Related Work Completeness Protocol

Related work is NOT a literature dump — it's a positioning argument: "Here's the landscape, here's the gap, here's where we fit."

**Structure** (one of):
- **By dimension**: Group by approach type, then show what's missing
- **By evolution**: Show how the field progressed, then show the next step (yours)
- **By contrast**: Explicitly compare your method to each category

**Completeness Audit**:
1. **Must-cite list**: For your research area, which papers would ANY reviewer expect to see? List them.
2. **Recency check**: Are you citing papers from the last 2 years? (stale related work = red flag)
3. **Coverage check**: Does your categorization cover ALL major approaches, or are you conveniently omitting competitors?
4. **Self-citation check**: Are you citing your own prior work fairly? (not too much, not too little)
5. **Positioning clarity**: After reading related work, can the reader state exactly how your work differs from each category?

**Red flag**: If related work reads like a list of "X did this. Y did that." without a clear narrative thread → rewrite with positioning.

### 6. Threats to Validity Protocol

Draw from Risk Registry (`accepted_risk` items are primary candidates).

**Standard SE categorization**:

| Category | What to Address | Example |
|----------|----------------|---------|
| **Construct validity** | Do metrics measure what you claim? | "Slither findings ≠ security" |
| **Internal validity** | Can you attribute results to your method? | "LLM non-determinism, confounding variables" |
| **External validity** | Do results generalize? | "Only tested on Solidity, dataset bias" |
| **Conclusion validity** | Are statistical conclusions sound? | "Single-run variance, sample size" |

**Writing rules**:
- Be honest but not suicidal — acknowledge the threat, then describe your mitigation
- Format: "Threat → What we did about it → Residual risk"
- Don't list threats you have NO mitigation for (that's just handing ammo to reviewers)
- Threats should map to design decisions in the Decision Log

### 7. Figure/Table Quality Standards

**Figures**:
- [ ] Clear axis labels with units
- [ ] Readable font size (≥8pt when printed)
- [ ] Color-blind friendly palette (no red-green only distinctions)
- [ ] Standalone caption (reader understands without reading body text)
- [ ] No 3D charts (almost never justified)
- [ ] Consistent style across all figures
- [ ] Vector format (PDF) for line plots, high-DPI for screenshots

> Caption provenance: a caption describing a *cited paper's* figure, or any AI-drafted caption, follows §4's decoupled-descriptions rule — a model-written caption is never presented as the source's verbatim text.

**Tables**:
- [ ] Consistent decimal places per column
- [ ] Clear which direction is "better" (bold best, ↑/↓ indicators)
- [ ] Units in column header, not repeated per cell
- [ ] Standalone caption
- [ ] If comparing methods: row per method, column per metric (standard layout)
- [ ] Statistical significance markers if applicable (*, **, ***)

### 8. Self-Audit Before Handoff

**Prose Quality [DOMAIN:se]** (top-venue papers require clear writing):
- [ ] Active voice predominant (not "it was observed that" but "we observed")
- [ ] Each paragraph has a clear topic sentence
- [ ] No orphan pronouns ("this" without clear antecedent → specify "this approach" / "this result")
- [ ] Concrete subjects (not "it is important to note" but state what's important directly)
- [ ] No walls of text — paragraphs ≤ 8 lines, break up with subheadings
- [ ] Transitions between sections are explicit (not just juxtaposition)
- [ ] Technical terms defined on first use
- [ ] Consistent tense (present for general truths, past for your experiments)

Before declaring any section "done":
- [ ] All numbers verified against Claim Provenance Table
- [ ] All `\cite{}` verified against .bib (no phantom citations)
- [ ] All `\ref{}` targets exist (no broken references)
- [ ] §1 contributions match §9 conclusion claims EXACTLY
- [ ] No `[UNVERIFIED]` markers remain (or explicitly acknowledged)
- [ ] Spell check / grammar check passed
- [ ] Page budget check — within allocation?
- [ ] Cross-section consistency (same terminology, same numbers everywhere)

## Emitted Artifact

`Paper Draft` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `all upstream artifacts` → scores `Paper Draft`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- H1: Narrative arc is coherent? (first sentences tell a story?)
- H2: Related work positions your work clearly? (not a literature dump?)
- H3: Threats section is honest but defended? (from Risk Registry?)
- H4: Within page budget? (or deliberate overrun with cut plan?)
- B5: Every claim's scope ≤ evidence scope?
- All numbers in provenance table? All verified?
- §1 contributions = §9 conclusion claims?
