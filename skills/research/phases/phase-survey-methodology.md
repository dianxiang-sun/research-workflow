# Phase: Survey/SoK Methodology

> Replaces Phases 2-5 for `paper_type: survey`.
> A systematic review is NOT "read papers and summarize" — it's a reproducible research method.

## When This Phase Activates

After Phase 1 (foundation — why is this survey needed now?), survey papers enter this phase instead of Phases 2-5. Proceed to Phase 6 (write) after completing this phase.

```
Phase 0 (explore) → Phase 1 (foundation) → THIS PHASE → Phase 6 (write) → Phase 7 (review) → Phase 8 (rebuttal)
```

## Protocol

### 1. Search Protocol Definition (BEFORE searching)

Document the search protocol upfront — this IS the "method" of a survey:

```markdown
## Search Protocol
- Databases: [DBLP, IEEE Xplore, ACM DL, Scopus, Google Scholar, arXiv]
- Query strings: [list ALL queries with Boolean operators]
- Time range: [e.g., 2019-2026]
- Language: [e.g., English only]
- Date of search: [exact date]
```

**Rules**:
- Define queries BEFORE executing them (not post-hoc rationalization)
- Use ≥3 databases to avoid single-source bias
- Record exact queries and result counts per database
- Include arXiv/preprints but flag them as non-peer-reviewed

### 2. Screening Process (Two-Phase)

**Phase A — Title + Abstract Screening**:
- Apply inclusion/exclusion criteria to ALL results
- Criteria must be defined BEFORE screening:

| Criterion | Include | Exclude |
|-----------|---------|---------|
| Topic | (define) | (define) |
| Venue tier | (define) | (define) |
| Paper type | (define) | (define) |
| Language | (define) | (define) |

- Record: total found → after dedup → after title/abstract screening

**Phase B — Full-Text Screening**:
- Read full text of surviving papers
- Apply additional quality/relevance criteria
- Record: after full-text screening → final corpus size

**PRISMA Flow Diagram** (must produce):
```
Records identified (N=__)
  ↓ Remove duplicates (N=__)
  ↓ Title/abstract screening (excluded: N=__, reasons: __)
  ↓ Full-text screening (excluded: N=__, reasons: __)
  ↓ Snowballing additions (N=__)
Final corpus (N=__)
```

### 3. Snowballing

After initial corpus:
- **Backward snowballing**: Check reference lists of included papers
- **Forward snowballing**: Check papers citing included papers (Google Scholar)
- Apply same inclusion/exclusion criteria
- Record additions separately in PRISMA diagram

### 4. Quality Assessment

For each included paper, assess methodological quality:

| Paper | Study Design | Threats Addressed | Data Quality | Reproducibility | Score |
|-------|-------------|-------------------|-------------|-----------------|-------|

Scoring:
- Define scoring rubric BEFORE assessment
- If possible, have 2+ raters with inter-rater agreement (Cohen's κ)
- Quality scores may be used to weight findings in synthesis

### 5. Data Extraction

Define extraction form BEFORE reading:

| Paper | Year | Venue | Method Category | Key Approach | Evaluation | Limitations | Findings Relevant to RQ1 | ... |
|-------|------|-------|----------------|-------------|------------|-------------|--------------------------|-----|

**Rules**:
- One row per paper, columns aligned with RQs
- Extract FACTS, not interpretations (interpretation comes in synthesis)
- Use `/verify-before-write` for any specific statistics
- Flag ambiguous or conflicting data explicitly

### 6. Synthesis Methodology

Choose ONE synthesis method and justify:

| Method | When to Use | How |
|--------|------------|-----|
| **Narrative synthesis** | Heterogeneous studies, qualitative focus | Organize by theme, identify patterns and contradictions |
| **Thematic analysis** | Many papers, need categorization | Code findings → themes → cross-cutting analysis |
| **Meta-analysis** | Quantitative results, comparable metrics | Statistical pooling of effect sizes (requires comparable measures) |
| **Mapping study** | Broad landscape, frequency-focused | Tabulate categories, visualize distribution |

**Synthesis structure** (must produce at least):
- Taxonomy/classification of approaches (with clear categories)
- Comparison table (papers × dimensions)
- Trend analysis (evolution over time)
- Gap identification (what's missing from the landscape)
- Contradiction analysis (where papers disagree and why)

### 7. Threats to Validity (Survey-Specific)

| Threat | How to Address |
|--------|---------------|
| Search completeness | Multiple databases, snowballing, multiple query variants |
| Selection bias | Explicit inclusion/exclusion criteria, PRISMA documentation |
| Data extraction reliability | Extraction form, inter-rater agreement if possible |
| Publication bias | Include grey literature (arXiv), check for negative results |
| Recency bias | Fixed time window, documented search date |

## Emitted Artifact

`Survey Methodology Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `Research Question Card` → scores `Survey Methodology Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- Search protocol documented BEFORE execution?
- PRISMA diagram complete with numbers at every stage?
- Inclusion/exclusion criteria explicit and applied consistently?
- Data extraction form covers all RQs?
- Synthesis method justified and executed?
- At least one taxonomy + one comparison table produced?
- Gaps explicitly identified (these drive the "so what" of the survey)?
