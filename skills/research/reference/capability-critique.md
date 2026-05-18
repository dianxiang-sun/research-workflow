# Capability — Critique & Review Patterns

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

### Generator-Verifier-Reviser Pattern (Aletheia-Inspired)

For high-stakes outputs (Phase 2 design, Phase 3 eval design, Phase 6 key sections):

```
Generator → Verifier → Reviser → Verifier → ... (until approved or 3 rounds)
```

1. **Generator**: Produces the initial output (design doc, paper section, eval plan)
2. **Verifier**: Checks for flaws, hallucinations, logical gaps, unsupported claims
   - Must cite specific evidence for each flaw found
   - Returns: APPROVED or FLAWS_FOUND with list
3. **Reviser**: Takes Generator output + Verifier flaws → produces corrected version
4. Loop back to Verifier until APPROVED or 3 rounds reached
5. If not approved after 3 rounds → escalate to user with full history

This is a more fine-grained alternative to the Adversarial Gate for within-phase quality control.
Use Gate for phase transitions; use G-V-R for critical artifacts within a phase.

### Specialized Agent Patterns

**Worker-Critic Pair** (from academic-research-skills):
For any creative task (writing, design), spawn TWO agents:
- Worker: Generates content
- Critic: Immediately evaluates, finds flaws
- Worker revises based on Critic feedback
- Repeat until Critic approves or 3 rounds reached

Use for: `/research write`, `/research design`, `/research explore`

**CitationAgent contract** (from Anthropic multi-agent blog; enforces G1):
A MANDATORY citations-only post-processing pass for Phase 6 (write) and Phase 7
(review). For EVERY `\cite{}`, record one row of the verdict table:

`| citekey | source 1 | source 2 | metadata match | retraction | verdict | action |`

- `source 1/2` — two independent metadata sources (Crossref / Unpaywall / OpenAlex /
  Semantic Scholar), each named with the ID or URL actually checked
- `metadata match` — do title / authors / year / venue agree across both? yes/no
- `retraction` — `clear` / `retracted` / `erratum`
- `verdict` — `verified` (≥2 sources agree, not retracted) / `unverifiable` / `retracted` / `mismatch`
- `action` — for any non-`verified` row: `removed` / `replaced` / `logged-to-GAP_REPORT`

A `\cite{}` not `verified` MUST NOT ship. The completed verdict table is a required
field of the Phase 6/7 artifact and is checked at the Gate.

**Citation Context Analysis** (inspired by scite.ai):
When evaluating related work, classify each citation as:
- **Supporting**: Paper X confirms our approach
- **Contrasting**: Paper Y contradicts our claim
- **Mentioning**: Paper Z is tangentially related
This prevents misrepresenting cited work.

### Candidate-Level Novelty Check (Phase 0 — DD2)

Run at idea-SELECTION time, two tiers — distinct from `novelty-watch` (freshness
monitoring) and the Phase-2 Novelty Stress Test (method-design time):

- **Quick** (Converge — every surviving candidate): 2-3 targeted searches → closest
  prior work + overlap **HIGH / MED / LOW**.
- **Deep** (Refine — the chosen direction only): multi-source search, optionally
  cross-checked by a different model (cross-model adversarial check — cf.
  `phases/phase-7-review.md` §1b) → a closest-work table + a categorical verdict
  **PROCEED / CAUTION / ABANDON** + a one-line positioning statement.

The verdict is a novelty *judgement*, not an action: it is a cited reason feeding the
Converge `novelty` disposition filter — an `ABANDON` candidate is dispositioned
park / revise / escalate and recorded in `findings.md`, never silently dropped. Emit the
overlap tier + verdict into the Research Direction Card's `candidate novelty` field
(`reference/capability-artifacts.md`). Never collapse novelty to a numeric score.
