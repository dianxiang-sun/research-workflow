# Skill Evolution Protocol (`/research evolve`)

> Analyze accumulated reflection / rule / outcome data to refine routing, rules, and gates over time — propose, never auto-apply.

## Applies to: ALL paper types (meta-protocol)

## Scope (READ FIRST)

`/research evolve` is a **proposal pipeline with a per-item human-approval gate**, not autonomous self-modification. It produces TWO apply paths, and the user controls both:

| Apply path | What it changes | How it's applied |
|---|---|---|
| **runtime** | `rules.jsonl` / `outcomes.jsonl` / `routes.json` under `${RESEARCH_SKILL_STATE_DIR}` (default `~/.claude/research/memory/`) | `research-reflect boost-rule\|retire-rule` / `research-router add-example`, after per-item user approval |
| **bundle proposal** | `phases/*.md` / `reference/*.md` / `tools/semantic_router.py` `DEFAULT_ROUTES` — skill files inside the plugin cache, which is read-only on public installs | Emits a markdown proposal document under `${RESEARCH_SKILL_STATE_DIR}/proposals/`; the maintainer applies it inside a clone of `~/code/research-workflow` and re-releases |

Public users get the runtime half end-to-end. Bundle changes become a paper trail the maintainer can act on; the skill never writes into its own bundle.

A single proposal record MAY mix both lists (e.g. promote a rule AND propose a gate question that references it).

## Protocol

### Step 1 — Data

Read the raw JSONL files under `${RESEARCH_SKILL_STATE_DIR}` (default `~/.claude/research/memory/`):

- `rules.jsonl` — id, phase, rule text, confidence, times_tested, times_validated, source, status
- `outcomes.jsonl` — skill_mode, task, approach, score, failure_reasons
- `reflections.jsonl` — id, skill_mode, result, what_happened, lesson

Do NOT rely on `research-reflect query-*` for analysis — its human-formatted output strips id / phase / counters that Step 2 needs. Use `research-reflect stats` only for the cold-start sanity exit.

If all three files are empty or missing, there is nothing to evolve — exit. Otherwise record date + per-file record counts as the evolution baseline; compute the Health Score (below).

### Step 2 — Pattern Analysis

**2a. Rule promotion (soft → hard)** — rules with `times_tested ≥ 5` and `confidence ≥ 0.7`. **Fresh-rule guard**: a rule with `times_tested < 3` is treated as "strong soft", **never promotable to hard**, even if `confidence ≥ 0.7` — this defends against one-shot hardening from `boost-rule` (which currently lifts a 0.5 rule to 0.99 / hard in a single call; see backlog **L8**). If only one of (frequency, confidence) holds, flag as "strong soft rule, monitor one more cycle".

**2b. Rule retirement** — rules with `times_tested ≥ 5` and `confidence ≤ 0.3`. Distinguish "wrong rule" (consistently bad) from "rarely triggered" (few opportunities). Wrong → propose retirement with a replacement candidate if a pattern exists. Rarely triggered → propose rewording the trigger condition, not retirement.

**2c. New gate question discovery** — scan `reflections.jsonl` for ≥ 3 occurrences of the same root-cause failure. Formulate a yes/no, specific, testable gate question that would have caught it earlier; pick the phase whose existing gate criteria should host it.

**2d. Route example expansion** — scan reflections for user phrasings where `research-router route "<phrase>"` returned no match or the wrong mode. For each missed phrase, propose adding it as an example to the correct mode. Verify the new example does not collide with another mode's tokens (`research-router route` returns the candidate phrase itself as the top hit only for the intended mode).

(Dead-mode analysis — "modes with 0 uses since last evolution" — is intentionally **NOT** in MVP: it requires an invocation counter `reflect.py` does not emit. Tracked as a backlog item for a future increment.)

### Step 3 — Proposal Generation

For each pattern from Step 2, emit a **proposal record** with two parallel lists. Every entry MUST cite ≥ 3 data points (`reflection_id` / `outcome_id` / `rule_id`).

