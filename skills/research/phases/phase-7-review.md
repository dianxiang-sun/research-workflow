# Phase 7: Review & Submission (`/research review`)

> Find every weakness before reviewers do. Be harder on yourself than they will be.

## Applies to: ALL paper types

## Scope & Ethics

`/research review` and its 5 reviewer personas **simulate** peer review — they are the
authors' own pre-mortem (Global Rule G9), a self-review aid for *your own* manuscript to
find what real reviewers will. The output is internal self-review; it is not a genuine
peer review and carries no venue authority.

**Before running `review`, check the manuscript's provenance:**
- Your own / your team's manuscript → proceed.
- Someone else's manuscript → proceed ONLY if its authors asked you for pre-submission
  feedback (you are running their self-review for them) — confirm this first.
- A manuscript you were assigned to peer-review for a venue, or any confidential
  submission → do NOT run `review`: generating an AI review for it is undisclosed AI
  peer review, which venues prohibit (G9). Decline and tell the user why.

Never present a simulated review, or its scores, to co-authors, an advisor, or a venue
as if it were a real external review.

## Protocol

### 1. Multi-Perspective Simulated Review

Spawn 5 reviewer agents, each with a distinct persona and focus:

| Persona | Focus | Key Questions |
|---------|-------|--------------|
| **Methodology Reviewer** | Technical soundness | "Is the approach technically sound? Any logical gaps in the method? Are assumptions reasonable?" |
| **Experiments Reviewer** | Evaluation rigor | "Are experiments convincing? Fair baselines? Sufficient data? Statistical rigor? Reproducible?" |
| **Domain Expert** | Practical relevance | "Does this matter for practitioners? Is the framing right for this community? Missing domain knowledge?" |
| **Skeptical Reviewer** | Weakest links | "Why should I believe any of this? What's the single biggest reason to reject? What claim has the weakest evidence?" |
| **Presentation Reviewer** | Writing quality | "Is this well-written? Clear? Well-structured? Figures readable? Within page limit? Easy to follow?" |

**Each reviewer fills the 7-Dimension Standardized Rubric** (from Stanford Agentic Reviewer):

| Dimension | Score (1-5) | Evidence |
|-----------|------------|---------|
| D1: Originality | _ | Is this genuinely novel? |
| D2: Research Question Importance | _ | Does this matter? |
| D3: Claim-Evidence Support | _ | Do results support claims? |
| D4: Experimental Soundness | _ | Fair, reproducible, rigorous? |
| D5: Writing Clarity | _ | Well-structured, readable? |
| D6: Community Value | _ | Will the field benefit? |
| D7: Prior Work Contextualization | _ | Well-positioned in literature? |

Each reviewer produces:

```
7-Dimension Scores:
  D1 Originality:       [1-5] — [one-line evidence]
  D2 RQ Importance:     [1-5] — [one-line evidence]
  D3 Claim-Evidence:    [1-5] — [one-line evidence]
  D4 Experimental:      [1-5] — [one-line evidence]
  D5 Writing Clarity:   [1-5] — [one-line evidence]
  D6 Community Value:   [1-5] — [one-line evidence]
  D7 Prior Work:        [1-5] — [one-line evidence]

Overall Assessment: Accept / Weak Accept / Borderline / Weak Reject / Reject
Confidence: Low / Medium / High

Strengths (3+):
1. ...

Weaknesses (3+):
1. ...

Questions for Authors (3+):
1. ...

Minor Issues:
- ...

Missing References:
- ...
```

**Aggregation**: After all 5 reviewers score, compute per-dimension averages and identify
convergence (all reviewers agree) vs divergence (spread > 2 points) — divergent dimensions
need discussion and are likely the paper's most controversial aspects.

### 1b. Cross-Model Adversarial Review (Optional but Recommended)

If multiple LLM APIs are available, use a DIFFERENT model as adversarial reviewer:
- Primary work done by Claude → Review by GPT-4o (or vice versa)
- Cross-model review catches blind spots that same-model self-review misses
- Format: Give the other model the paper + ask it to play Reviewer 2

This is inspired by the ARIS (Auto-Research-In-Sleep) pattern where Claude drives research
while an external LLM acts as critical reviewer.

To invoke: Use Bash to call the other model's API with the paper content.

