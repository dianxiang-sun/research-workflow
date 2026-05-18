# Phase 8: Post-Submission (`/research rebuttal`)

> Respond to reviewer feedback effectively, or pivot gracefully. Don't let ego drive decisions.

## Applies to: ALL paper types

## Protocol

### 1. Reviewer Feedback Analysis (Before Reacting)

**Cooling period**: Read reviews once, then wait. Re-read after 24h with fresh eyes.

**Structured analysis per reviewer**:

| Reviewer | Score | Confidence | Top Concern | Fixable? | Our Assessment |
|----------|-------|-----------|-------------|----------|---------------|
| R1 | ... | ... | ... | Yes/No | Agree/Partially/Disagree |

**Classify each comment**:
- **Valid criticism**: They're right. Fix it.
- **Misunderstanding**: They misread. Clarify the paper (not just the response).
- **Scope disagreement**: They want something different. Politely explain scope choice.
- **Subjective preference**: "I'd prefer X" — accommodate if easy, explain if not.

**Red flag**: If you classify >50% as "misunderstanding" or "disagree", the paper has a clarity problem.

### 2. Response Letter (If Revision Allowed)

**Format per comment**:
```
> [Reviewer comment, quoted]

Thank you for this observation. [Concrete action taken]:
- In §X, we [specific change with diff].
- [Evidence or reasoning that addresses the concern].
- [What has changed in the revised paper].
```

**Rules**:
- Be SPECIFIC: "We added Table X in §Y" not "We addressed this."
- Be GRATEFUL, not defensive: "Thank you for catching this" not "The reviewer missed that..."
- Show, don't tell: Include the actual revised text or table
- If you disagree: Present evidence, not opinion. "Our experiments show..." not "We believe..."
- Track all changes: Provide a change log mapping reviewer comments to paper edits

**Consistency check after revisions**:
- Changes in §3 don't contradict §5?
- New data in Table X matches text in §5.2?
- Updated claims don't exceed updated evidence?

### 3. If Accepted (with Minor/Major Revisions)

**Minor revisions**:
- Address every point. Reviewers remember.
- Don't introduce new content that changes the paper's scope.
- Camera-ready deadline is HARD — plan backward from it.

**Major revisions**:
- Prioritize by impact: Address the concerns that caused rejection risk first.
- If additional experiments needed → back to Phase 5 (mini version).
- Timeline: Major revision cycles are typically 2-4 months. Plan accordingly.
- Keep a revision log: what changed, where, why.

### 4. If Rejected — Venue Pivot

**Don't**:
- Submit to the same venue without significant changes (desk reject risk)
- Rage-quit the paper (sunk cost is real, but so is the value of the work)
- Ignore all feedback (even unfair reviews often contain valid points)

**Do**:
1. **Extract lessons**: What's the REAL reason it was rejected? (not what you want to believe)
2. **Decision**: Revise for another venue, or shelf?

**Venue Pivot Analysis**:

| Factor | Current Venue | Candidate Venue | Impact |
|--------|-------------|-----------------|--------|
| Page limit | 10 | 12 (or unlimited journal) | Can expand method/results |
| Review culture | Novelty-heavy | Engineering-welcome | May reframe contribution |
| Audience | Researchers | Practitioners | May emphasize different results |
| Deadline | Past | +3 months | Time for additional experiments? |
| Tier | A* | A / B | Acceptable trade-off? |

**Adaptation plan**:
- Which reviewer concerns can be addressed?
- Which require additional experiments? (cost + time estimate)
- How does framing change for new audience?
- What can be added with the extra time/pages?

### 5. Lessons Learned Capture

Regardless of outcome, update:
- **Risk Registry**: Which risks materialized? Which mitigations worked?
- **Decision Log**: Outcome of this submission cycle
- **Personal learnings**: What would you do differently next time?
- **Skill feedback**: Did the `/research` skill miss anything? What check would have caught the issue earlier?

## Emitted Artifact

`Rebuttal / Revision Record` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `reviewer feedback` → scores `Rebuttal / Revision Record`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- Every reviewer comment addressed (explicitly, not implicitly)?
- Response letter is specific and evidence-based (not defensive)?
- Revised paper passes full cross-section consistency check?
- No new content introduced that contradicts existing content?
- Lessons captured for next project?
