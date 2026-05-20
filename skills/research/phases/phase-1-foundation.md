# Phase 1: Problem Foundation (`/research foundation`)

> Build rigorous intellectual foundation — motivation backed by evidence, RQs that are testable.

## Applies to: ALL paper types

## Protocol

### 1. Deep Reading (core papers, ≤12)
- If installed: use `/speed-read` per paper, `/map-reduce-papers` for 3+. Otherwise: read each paper end-to-end and fill the notes table below by hand — the table is what matters, the commands are only a shortcut to populate it.
- Structured notes per paper:

  | Aspect | Content |
  |--------|---------|
  | Method | Core approach + architecture |
  | Key Results | Quantitative, with `[Paper, §X, p.Y]` provenance |
  | Limitations | What they acknowledge + what they miss |
  | Inspiration | What we can learn / build upon / differentiate from |
  | Relevance to direction | What this paper settles / opens up *for our research direction* — read through the lens of the working direction, not as a generic abstract |

- Every extracted statistic MUST be verified before being written into the notes — this is a **G1 hard requirement, not optional**:
  - **Preferred path:** `/verify-before-write` if the command is installed.
  - **Inline fallback (always available, MUST be used when the command is not):** re-open the source paper, locate the statistic in context, copy the exact value + unit + sample size into the note, and confirm the surrounding sentence's truth claim. Skipping this fallback because "the command isn't installed" is a G1 (zero-fabrication) violation, not a tolerated degradation.
- Distinguish "paper claims X" from "paper proves X" — many claims are unverified
- **Query-conditioned reading (RCS, T2)**: write every note above *relative to the working research direction* (the Phase-0 Research Direction Card — Phase 1's input) — a generic, abstract-style summary that ignores our direction is the anti-pattern. After noting the set, **re-rank** the reading list by relevance to set reading *depth*. Re-ranking sets depth, never inclusion — a must-cite, closest-prior-work, or contradictory / threatening paper is read regardless of its relevance rank.

### 2. Motivation Construction

**[SYSTEMS/EMPIRICAL]**
- Identify the REAL problem (not a strawman you build just to knock down)
- Quantitative evidence for the problem's existence and severity
- Every motivation data point: verified provenance `[Paper, §X, p.Y]`
- The "taxi test": Can you explain why this matters to a non-expert in 2 sentences?

**[SURVEY]**
- Justify WHY a survey is needed now (rapid growth? fragmentation? contradictions?)
- Show evidence: paper count growth curve, conflicting findings, missing synthesis

**[BENCHMARK]**
- Show existing benchmarks' inadequacy with concrete examples
- Gap in coverage, staleness, or methodology flaws

### 3. Research Question Formulation
- Each RQ must be **SMART**: Specific, Measurable, Answerable (by YOUR method), Relevant, Time-bounded
- For each RQ, define explicitly:
  - **Confirmation**: What result would confirm it?
  - **Refutation**: What result would refute it? (If nothing can refute it, it's not a good RQ)
  - **Measurement**: RQ → required experiment → required metric → required data
- Common RQ anti-patterns:
  - Too broad: "Does our method improve security?" → Improve which aspect? By how much? Compared to what?
  - Unfalsifiable: "Can LLMs generate code?" → Yes, trivially. What's the interesting question?
  - Tautological: "Does adding component X improve metric Y?" when X directly targets Y by design

### 4. Contribution Statement
- Draft 1-sentence contribution claims (will evolve through later phases)
- For each contribution:
  - "How is this DIFFERENT from all prior work?" (not just "better")
  - "What type of contribution is this?" (method/tool/empirical finding/dataset/insight)
  - "What would the field lose if this contribution didn't exist?"
  - **[DOMAIN:se] Contribution type classification** (helps calibrate novelty bar):
    | Type | Novelty Bar | Example |
    |------|------------|---------|
    | New technique/algorithm | Must demonstrate theoretical or empirical advantage over SOTA | "A new static analysis that detects X with Y% fewer false positives" |
    | New empirical finding | Must reveal non-obvious insight from data | "We find that 83% of developers ignore security until deployment" |
    | New dataset/benchmark | Must fill a clear gap, be high-quality, and be reusable | "A dataset of 1000 real-world vulnerable smart contracts with ground truth" |
    | New tool | Must demonstrate practical value beyond proof-of-concept | "A tool that integrates into CI/CD and reduces vulnerability introduction by X%" |
    | Systematization of Knowledge (SoK) | Must synthesize across 50+ papers with novel taxonomy | "We categorize 120 smart contract security papers into 8 defense strategies" |

    Your target venue's culture determines which types are valued — ICSE favors technique+empirical, ASE favors tool+empirical, ISSTA favors technique+formal.

## Emitted Artifact

`Research Question Card` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Research Direction Card` → scores `Research Question Card`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- **Evidence gate**: every motivation citation + the RQ's supporting evidence is a real retrievable source — no abstract-only or placeholder citation.
- Can a SKEPTICAL reviewer accept every motivation data point? (all verified?)
- Are RQs answerable by experiments you can actually run with your resources?
- For each RQ: Can you name a plausible result that would REFUTE it?
- Is each contribution a genuine advance, not just "we applied X to Y"?
- Can you explain your motivation to a non-expert in 2 sentences?