```yaml
proposal_id: <slug>
runtime_actions:
  - action: boost-rule | retire-rule | add-route-example
    target: <rule_id or mode_name>
    args: <CLI args, ready to execute>
    rationale: <one-liner>
    evidence_refs: [<reflection_id | outcome_id | rule_id>, ...]
bundle_changes:
  - file: phases/phase-N.md | reference/<file>.md | tools/semantic_router.py
    change_type: new-gate | reword-phase | router-default-edit | policy-update
    snippet: <suggested unified diff or replace-block>
    rationale: <one-liner>
    evidence_refs: [...]
```

### Step 4 — User Review

Present the proposal record(s) as a numbered list — `runtime_actions` first, `bundle_changes` second. Per entry show: change, evidence refs, risk if rejected, apply path. The user approves, rejects, or modifies each individually. Rejected entries log to the runtime evolution log (`${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` § Skill Update Proposals) with reason and may resurface in a later cycle.

### Step 5 — Application

**Before any apply — first-time setup of the runtime evolution log.** If `${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` does not yet exist, create it (mkdir -p the directory; Write the file) with these six section headers — they are the schema that Steps 5a/5b append into:

```
# Research Skill Evolution Log (runtime)

## Learned Anti-Patterns

## Custom Gate Questions

## Keyword Supplements

## Project Lessons

## Skill Update Proposals

## Runtime Apply Manifest
```

The bundle file `skills/research/evolution.md` is **legacy pre-H2 scaffolding** — not read or written by `/research-workflow:research` after H2. Removal of the bundle file is tracked by backlog **M4** (separate cleanup); it remains in the bundle for now as a structural reference.

**5a. Runtime apply (per approved `runtime_actions` entry).** Before executing the CLI action:

1. Append a one-line **undo manifest** record to the runtime evolution log (`${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` § Runtime Apply Manifest) containing the pre-edit state — for `boost-rule` / `retire-rule`, the rule's current `rules.jsonl` line; for `add-route-example`, the route's pre-edit example list. This is the rollback paper trail — there is no git-level revert for runtime state.
2. Execute the CLI: `research-reflect boost-rule --rule-id <id>` / `research-reflect retire-rule --rule-id <id>` / `research-router add-example --mode <m> --phrase "<p>"`.
3. Append the apply-success line to the appropriate `evolution-log.md` section (under `${RESEARCH_SKILL_STATE_DIR}`) per change semantics (Learned Anti-Patterns / Project Lessons / Keyword Supplements).

**5b. Bundle proposal (per approved `bundle_changes` entry).**

1. `mkdir -p "${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/proposals"`.
2. Write `proposal-<UTC-yyyymmddTHHMMSS>-<short-slug>.md` with this schema:

```markdown
---
created: <UTC ISO 8601, to the second>
source_evidence_refs: [<reflection_id | outcome_id | rule_id>, ...]
target_files: [phases/phase-N.md, reference/<file>.md, ...]
change_type: new-gate | reword-phase | router-default-edit | policy-update
scope: skill-bundle | project-local
project_context: <project name or "n/a">
redaction_note: <"none" | "sensitive content scrubbed: <what>">
status: proposed
---

## Why
<rationale, with evidence quotes>

## Proposed change
<unified diff or replace-block>

## Maintainer handoff
1. `cd ~/code/research-workflow` (or another writable clone of the bundle).
2. Apply the diff to the listed target_files.
3. Re-run the § Budget & Structure Check (G8) sweep in that clone.
4. Bump plugin version; commit; re-release.
```

3. Append a one-liner to the runtime evolution log (`${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` § Skill Update Proposals): `- [DATE] [TARGET_FILES] [CHANGE_TYPE]: <description> (proposal: <path>, status: proposed)`.

**There is no `git commit` step inside `/research evolve`.** Public installs run from a read-only plugin cache; the maintainer's clone receives bundle changes via the proposal documents.

### Step 6 — Verification

Run the G8 mechanical hook (see § Budget & Structure Check below):

- The 8-check structural sweep
- The dispatcher-shape check (`SKILL.md` `wc -l` ≤ ~400, no fenced block > ~15 lines)
- The `wc -l` trend (reported only — never a reject reason on its own)

Additional, when runtime changes applied:

- `research-router rebuild-index` — only if any `add-route-example` applied
- `research-reflect stats` — sanity (the tool still loads after JSONL edits)

