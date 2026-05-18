# Phase 9: Presentation Preparation (`/research present`)

> After paper acceptance, prepare a compelling conference talk, poster, or demo that communicates your work effectively.

## Applies to: ALL paper types

## Protocol

### 1. Talk Structure (15-25 minute conference talk)

#### Opening Hook (30 seconds)
- One striking example, statistic, or failed scenario that makes the problem visceral
- NOT "In this paper we present..." — start with the problem, not yourself
- Aim for the audience to think "oh, that IS a problem" within 20 seconds

#### Problem and Motivation (2-3 minutes)
- Why this matters to the audience (not just to you)
- Scope the problem clearly — what is in and out
- One concrete example that the audience can follow through the entire talk
- End with: "Existing approaches do X, but they miss Y" (the gap)

#### Key Insight (1 minute)
- The single "aha" moment that makes your approach work
- State it in one sentence a non-expert could understand
- This is the slide the audience photographs — make it count

#### Method Overview (5-7 minutes)
- Architecture diagram: high-level boxes and arrows, NOT code
- Walk through your running example step by step through the system
- Explain WHY each component exists, not HOW it is implemented
- Skip implementation details that do not affect understanding
- If multi-phase: show the pipeline with one slide per phase, highlight the novel parts

#### Key Results (5-7 minutes)
- Lead with the most impactful number or comparison
- Show at most 2-3 result figures/tables — not the full paper's worth
- For each result: state what the audience should see, THEN show the figure
- One qualitative example or demo that makes the numbers tangible
- Acknowledge limitations briefly (shows intellectual honesty, builds trust)

#### Takeaway (1-2 minutes)
- What should the audience remember tomorrow? State it explicitly
- Broader implications: what does this enable beyond your specific problem?
- Future work: one sentence, not a roadmap
- End with a clear final slide (not "Questions?") — a summary slide with key claim + result

#### Q&A Preparation
- Predict top-5 questions from reviewer feedback and prepare concise answers
- Prepare backup slides for: detailed results, ablation breakdowns, failure cases, related work comparison
- For hostile questions: acknowledge the concern, give a short answer, offer to discuss offline
- Never bluff — "I don't know, but here's how I'd find out" is always acceptable

### 2. Slide Design Rules

- **One message per slide** — if you need two points, use two slides
- **Minimize text** — the audience either reads or listens, not both; use keywords not sentences
- **Font sizes**: title >=28pt, body >=20pt, axis labels >=16pt; if you squint, it is too small
- **Figures from paper**: reuse but ENLARGE all labels and legends for projection
- **Table to chart**: convert paper tables to bar/line charts for talks; tables are for reading, charts for presenting
- **Consistent color scheme**: pick 3-4 colors, use them throughout; match paper figures if possible
- **Slide numbers**: always show "current/total" (e.g., "12/25") so audience knows pacing
- **Animation**: use sparingly to reveal information progressively, never for decoration
- **Build slides**: for complex diagrams, reveal components one at a time as you explain them

### 3. Demo Preparation (if applicable)

- **Pre-record a backup** — ALWAYS, even if you plan to demo live; Murphy's law applies at conferences
- **Test on the presentation machine** beforehand: projector resolution, font rendering, network access
- **Minimize dependencies**: no live network calls if avoidable; use cached/local data
- **Have fallback screenshots** if the demo crashes — narrate over the screenshots as if it were a video
- **Keep demo under 3 minutes** — longer demos lose the audience; show the highlight, not the full workflow
- **Annotate what to look at**: audience does not know your UI; use cursor, highlights, or callouts

### 4. Poster Protocol (if applicable)

- **Size and orientation**: check venue requirements (typically A0, portrait or landscape)
- **Title readable from 3 meters**, body text readable from 1 meter
- **Flow**: top-left to bottom-right (or clearly numbered sections)
- **Structure**: Title/Authors, Problem, Method (one figure), Key Results (one figure), Conclusion, QR code
- **QR code**: link to paper PDF, code repository, or project page
- **White space**: do not fill every pixel; breathing room helps readability
- **Print a draft at actual size** before the final print — things look different at A0
- **Prepare a 2-minute elevator pitch** and a 5-minute detailed walkthrough

### 5. Rehearsal Protocol

- **Minimum 3 dry runs**:
  1. Alone with timer (focus on content and pacing)
  2. With a labmate (focus on clarity — do they understand without reading the paper?)
  3. With advisor or senior colleague (focus on framing and academic positioning)
- **Time each run**: must finish within the time limit minus 2-minute buffer for Q&A setup
- **Record yourself** (screen + audio at minimum): watch for filler words ("um", "so"), pacing issues, and slides you rush through
- **Iterate slides after each rehearsal** — rehearsal is not just practice, it is debugging
- **Day-of checklist**: adapter cables, backup on USB, water bottle, slide PDF backup on phone, presenter remote with fresh batteries

## Emitted Artifact

`Presentation Package` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `accepted paper` → scores `Presentation Package`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below; A–H matrix `reference/gate-matrix.md`.

- Can a non-expert follow the talk from hook to takeaway without reading the paper?
- Is every slide readable from the back of a 50-person room?
- Does the talk finish within the time limit with 2-minute buffer in rehearsal?
- Do you have a pre-recorded demo backup (if demoing)?
- Have you rehearsed at least 3 times with at least 1 external audience?
