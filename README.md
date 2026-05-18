# research-workflow

An end-to-end research workflow skill for Claude Code — direction exploration through
paper writing, simulated peer review, and rebuttal, with an adversarial validation Gate
at every phase transition. Domain- and venue-agnostic; supports multiple paper types
(systems, empirical, benchmark, survey, theory).

## Install

```
/plugin marketplace add dianxiang-sun/research-workflow
/plugin install research-workflow@research-workflow
```

## Use

The skill is invoked namespaced:

```
/research-workflow:research <mode> [args]
```

Start with `/research-workflow:research init` to set up a project, then `explore`.

Modes: `init` · `status` · `explore` · `foundation` · `design` · `pilot` · `eval-design` ·
`implement` · `experiment` · `write` · `review` · `rebuttal` · `gate` · `rollback` · `risk` ·
`cost` · `novelty-watch` · `present` · `evolve` · `mine-patterns` · `advisor-prep`.

## Runtime state

Learning state (reflections, rules, outcomes, learned routes) lives **outside** the plugin
bundle:

- default: `~/.claude/research/memory/`
- override: set `RESEARCH_SKILL_STATE_DIR` to an **absolute, writable directory**.

A fresh install starts cold — no accumulated rules / reflections / outcomes; the skill
learns from your usage.

## Optional: semantic-router hook

`semantic_router.py` can power a `UserPromptSubmit` hook that auto-suggests the right mode.
It is **opt-in** — the skill is fully correct without it; `/research-workflow:research <mode>`
is the canonical dispatch path.

## Scope & ethics

See [SCOPE-AND-ETHICS.md](SCOPE-AND-ETHICS.md). In brief: the simulated peer review is a
pre-mortem self-review of your **own** work — never a substitute for, or an undisclosed
input to, a real venue peer review.

## License

MIT — see [LICENSE](LICENSE).