The "one recent reflection still routes correctly" smoke from earlier versions is removed: it produced false-positive failures whenever the input had no router-touching changes, and conflated "tool returns" with "routing logic is correct".

## Health Score

Computed in Step 1 to gauge whether evolution is premature:

```
Score = min(outcomes / 20, 1.0)
      + min((2 * hard_rules + soft_rules) / 10, 1.0)
      + 0.5 * min(reflections / 3, 1.0)
```

| Score | Maturity | Recommended Cadence |
|---|---|---|
| < 0.75 | Cold start | Keep using the skill; revisit after ≥ 20 outcomes or ≥ 5 hard rules |
| 0.75 – 1.75 | Learning | Evolve monthly |
| ≥ 1.75 | Mature | Evolve quarterly |

The previous formula `(3 * hard + soft + 0.5 * outcomes) / max(total_invocations, 1)` used a denominator `reflect.py` does not emit (`total_invocations`), and produced 3.0 for the absurd "one hard rule, no outcomes" case. The new shape is bounded (0 – 2.5), monotonic in each dimension, and rewards evidence breadth across rules / outcomes / reflections.

Report the score at the start of every evolution run.

## Budget & Structure Check (G8)

Run by `/research evolve` (and, during the restructure, by each migration phase) — the
standing enforcement of Global Rule **G8**. NOT a CI job and NOT new tooling: the same
kind of mechanical check the skill already does.

### Mechanical hook

1. **`wc -l` trend** — count the skill's `*.md` + `templates/research-state.yaml`;
   report the delta + cumulative vs the 3143 baseline. Reported for visibility — a
   positive delta is NOT a reject reason (§15).
2. **Structural sweep — 8 checks, each pass/fail:**
   1. every router-table mode in `SKILL.md` resolves to a phase / capability;
   2. every gated `phases/` file (all but `phase-writing-memory.md`, which has no gate)
      has an `## Emitted Artifact` section and a `## Gate Criteria` whose first line is
      a `> **Rubric contract** —` header naming input · emitted artifact · verdict;
   3. no live cross-reference points to an M2-retired file — `phase-progress-tracker.md`
      or the flat `research-progress` / `research-risks` / `research-decisions` files —
      except the sanctioned `SKILL.md` one-release fallback, `capability-artifacts.md`,
      and this G8 spec naming them;
   4. the Phase-3 mandatory-question count is identical in every file that states it;
   5. the skill loads — frontmatter intact, `research-state.yaml` parses, `/research status` dispatches.
   6. no `python3 reflect.py` / `python3 semantic_router.py` bare invocations — tools are
      always called via the `research-reflect` / `research-router` wrapper names (H1 anchor);
   7. no user-facing bare `/research <mode>` in `reference/dispatch-recipes.md`, `../../README.md`,
      anywhere under `templates/` (recursive), or as a quoted literal in `tools/*.py` — runtime
      output / user-typing strings use canonical `/research-workflow:research <mode>` (M1 anchor;
      SKILL.md "canonical"). Heuristic on `tools/*.py`: fragmented Python forms (split-print,
      str-concat across literals, `.join` over fragments) are NOT caught — APPLY artifact below;
   8. every `*.md` line that mentions `/verify-before-write` or `/verify-citations` (G1
      companion commands) also carries a substring fallback marker — `installed`,
      `otherwise`, `fallback`, `inline manual`, `re-open`, or `MUST` — as a *heuristic
      missing-marker lint* (necessary but NOT sufficient — semantic fallback check is
      REQUIRED at G8 APPLY manual review of every modified `/verify-*` line; H3 anchor).
3. **Dispatcher-shape check** — `wc -l SKILL.md` ≤ ~400, and no fenced code block in
   `SKILL.md` exceeds ~15 lines.

Concrete read-only checks:
- rubric headers — `grep -LF '**Rubric contract**' phases/phase-*.md` lists any gated
  phase missing the header (only `phase-writing-memory.md` is expected).
