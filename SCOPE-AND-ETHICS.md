# Scope & Ethics

Read this before using the `review` mode or the Adversarial Gate.

## Simulated peer review is self-review (Global Rule G9)

`/research-workflow:research review` and the multi-persona reviewer personas (Phase 7;
the Adversarial Gate) **simulate** peer review. They are a **pre-mortem self-review of the
authors' OWN work**, run by or for that work's authors to surface weaknesses before
submission. They carry no venue authority.

- NEVER present a simulated review, or its scores, as a genuine external / venue peer review.
- NEVER run this skill to produce an AI-generated review for a manuscript you have been
  assigned to peer-review, or for any confidential submission — that is undisclosed AI peer
  review, which venues prohibit.
- On a third party's manuscript, `review` is valid ONLY as that manuscript's authors' own
  self-review aid (you are a co-author, or its authors asked you).

## Cross-model review transmits the manuscript to an external API

Phase 7 §1b (Cross-Model Adversarial Review) is optional; if used, it calls a **different**
LLM's API with the paper content — transmitting your manuscript to an external service.
Before using it, confirm you may disclose the manuscript to that provider and that doing
so breaches no venue-confidentiality rule or co-author agreement. Skip §1b if in doubt.

## Conservative autonomy default

A fresh install defaults `autonomy_level` to `checkpoint` — the skill pauses at every
Adversarial Gate and before every must-log decision. It never inherits a high-autonomy
setting; opting up to `gate-only` or `full-auto` is an explicit, per-project choice.
Mandatory checkpoints (new spending, a new external-facing claim, a reviewer commitment,
an irreversible submission edit) pause at every level.

## Attribution

This skill cites, as named inspirations, patterns from `academic-research-skills`
(CC BY-NC 4.0), the Stanford Agentic Reviewer rubric, and the ARIS pattern. These are
idea-level attributions; the skill's own text is original and MIT-licensed.
