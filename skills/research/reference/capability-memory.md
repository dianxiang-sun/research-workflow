# Capability — Three-Tier Memory

> Reference detail for the `research` skill, carved out of `SKILL.md` in the M1 restructure (pure relocation, zero behavior change). `SKILL.md` is the dispatcher and points here.

### Mechanism 4: Three-Tier Memory Architecture (MemGPT/Letta Pattern)

```
Tier 1 — Core Memory (always loaded):
  SKILL.md + current phase file
  → Base protocols, global rules, gate matrix

Tier 2 — Session Memory (per-session scratch):
  What happened this session, decisions made, files edited
  → Claude's native conversation context

Tier 3 — Archival Memory (persistent, searchable):
  ~/.claude/research/memory/
  ├── reflections.jsonl   ← what went wrong + lessons (Reflexion)
  ├── rules.jsonl         ← IF/THEN predicate rules with confidence (MPR)
  ├── outcomes.jsonl      ← task→approach→score history (CrewAI)
  └── routes.json         ← learned trigger examples (Semantic Router)

At invocation: search Tier 3 for relevant entries → inject into Tier 1.
After execution: write new entries to Tier 3.
```

> Runtime state resolves **outside** the skill bundle (`RESTRUCTURE-PLAN.md` §14.4): `$RESEARCH_SKILL_STATE_DIR` if set, else the `~/.claude/research/memory/` default above. A fresh install starts cold — no accumulated reflections/rules/outcomes, base routes only.