- retired-file pointers — `grep -rl 'phase-progress-tracker\|research-progress\|research-risks\|research-decisions' --include='*.md' . | grep -vE 'phase-evolve|SKILL|capability-artifacts'` must be empty (the G8 spec, the `SKILL.md` one-release fallback, and `capability-artifacts.md` legitimately name these retired tokens; any other hit is a dangling pointer).
- Phase-3 count — `grep -rhoE 'MANDATORY 1[0-9]' --include='*.md' .` must read "12" everywhere.
- dispatcher-shape — `wc -l SKILL.md`, then scan `SKILL.md` for a code-fence pair more than ~15 lines apart.
- tool naming (sweep #6) — `find . \( -name '*.md' -o -name '*.py' \) ! -path './phases/phase-evolve.md' -print0 | xargs -0 grep -nE 'python3 (reflect|semantic_router)\.py'` must be empty (the G8 spec itself names these tokens at the exact path `./phases/phase-evolve.md`; any other file hit is drift back to bare invocation) (H1 anchor). Run with cwd = `skills/research/`.
- canonical command (sweep #7) — all four must be empty:
  (a) `grep -nE '/research [A-Za-z0-9_-]+' reference/dispatch-recipes.md ../../README.md`
  (b) `grep -rnE '/research [A-Za-z0-9_-]+' templates/`
  (c) `grep -nE "['\"][[:space:]]*/research [A-Za-z0-9_-]*" tools/*.py`
  (d) `grep -nE "['\"]/research['\"]" tools/*.py`
  Shorthand `/research <mode>` remains legal *inside* `SKILL.md` / `phases/` / `reference/` prose (see SKILL.md "canonical" anchor). Symlinked `templates/` subdirs are out of scope for (b) — BSD `grep -r` does not traverse symlinks by default; reviewer manually inspects at G8 APPLY. Fragmented Python forms (split-print, str-concat across literals, `.join` over fragments) are heuristic-only NOT caught by (c)/(d); APPLY artifact: `git diff -- skills/research/tools/*.py | grep -nE '^\+[^+].*\bresearch\b'` reviewed manually.
- verify fallback (sweep #8) — `find . -name '*.md' ! -path './phases/phase-evolve.md' -print0 | xargs -0 grep -nE '/verify-(before-write|citations)' | grep -vE 'installed|otherwise|fallback|inline manual|re-open|MUST'` must be empty. Heuristic missing-marker check (necessary but NOT sufficient — reverse-semantic lines carrying a marker still pass). APPLY artifact: `git diff -- skills/research/ | grep -nE '^\+.*\b/verify-(before-write|citations)\b'` output, with each resulting line annotated by reviewer as `fallback in place` or `reverse-semantic risk` (H3 anchor).

### Budget & Structure checklist (required artifact)

Every `/research evolve` change proposal (and every restructure migration-phase
proposal) MUST carry: (a) the `wc -l` delta + cumulative trend; (b) each new
`reference/`/`templates/` file's D-diagnosis / R-item justification; (c) each change
classified — *relocation* (names its paired delete) or *net-new gap-fill* (names the
D/R item); (d) a DRY / pointer audit.

G8 **REJECTS** a proposal that omits the checklist, or that fails the structural sweep
or the dispatcher-shape check — **never** on a positive line-count delta alone. The
checklist's *presence* is mechanical; its *content* is the judgement reviewed at the
APPLY gate.

## Emitted Artifact

`Evolution Log entry` — required fields & provenance: `reference/capability-artifacts.md`.

## Gate Criteria

> **Rubric contract** — input `accumulated reflection / rule / outcome data + proposal record(s)` → scores `Evolution Log entry`; verdict **PASS / CONDITIONAL / BLOCK**; dimensions = the criteria below.

- Does the Health Score support evolution (≥ 0.75)? If not, defer.
- Has it been ≥ 2 weeks since the last evolution? (Avoid thrashing.)
- Did every proposal entry cite ≥ 3 evidence refs?
- Did the user explicitly approve each applied entry?
- For runtime applies, was the pre-state recorded to `${RESEARCH_SKILL_STATE_DIR:-$HOME/.claude/research/memory}/evolution-log.md` § Runtime Apply Manifest BEFORE the CLI ran?
- For bundle proposals, does each `proposal-*.md` carry the full schema (frontmatter + Why + Proposed change + Maintainer handoff)?
- Does `research-router rebuild-index` complete without errors (if any route changes applied)?