### 2. Consolidated Weakness Analysis

After all reviews, consolidate:

| # | Weakness | Reviewers | Severity | Fixable? | Action |
|---|----------|-----------|----------|----------|--------|
| W1 | ... | R1, R3 | Fatal | Yes | Fix: ... |
| W2 | ... | R2 | Serious | No | Frame: ... |
| W3 | ... | R4 | Moderate | Yes | Fix: ... |

**Triage categories**:
- **Fix**: Can be addressed before deadline → DO IT
- **Frame**: Can't be fixed but can be reframed in the paper → adjust narrative, add discussion
- **Acknowledge**: Can't be fixed or framed → add to Threats to Validity
- **Dismiss**: Reviewer misunderstood → ensure paper is clearer (don't just argue)

**Important**: If a "Dismiss" requires the reviewer to have misunderstood, the paper is probably unclear. Fix the clarity, don't blame the reviewer.

### 3. Cross-Section Consistency Audit

| Check | How |
|-------|-----|
| §1 contributions = §9 conclusion | Side-by-side comparison, word-for-word |
| Numbers match everywhere | Same metric reported in Abstract, §1, §5, §9 — all identical? |
| Terminology consistent | Same concept uses same term throughout? |
| Figures match text | Every claim about a figure accurately reflects what's shown? |
| Forward/backward refs valid | Every \ref points to existing target? |

### 4. Related Work Completeness Final Check

- For each reviewer persona: "What papers would this reviewer expect to see cited?"
- Search for papers published AFTER your initial literature scan
- Check upcoming conference accepted paper lists in your area
- Any new paper that overlaps → cite and differentiate

### 5. Venue-Specific Checklist

**Conferences (general)**:
- [ ] Page limit compliant (main body + references)
- [ ] Correct template/formatting (single/double column, font size)
- [ ] Anonymous submission (if double-blind): no author names, no self-identifying citations ("our previous work [1]"), no repo links
- [ ] Required sections present (Data Availability, Ethics, etc.)
- [ ] Supplementary material policy followed
- [ ] PDF is clean (no tracked changes, no comments, no metadata leaks)

**SE-specific venues (ASE, ICSE, FSE, ISSTA)**:
- [ ] Threats to Validity section present
- [ ] Replication package mentioned (if applicable)
- [ ] Research questions explicitly stated
- [ ] Data availability statement

**Journals (TSE, TOSEM, ESE)**:
- [ ] Highlights / key points (if required)
- [ ] Graphical abstract (if required)
- [ ] Extended related work (more space, higher expectations)
- [ ] Cover letter drafted

### 6. Double-Blind Compliance Audit (if applicable)

- [ ] Grep for author names in all .tex files
- [ ] Check for self-citations that reveal identity ("our previous work [X]" → use "prior work [X]")
- [ ] Search for repo URLs, institutional URLs, or project-specific URLs
- [ ] Check PDF metadata (Author field, Creator field) — use `pdfinfo` or `exiftool`
- [ ] Check figures for institutional logos or watermarks
- [ ] Check acknowledgments section — should be anonymized or removed
- [ ] Verify .bib entries don't contain author-revealing notes

### 7. Pre-Submission Technical Checks

- [ ] PDF compiles cleanly (no LaTeX warnings for refs/citations)
- [ ] All figures render correctly at print resolution
- [ ] All hyperlinks work
- [ ] Supplementary materials are complete and organized
- [ ] Replication package (code, data, scripts) is ready (if required)
- [ ] Co-author approval obtained
- [ ] Submission system requirements verified (file size, format, etc.)

## Emitted Artifact

`Submission Package` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria (FULL matrix — this is the FINAL gate)

> **Rubric contract** — input `Paper Draft` → scores `Submission Package`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- ALL "Fix" weaknesses actually fixed?
- ALL "Frame" weaknesses have defensible framing in paper?
- ALL "Acknowledge" weaknesses in Threats section?
- Cross-section consistency perfect?
- Venue checklist 100% compliant?
- Related work up-to-date (checked within last 2 weeks)?
- Co-author/advisor sign-off obtained?
- CitationAgent verdict table complete — every `\cite{}` `verified`; `GAP_REPORT.md` has no `open` row?
